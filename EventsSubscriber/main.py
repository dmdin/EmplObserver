import os
from dotenv import load_dotenv
from KafkaSubscriber.KafkaSubscriber import KafkaEventsConsumer

load_dotenv()

kafkaHost = os.getenv('KAFKA_HOST')
kafkaPort = os.getenv('KAFKA_PORT')

kafkaServer = f'{kafkaHost}:{kafkaPort}'

def consume_messages():
    try:
        consumer = KafkaEventsConsumer("winEvents", [kafkaServer])

        for message in consumer.consume():
            print(message)
    except Exception as err:
        print(err)
        consume_messages()



consume_messages()