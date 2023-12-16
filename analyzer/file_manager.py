from exchangelib import Account, FileAttachment, Message, Configuration, Credentials
from exchangelib.errors import ErrorNonExistentMailbox, ErrorInvalidServerVersion
from exchangelib.protocol import BaseProtocol
import os
from dotenv import load_dotenv

load_dotenv()

serviceEmail = os.getenv('SERVICE_EMAIL')
servicePassword = os.getenv('SERVICE_PASSWORD')
serviceServer = os.getenv('SERVICE_SERVER')


BaseProtocol.HTTP_ADAPTER_CLS.allow_redirects = False

def send_week_stats(manager_email): 
    try:
        config = Configuration(server=serviceServer, credentials=Credentials(serviceEmail, servicePassword))
        account = Account(primary_smtp_address=serviceEmail, config=config, autodiscover=False, access_type='delegate')
        print('Авторизация успешна!')

        # Отправка письма с вложением
        subject = 'Еженедельная отправка информации о вовлеченности сотрудников'
        body = 'Добрый день!\nВо вложении файл с информацией об активности сотрудников Вашего подразделения с прогнозом вероятности их увольнения.\nЭто автоматическое письмо, не нужно на него отвечать'

        message = Message(
            account=account,
            folder=account.sent,
            subject=subject,
            body=body,
            to_recipients=['komlevdanila742@gmail.com']
        )
            
        with open("temp.csv", 'rb') as f:
            attachment = FileAttachment(name="results.csv", content=f.read())
            message.attach(attachment)
        message.send_and_save()

        print('Сообщение с вложением отправлено.')

    except ErrorNonExistentMailbox:
        print('Почтовый ящик не существует или неправильный логин / пароль')
    except ErrorInvalidServerVersion:
        print('Указан неправильный сервер или версия сервера')
