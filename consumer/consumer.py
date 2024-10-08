import os
import boto3
from kafka import KafkaConsumer
import logging
import time
import multiprocessing

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Part 1: Consume data from AWS SQS
def consume_from_sqs():
    sqs = boto3.client(
        'sqs',
        region_name=os.getenv('AWS_REGION'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    queue_url = os.getenv('SQS_QUEUE_URL')
    
    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=2,
            WaitTimeSeconds=5
        )
        
        messages = response.get('Messages', [])
        if not messages:
            continue
        
        for message in messages:
            logging.info(f"Received SQS message: {message['Body']}")
            sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])

# Part 2: Consume data from Kafka
def consume_from_kafka():
    kafka_topic = os.getenv('KAFKA_TOPIC')
    kafka_servers = os.getenv('KAFKA_SERVERS').split(',')

    try:
        consumer = KafkaConsumer(
            kafka_topic,
            bootstrap_servers=kafka_servers,
            auto_offset_reset='earliest',  # Uncomment if you want to start from the earliest offset
            enable_auto_commit=True,  # Uncomment if you want to enable auto commit
            group_id=os.getenv('KAFKA_GROUP_ID'),  # Uncomment if you need a specific group ID
            api_version=(0, 11, 5),  # Ensure this matches your Kafka cluster version
        )

        for message in consumer:
            logging.info("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                 message.offset, message.key,
                                                 message.value))

    except Exception as e:
        logging.error(f"Failed to consume messages from Kafka: {str(e)}")

# Part 3: CPU-intensive function for load testing
def cpu_load_test():
    def load_function():
        while True:
            _ = [x**2 for x in range(10000)]

    # Start multiple processes for a higher CPU load
    processes = []
    for _ in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=load_function)
        p.start()
        processes.append(p)
    
    # Let the processes run for a specified time
    time_to_run = int(os.getenv('CPU_LOAD_DURATION', '300'))
    time.sleep(time_to_run)
    
    # Terminate the processes after the specified time
    for p in processes:
        p.terminate()

# Main function to run based on environment variable
if __name__ == "__main__":
    run_type = os.getenv('RUN_TYPE')
    
    if run_type == 'sqs':
        logging.info("Running SQS consumer")
        consume_from_sqs()
    elif run_type == 'kafka':
        logging.info("Running Kafka consumer")
        consume_from_kafka()
    elif run_type == 'cpu':
        logging.info("Running CPU load test")
        cpu_load_test()
    else:
        logging.error("Invalid RUN_TYPE provided. Must be 'sqs', 'kafka', or 'cpu'.")
