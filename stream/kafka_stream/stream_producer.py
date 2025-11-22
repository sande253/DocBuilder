from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient,ConfigResource,NewTopic

import json 
class KafkaProducer:
    #Static ( Single -ton )
    __producer_instance = None 
    __admin_client =None 
    def __init__(self):
        #Future use 
        pass 
    #def create_topic(topic_name ):
        
    def topic_exists(self):
        metadata = KafkaProducer.__admin_client.list_topics()
        print(metadata.topics)
        
    def create_topic (self , topic_name ):
        #new_topic = NewTopic(topic_name,num_partitions=3,replication_factor=3)
        new_topic = NewTopic(topic_name,num_partitions=3)
        result_dict = KafkaProducer.__admin_client.create_topics([new_topic])
        
        for topic , future in result_dict.items():
            try :
                future.result()
                print("Topic created "+topic )
            except Exception as e :
                print(e)
              
        
    def getInstance(self):
        try:
            if KafkaProducer.__producer_instance is None :
                configuration={
                    'bootstrap.servers':'localhost:9092'
                }
                KafkaProducer.__producer_instance=Producer(configuration)
                KafkaProducer.__admin_client=AdminClient(configuration)
                print("Kafka intialized ")
        except Exception as e :
            raise ("Kafka configuration issue "+e )
    
    def send_message(self,topic_name,data):
        
        json_data=json.dumps(data).encode("utf-8")
        try:
            KafkaProducer.__producer_instance.produce(topic=topic_name ,value=json_data)
            KafkaProducer.__producer_instance.flush()
        except Exception as e :
            print("Utter flop")
            print(e)
        
    

obj = KafkaProducer()
obj.getInstance()
#obj.create_topic("Testing1")
obj.topic_exists()

obj.send_message("Testing1",{"video_path":"C:/languages/manim/media/videos/957c9612-8195-406e-8b41-d5020619121b/480p15/BubbleSortPerfect.mp4","show_popup":True})