import os
import boto3
from kafka import KafkaProducer
import json
import random
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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
        logging.info(f"Sent SQS message: {message}") # Wait for 10 minutes (600 seconds)


# Produce random data to Kafka
def produce_to_kafka():
    kafka_topic = os.getenv('KAFKA_TOPIC')
    kafka_servers = os.getenv('KAFKA_SERVERS').split(',')

    producer = KafkaProducer(
        bootstrap_servers=kafka_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        api_version=(0, 11, 5),
    )
    logging.info(f"Kafka producer API version: {producer.config['api_version']}")

    while True:
        message = {"id": random.randint(1, 100), "value": random.random()}
        producer.send(kafka_topic, message)
        logging.info(f"Sent Kafka message: {message}")
        time.sleep(2)  # Wait for 10 minutes (600 seconds)


# Main function to run the producer based on RUN_TYPE
if __name__ == "__main__":
    run_type = os.getenv('RUN_TYPE')

    if run_type == 'sqs':
        logging.info("Starting SQS producer")
        produce_to_sqs()
    elif run_type == 'kafka':
        logging.info("Starting Kafka producer")
        produce_to_kafka()
    else:
        logging.error("Invalid RUN_TYPE. Must be 'sqs' or 'kafka'.")
