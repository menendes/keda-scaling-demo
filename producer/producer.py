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

    while True:
        message = {"id": random.randint(1, 100), "value": random.random()}
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message)
        )
        print(f"Sent SQS message: {message}")
        time.sleep(600)  # Wait for 10 minutes (600 seconds)

# Produce random data to Kafka
def produce_to_kafka():
    kafka_topic = os.getenv('KAFKA_TOPIC')
    kafka_servers = os.getenv('KAFKA_SERVERS').split(',')

    producer = KafkaProducer(
        bootstrap_servers=kafka_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        api_version=(0, 11, 5),
    )
    print(producer.config['api_version'])
    while True:
        message = {"id": random.randint(1, 100), "value": random.random()}
        producer.send(kafka_topic, message)
        print(f"Sent Kafka message: {message}")
        time.sleep(2)  # Wait for 10 minutes (600 seconds)

# Main function to run the producer based on RUN_TYPE
if __name__ == "__main__":
    run_type = os.getenv('RUN_TYPE')
    
    if run_type == 'sqs':
        print("Starting SQS producer")
        produce_to_sqs()
    elif run_type == 'kafka':
        print("Starting Kafka producer")
        produce_to_kafka()
    else:
        print("Invalid RUN_TYPE. Must be 'sqs' or 'kafka'.")
