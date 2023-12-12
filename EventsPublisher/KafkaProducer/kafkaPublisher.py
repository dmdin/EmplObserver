from kafka import KafkaProducer

class kafkaEventsProducer:
    def __init__(self, 
                 bootstrap_servers,
                 sasl_plain_username, 
                 sasl_plain_password):
        self.kafka_producer = KafkaProducer(
            # sasl_plain_username = sasl_plain_username,
            # sasl_plain_password = sasl_plain_password,
            bootstrap_servers = bootstrap_servers,
            # security_protocol='SASL_PLAINTEXT',
            # sasl_mechanism='PLAIN',
            api_version=(0, 10))
        self.count_events = 0

    def publish_message(self, topic_name, key, value):
        try:
            key_bytes = bytes(key, encoding='utf-8')
            value_bytes = bytes(value, encoding='utf-8')
            print(len(key_bytes))
            print(len(value_bytes))
            self.kafka_producer.send(topic_name, key=key_bytes, value=value_bytes)
            self.kafka_producer.flush()
                 
            self.count_events+=1
            print(f'Message published successfully: {self.count_events}')
        except Exception as ex:
            print(str(ex))