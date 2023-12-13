from exchangelib import Account, FileAttachment, Message, Configuration, Credentials
from exchangelib.errors import ErrorNonExistentMailbox, ErrorInvalidServerVersion
from exchangelib.protocol import BaseProtocol

# Установите автоматическое обнаружение сервера Outlook (если нужно)
BaseProtocol.HTTP_ADAPTER_CLS.allow_redirects = False

email, password = "galimovdv@outlook.com", "MRC-qCm-6ec-FKN"
server = 'outlook.office365.com'  # или другой сервер по вашему усмотрению

try:
    config = Configuration(server=server, credentials=Credentials(email, password))
    account = Account(primary_smtp_address=email, config=config, autodiscover=False, access_type='delegate')
    print('Авторизация успешна!')

    # Отправка письма с вложением
    subject = 'Subject of email'
    body = 'Body of email'
    attachment_path = '.gitignore'

    message = Message(
        account=account,
        folder=account.sent,
        subject=subject,
        body=body,
        to_recipients=['galimovdv@yandex.ru']
    )

    with open(attachment_path, 'rb') as f:
        attachment = FileAttachment(name=attachment_path.split('/')[-1], content=f.read())
        message.attach(attachment)

    message.send_and_save()
    print('Сообщение с вложением отправлено.')

    # Скачивание вложений входящего письма
    folder = account.inbox

    for item in folder.all().order_by('-datetime_received')[:10]:  # выберите количество писем для скачивания вложений
        print(f"Скачиваем вложения из письма '{item.subject}' от {item.sender}")

        for attachment in item.attachments:
            if isinstance(attachment, FileAttachment):
                local_path = f'attachments/{attachment.name}'
                with open(local_path, 'wb') as f:
                    f.write(attachment.content)
                print(f'Скачали вложение "{attachment.name}" и сохранили в  "saved_attachments".')

except ErrorNonExistentMailbox:
    print('Почтовый ящик не существует или неправильный логин / пароль')
except ErrorInvalidServerVersion:
    print('Указан неправильный сервер или версия сервера')
