from confluent_kafka import Consumer, KafkaException, KafkaError
import sys

# Global flag
running = True

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'foo',
    'auto.offset.reset': 'latest'
}

consumer = Consumer(conf)
# class KafkaConsumer: 
#     __consumer_instance=None 

#     def __init__(self):
#         #Future use 
#         pass   

#     def getInstance (self ):
#         conf = {
#             "bootstrap.servers": "localhost:9092",
#             "group.id": "streamlit-consumer",
#             "auto.offset.reset": "earliest"
#         }
#         if KafkaConsumer.__consumer_instance is None :
#             KafkaConsumer.__consumer_instance=Consumer(conf)


#         return KafkaConsumer.__consumer_instance

def msg_process(msg):
    """Dummy processor — replace with your actual logic."""
    print(f"Received message: {msg.value().decode('utf-8')}")


def basic_consume_loop(consumer, topics):
    global running
    try:
        consumer.subscribe(topics)

        while running:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write(
                        f"%% {msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}\n"
                    )
                else:
                    raise KafkaException(msg.error())
            else:
                msg_process(msg)

    finally:
        print("Closing consumer...")
        consumer.close()


def shutdown():
    global running
    running = False


basic_consume_loop(consumer,["Testing1"])