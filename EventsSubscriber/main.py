from KafkaSubscriber.KafkaSubscriber import KafkaEventsConsumer



def consume_messages():
    try:
        consumer = KafkaEventsConsumer("winEvents", ['localhost : 9092'])

        for message in consumer.consume():
            print(message)
    except Exception as err:
        print(err)
