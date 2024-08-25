# KEDA Scaling Project

## Project Overview

This project is designed to demonstrate how to scale applications on Kubernetes using [KEDA](https://keda.sh/). The application consists of two main scripts:

1. **Consumer**: A script that consumes data from AWS SQS or Kafka queues.
2. **Producer**: A script that produces random data into AWS SQS or Kafka queues.

Additionally, the project includes a CPU-intensive script to simulate load, which can be used to demonstrate scaling based on CPU usage.

## Purpose

The main purpose of this project is to showcase how KEDA can be used to scale workloads in Kubernetes based on various metrics, such as:

- **Queue Size**: Automatically scale up/down based on the number of messages in SQS or Kafka queues.
- **CPU Usage**: Scale up/down based on CPU load to handle intensive processing tasks.

## Project Structure
keda_scaling_demo/
├── consumer/
│   └── consumer.py                       # Script to consume data from SQS or Kafka
├── producer/
│   └── producer.py                       # Script to produce random data to SQS or Kafka
├── kubernetes/
│   ├── config-map.yaml                   # ConfigMap for non-sensitive environment variables
│   ├── consumer-deployment.yaml          # Kubernetes Deployment for the consumer
│   ├── producer-deployment.yaml          # Kubernetes Deployment for the producer
│   ├── keda-scaledobject-cpuload.yaml    # KEDA ScaledObject for CPU-based scaling
│   ├── keda-scaledobject-kafka.yaml      # KEDA ScaledObject for Kafka-based scaling
│   ├── keda-scaledobject-sqs.yaml        # KEDA ScaledObject for SQS-based scaling
│   ├── sqs-secrets.yaml                  # Kubernetes Secret for AWS credentials
│   └── sqs-trigger-authentication.yaml   # KEDA TriggerAuthentication for AWS SQS
├── Dockerfile                            # Dockerfile for containerizing the application
├── poetry.lock                           # Poetry lock file for reproducible builds
├── pyproject.toml                        # Poetry configuration file for managing dependencies
└── README.md                             # Project documentation




