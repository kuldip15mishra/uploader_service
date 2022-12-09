
import certifi
from uuid import uuid4
from confluent_kafka import Producer, KafkaException




def addCommentsToKafka(comment):

    print("Starting Kafka Producer")
    conf = {
        'bootstrap.servers': 'pkc-lgk0v.us-west1.gcp.confluent.cloud:9092',
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': 'DQIGRAOSHTUPI6VX',
        'sasl.password': 'yfuUrxiLlqZGebQLfJQ9LNqmgPS7NsFXuElBANLeFDOgQDjyuII54ZGgUIE7l6Pp',
        'ssl.ca.location': certifi.where()
    }

    print("connecting to Kafka topic...")
    producer1 = Producer(conf)
    kafka_topic_name = "comments_youber_raw"
# Trigger any available delivery report callbacks from previous produce() calls
    producer1.poll(0)

    try:
        # Asynchronously produce a message, the delivery report callback
        # will be triggered from poll() above, or flush() below, when the message has
        # been successfully delivered or failed permanently.
        producer1.produce(topic=kafka_topic_name, key=str(
            uuid4()), value=comment, on_delivery=delivery_report)
        # producer1.produce(topic=kafka_topic_name, key=str(uuid4()), value=jsonv2, on_delivery=delivery_report)
        # producer1.produce(topic=kafka_topic_name, key=str(uuid4()), value=jsonv3, on_delivery=delivery_report)

        # Wait for any outstanding messages to be delivered and delivery report
        # callbacks to be triggered.
        producer1.flush()

    except Exception as ex:
        print("Exception happened :", ex)

    print("\n Stopping Kafka Producer")


def delivery_report(errmsg, msg):

    if errmsg is not None:
        print("Delivery failed for Message: {} : {}".format(msg.key(), errmsg))
        return
    print('Message: {} successfully produced to Topic: {} Partition: [{}] at offset {}'.format(
        msg.key(), msg.topic(), msg.partition(), msg.offset()))



