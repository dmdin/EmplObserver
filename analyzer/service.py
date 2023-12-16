import datetime
import time
from functools import wraps
from exchangelib import Credentials, Account, EWSDateTime, EWSTimeZone, Q
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
import requests
import re
from transformers import pipeline
from database import UserStatistic, User
import datetime
import schedule
import csv
from file_manager import send_week_stats
from api import run_fastapi
from ml_model import predict

requests.packages.urllib3.disable_warnings()

BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter
tz = EWSTimeZone('UTC')
from database import get_users

def check_mail_iteration():
    manager_user_stats = {}

    try:
        for user in get_users():
            try:
                stats = calculate_user_statistics(user)

                if user.manager in manager_user_stats:
                    manager_user_stats[user.manager].append(stats)
                else:
                    manager_user_stats[user.manager] = [stats]
                break
            except Exception as ex:
                print(f"Ошибка рассчета статистик для сотрудника: {user.domainEmail}. {ex}")

        send_report(manager_user_stats)
    except Exception as ex:
        print(ex)


def send_report(manager_user_stats):
    for manager in manager_user_stats:
        csv_file_path = 'temp.csv'

        with open(csv_file_path, 'w', newline='') as file:
            fieldnames = ["Пользователь", "Вероятность увольнения"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for user in manager.users:
                writer.writerow({"Пользователь":user.domainEmail, "Вероятность увольнения": 0.5 })

        send_week_stats(manager.domainEmail)


def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        time_elapsed = end_time - start_time
        print(f"Функция {func.__name__} исполнилась за {time_elapsed:.6f} секунд(ы).")
        return result
    return wrapper

@timing_decorator
def sent_messages_count(account,
                        start_date = EWSDateTime(2021, 1, 1, tzinfo=tz),
                        end_date = EWSDateTime(2025, 12, 31, tzinfo=tz)):
    # 1. Количество отправленных сообщений за период
    sent_folder = account.sent
    q = Q(datetime_received__range=(start_date, end_date))
    return sent_folder.filter(q).count()


@timing_decorator
def received_messages_count(account,
                            start_date = EWSDateTime(2021, 1, 1, tzinfo=tz),
                            end_date = EWSDateTime(2025, 12, 31, tzinfo=tz)):
    # 2. Количество получаемых сообщений за период
    inbox_folder = account.inbox
    q = Q(datetime_received__range=(start_date, end_date))
    return inbox_folder.filter(q).count()


@timing_decorator
def recipient_counts(messages):
    # 3. Количество адресатов в отправляемых сообщениях
    count = sum(len(msg.to_recipients) for msg in messages)
    return count


@timing_decorator
def bcc_count(messages):
    # 4. Количество сообщений с адресатами в поле «скрытая копия»
    return sum(1 for msg in messages if msg.bcc_recipients)


@timing_decorator
def cc_count(messages):
    # 5. Количество сообщений с адресатами в поле «копия»
    return sum(1 for msg in messages if msg.cc_recipients)


@timing_decorator
def read_messages_later_than(messages, hours):
    # 6. Количество сообщений, прочитанных позднее времени
    # получения на Х часов. Принять Х как параметр настройки с
    # начальным значением 4 часа
    count = 0
    for msg in messages:
        if msg.is_read and (msg.datetime_received + datetime.timedelta(hours=hours) < msg.last_modified_time):
            count += 1
    return count

@timing_decorator
def days_between_received_and_read(messages):
    # 7. Количество дней между датой получения и датой прочтения сообщения
    days_diff = []
    for msg in messages:
        if msg.is_read:
            days_diff.append((msg.last_modified_time - msg.datetime_received).days)
    return days_diff


@timing_decorator
def replied_messages_count(account, received_messages):
    # 8. Количество сообщений, на которые произведен ответ
    replied_msg_ids = set(account.sent.all())
    return sum(1 for msg in received_messages if msg.message_id in replied_msg_ids)


@timing_decorator
def sent_characters_count(messages):
    # 9. Количество символов текста в исходящих сообщениях
    messages = [msg.text_body.split('________________________________')[0].strip() for msg in messages]

    return sum(len(''.join(c for c in msg if c.isprintable())) for msg in messages)


@timing_decorator
def messages_outside_working_hours(messages, working_hours=(9, 18)):
    # 10. Количество сообщений, отправленных вне рамок рабочего дня
    count = 0
    for msg in messages:
        if msg.datetime_created.hour < working_hours[0] or msg.datetime_created.hour > working_hours[1]:
            count += 1
    return count


@timing_decorator
def received_to_sent_ratio(received_count, sent_count):
    # 11. Соотношение количества полученных и отправленных сообщений
    return received_count / max(1, sent_count)


@timing_decorator
def bytes_received_to_sent_ratio(received_messages, sent_messages):
    # 12. Соотношение объема в байтах получаемых и отправляемых сообщений
    received_messages = [''.join(c for c in msg.text_body if c.isprintable()) for msg in received_messages]
    received_bytes = sum(len(msg.encode('utf-8')) for msg in received_messages)
    sent_bytes = sum(
        len(msg.text_body.split('________________________________')[0].strip().encode('utf-8'))
        for msg in sent_messages)
    return received_bytes / max(1, sent_bytes)

@timing_decorator
def messages_with_question_and_no_reply(account, messages):
    # 13. Количество входящих сообщений, имеющих вопросительные
    # знаки в тексте (исключая ссылки), но на которые не был направлен ответ
    count = 0
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    for msg in messages:
        text_without_urls = re.sub(url_pattern, '', msg.text_body)
        if '?' not in text_without_urls:
            continue
        reply_exists = False
        for sent_msg in account.sent.filter(in_reply_to=msg.message_id):
            reply_exists = True
            break

        if not reply_exists:
            count += 1

    return count

def get_start_date():
    now = datetime.datetime.now()
    now -= datetime.timedelta(days=7)

    return EWSDateTime(now.year, now.month, now.day, tzinfo=tz)

def get_end_date():
    now = datetime.datetime.now()

    return EWSDateTime(now.year, now.month, now.day, tzinfo=tz)

def get_predictions():
    clf = pipeline(
        task='sentiment-analysis',
        model='SkolkovoInstitute/russian_toxicity_classifier')
    messages = get_sent_messages()
    return list(zip(messages, clf(messages)))


def get_sent_messages(account,
                      start_date=EWSDateTime(2021, 1, 1, tzinfo=tz),
                      end_date=EWSDateTime(2025, 12, 31, tzinfo=tz)):
    # Получение списка отправленных сообщений за период
    sent_folder = account.sent
    q = Q(datetime_received__range=(start_date, end_date))
    messages = list(sent_folder.filter(q))
    m = messages[0]
    messages = [msg.text_body.split('________________________________')[0].strip() for msg in messages]
    return [''.join(c if c.isprintable() else ' ' for c in msg) for msg in messages]

def get_negative_messages_percent(account,
                                  start_date=EWSDateTime(2021, 1, 1, tzinfo=tz),
                                  end_date=EWSDateTime(2025, 12, 31, tzinfo=tz)):
    results = get_sent_messages(
        account,
        start_date,
        end_date)
    return sum(1 for i in results if i['label'] == 'toxic')/len(results)

def calculate_user_statistics(user: User):

    start_date = get_start_date()
    end_date = get_end_date()

    # Аутентификация и подключение к учетной записи Outlook
    credentials = Credentials(user.domainEmail, user.password)
    account = Account(primary_smtp_address=user.domainEmail, credentials=credentials, autodiscover=True, access_type='delegate')


    sent_messages = list(filter(lambda v: v is not None, account.sent.filter(datetime_received__range=(start_date, end_date))))
    received_messages = list(filter(lambda v: v is not None, account.inbox.filter(datetime_received__range=(start_date, end_date))))

    # Примеры вызовов функций
    sent_messages_count_val =  sent_messages_count(account, start_date, end_date)
    received_messages_count_val =  received_messages_count(account, start_date, end_date)
    recipient_counts_val = recipient_counts(sent_messages)
    bcc_count_val = bcc_count(sent_messages)
    cc_count_val =  cc_count(sent_messages)
    read_messages_later_than_val = read_messages_later_than(received_messages, 4)
    days_between_received_and_read_val = days_between_received_and_read(received_messages)
    replied_messages_count_val = replied_messages_count(account, received_messages)
    sent_characters_count_val = sent_characters_count(sent_messages)
    messages_outside_working_hours_val = messages_outside_working_hours(sent_messages)
    received_to_sent_ratio_val = received_to_sent_ratio(len(received_messages), len(sent_messages))
    bytes_received_to_sent_ratio_val = bytes_received_to_sent_ratio(received_messages, sent_messages)
    messages_with_question_and_no_reply_val = messages_with_question_and_no_reply(account, received_messages)

    statistic = UserStatistic(
        user = user,
        sendMessagesCount = sent_messages_count_val,
        receivedMessagesCount =  received_messages_count_val,
        recipientCounts = recipient_counts_val,
        bccCount = bcc_count_val,
        ccCount = cc_count_val,
        daysBetweenReceivedAndRead = days_between_received_and_read_val,
        repliedMessagesCount = replied_messages_count_val,
        sentCharactersCount = sent_characters_count_val,
        messagesOutsideWorkingHours = messages_outside_working_hours_val,
        receivedToSentRatio = received_to_sent_ratio_val,
        bytesReceivedToSentRatio = bytes_received_to_sent_ratio_val,
        messagesWithQuestionAndNoReply = messages_with_question_and_no_reply_val,
        readMessagesMoreThan4Hours = read_messages_later_than_val,
        startInterval = start_date,
        endInterval = end_date,
            toxic_messages_percent = get_negative_messages_percent(account, start_date, end_date)
    )


   # statistic.save()

    return statistic
    

def run_schedule():
    schedule.every(7).days.do(check_mail_iteration)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(run_fastapi)
        executor.submit(run_schedule)

