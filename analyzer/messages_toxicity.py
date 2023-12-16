from exchangelib import Credentials, Account, EWSDateTime, EWSTimeZone, Q
from transformers import pipeline

tz = EWSTimeZone('UTC')


def get_predictions():
    clf = pipeline(
        task='sentiment-analysis',
        model='SkolkovoInstitute/russian_toxicity_classifier')

    return clf(get_sent_messages())


def get_sent_messages(account=
                      Account(primary_smtp_address="galimovdv@outlook.com",
                              credentials=Credentials("galimovdv@outlook.com", "MRC-qCm-6ec-FKN"),
                              autodiscover=True, access_type='delegate'),
                      start_date=EWSDateTime(2021, 1, 1, tzinfo=tz),
                      end_date=EWSDateTime(2025, 12, 31, tzinfo=tz)):
    # Получение списка отправленных сообщений за период
    sent_folder = account.sent
    q = Q(datetime_received__range=(start_date, end_date))
    messages = list(sent_folder.filter(q))
    m = messages[0]
    messages = [msg.text_body.split('________________________________')[0].strip() for msg in messages]
    return [''.join(c if c.isprintable() else ' ' for c in msg) for msg in messages]


print(get_predictions())

"""
    [{'label': 'neutral', 'score': 0.9872767329216003},
     {'label': 'toxic', 'score': 0.985331654548645}]

"""
