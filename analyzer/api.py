import datetime
import time
from functools import wraps

from exchangelib import Credentials, Account, EWSDateTime, EWSTimeZone, Q
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
import requests
import re
requests.packages.urllib3.disable_warnings()

BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter
tz = EWSTimeZone('UTC')

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


if __name__ == '__main__':
    # Аутентификация и подключение к учетной записи Outlook
    email, password = "galimovdv@outlook.com", "MRC-qCm-6ec-FKN"
    credentials = Credentials(email, password)
    account = Account(primary_smtp_address=email, credentials=credentials, autodiscover=True, access_type='delegate')

    # Получение диапазона дат и сообщений с указанием часового пояса
    start_date = EWSDateTime(2021, 1, 1, tzinfo=tz)
    end_date = EWSDateTime(2025, 12, 31, tzinfo=tz)
    sent_messages = list(filter(lambda v: v is not None, account.sent.filter(datetime_received__range=(start_date, end_date))))
    received_messages = list(filter(lambda v: v is not None, account.inbox.filter(datetime_received__range=(start_date, end_date))))

    # Примеры вызовов функций
    print("sent_messages_count", sent_messages_count(account, start_date, end_date))
    print("received_messages_count", received_messages_count(account, start_date, end_date))
    print("recipient_counts", recipient_counts(sent_messages))
    print("bcc_count", bcc_count(sent_messages))
    print("cc_count", cc_count(sent_messages))
    print("read_messages_later_than", read_messages_later_than(received_messages, 4))
    print("days_between_received_and_read", days_between_received_and_read(received_messages))
    print("replied_messages_count", replied_messages_count(account, received_messages))
    print("sent_characters_count", sent_characters_count(sent_messages))
    print("messages_outside_working_hours", messages_outside_working_hours(sent_messages))
    print("received_to_sent_ratio", received_to_sent_ratio(len(received_messages), len(sent_messages)))
    print("bytes_received_to_sent_ratio", bytes_received_to_sent_ratio(received_messages, sent_messages))
    print("messages_with_question_and_no_reply", messages_with_question_and_no_reply(account, received_messages))