
# TWAP Order Strategy System

This project implements a TWAP (Time-Weighted Average Price) order strategy system targeting the Bybit exchange.

## Overview

The system accepts:
- **Trading symbol**
- **Side (buy/sell)**
- **Total size to execute**
- **Total runtime**
- **Frequency**

It periodically fetches the current market price and dispatches orders until the total size is reached, following the TWAP logic. Also, it can stop execution if a defined **price limit** is hit.

## Architecture

The system is built using a **Microservices Architecture** combined with an **Event-Driven** approach. Each core function—scheduling, ordering, logging, and job storage—is implemented as an independent service. These services communicate asynchronously via **RabbitMQ**, ensuring loose coupling and scalability. All services are containerized and deployed to a local Kubernetes cluster for orchestration and isolation.

Internally, each service follows the **Onion Architecture Pattern**, which cleanly separates business logic (domain) from infrastructure concerns. This pattern ensures that the core logic remains testable and independent of external systems like databases or APIs. The architecture allows for easy extensibility, such as integrating new exchanges or evolving order strategies, without disrupting the existing system.

### Job Storage Service
Stores scheduled jobs and orders via **APScheduler**.

### Log Storage Service
Persists logs for debugging and performance analysis into MongoDB.

### Queue Service
A RabbitMQ message queue that connects the **Scheduling Service** and **Ordering Service**.

### Scheduling Service
Schedules jobs and sends order events into the queue. Works with Job Storage to track state.

### Ordering Service
Consumes messages from the queue, fetches the current price from Bybit's testnet, and dispatches TWAP orders.

## Tech Stack

- **Python**
- **Docker + Kubernetes (local)**
- **RabbitMQ** for inter-service messaging
- **MongoDB** for log storage
- **Bybit Testnet API** for market data and order placement
- **APScheduler** for job scheduling

## Setup & Usage

### Requirements

- Docker Desktop with **Kubernetes enabled**
- `make` installed on your system

### Starting the system
In root of the project execute this: `make start`

This command:

-   Builds all Docker images
    
-   Deploys services into Kubernetes
    
-   Initializes required infrastructure (MongoDB, RabbitMQ, PostgreSQL)

### Stopping the system
In root of the project execute this: `make stop`

It cleans up all running services and Kubernetes resources.