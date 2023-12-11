import json
from kafka import KafkaProducer

class kafkaEventsProducer:
    def __init__(self, bootstrap_servers,):
        self.kafka_producer = KafkaProducer(bootstrap_servers=bootstrap_servers, api_version=(0, 10))

    def publish_message(self, topic_name, key, value):
        try:
            key_bytes = bytes(key, encoding='utf-8')
            value_bytes = bytes(value, encoding='utf-8')
            self.kafka_producer.send(topic_name, key=key_bytes, value=value_bytes)
            self.kafka_producer.flush()
            print('Message published successfully.')
        except Exception as ex:
            print(str(ex))

