import os
import boto3
from kafka import KafkaProducer
import json
import random
import time

# Produce random data to SQS
def produce_to_sqs():
    sqs = boto3.client(
        'sqs',
        region_name=os.getenv('AWS_REGION'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    queue_url = os.getenv('SQS_QUEUE_URL')

    for _ in range(10):  # Produce 10 messages
        message = {"id": random.randint(1, 100), "value": random.random()}
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message)
        )
        print(f"Sent SQS message: {message}")
        time.sleep(1)

# Produce random data to Kafka
def produce_to_kafka():
    kafka_topic = os.getenv('KAFKA_TOPIC')
    kafka_servers = os.getenv('KAFKA_SERVERS').split(',')

    producer = KafkaProducer(
        bootstrap_servers=kafka_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    for _ in range(10):  # Produce 10 messages
        message = {"id": random.randint(1, 100), "value": random.random()}
        producer.send(kafka_topic, message)
        print(f"Sent Kafka message: {message}")
        time.sleep(1)

# Main function to run the producer
if __name__ == "__main__":
    produce_to_sqs()
    produce_to_kafka()
