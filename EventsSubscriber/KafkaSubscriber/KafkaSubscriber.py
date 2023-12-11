from json import loads 
from kafka import KafkaConsumer 

class KafkaEventsConsumer:

    def __init__(self, topic, bootstrap_servers):
        self.consumer = KafkaConsumer( 
                topic, 
                bootstrap_servers = bootstrap_servers, 
                auto_offset_reset = 'earliest', 
                enable_auto_commit = True, 
                group_id = 'event-subscriber-group', 
                value_deserializer = lambda x : loads(x.decode('utf-8')) 
            ) 
        
    def consume(self):
        for message in self.consumer: 
            yield message.value
    