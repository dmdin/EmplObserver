import os
from dotenv import load_dotenv
from KafkaSubscriber.KafkaSubscriber import KafkaEventsConsumer
from peewee import *
from database import register_event

load_dotenv()

kafkaHost = os.getenv('KAFKA_HOST')
kafkaPort = os.getenv('KAFKA_PORT')
kafkaUser = os.getenv('KAFKA_USERNAME')
kafkaPassword = os.getenv('KAFKA_PASSWORD')

kafkaServer = f'{kafkaHost}:{kafkaPort}'

def consume_messages():
    try:
        consumer = KafkaEventsConsumer("winEvents", [kafkaServer],
            sasl_plain_username=kafkaUser,
            sasl_plain_password=kafkaPassword)

        for message in consumer.consume():
            print(message)
            if "UserName" in message and "AppName" in message:
                register_event(message["UserName"], message["AppName"])
            else:
                print(f'Некорректное событие')
    except Exception as err:
        print(err)
        consume_messages()



consume_messages()