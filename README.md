# MQTT Cluster Demo App

## Overview

This repository contains a demo application that showcases an MQTT-based messaging system designed for high availability, fault tolerance, and network stability. The setup consists of multiple MQTT brokers and publishers running on different IP addresses, all synchronized to maintain consistent state and data integrity even when some nodes drop offline. This is particularly useful in scenarios where network infrastructure is inconsistent, and continuous data availability is critical.

## Key Components

The system is built on the MQTT protocol, a lightweight messaging protocol ideal for IoT and machine-to-machine (M2M) communication. The demo includes the following core components:

- **MQTT Brokers**: Act as the central hub for message routing and state management. Multiple brokers are configured in a clustered setup to provide redundancy and load balancing.
- **Publishers**: Devices or applications that send messages to the MQTT brokers. In this demo, multiple redundant publishers are used to maintain state consistency.
- **Subscribers**: Devices or applications that receive messages from the MQTT brokers. In this setup, subscribers are designed to connect to any available broker in the cluster, ensuring uninterrupted service.
- **MQTT Bridges**: Connect MQTT brokers to each other, allowing messages to be shared across the cluster and maintaining synchronization between brokers.

## Architecture

The architecture for this demo is designed to simulate a real-world IoT environment where network reliability cannot be guaranteed. It includes:

1. **Seven Synchronized Brokers and Publishers**: Each broker-publisher pair runs on a different IP address (e.g., `10.0.0.55`, `10.0.0.56`, etc.) and is containerized for easy deployment. All brokers maintain state synchronization, ensuring that if one broker goes offline, the others continue to provide consistent data.
   
2. **Client Application**: A containerized client app running on a separate IP address (e.g., `10.0.0.140`) that subscribes to the cluster and receives messages from the brokers. The client is optimized to use any of the seven broker-publishers, providing seamless failover and load balancing without excessive error handling.

3. **Load Balancing and Failover**: The MQTT cluster acts like a load balancer, automatically directing clients to available brokers. This setup ensures clients are unaware of network instability or broker failures behind the scenes.

4. **Data Integrity and Synchronization**: With MQTT's Quality of Service (QoS) settings, publishers ensure reliable message delivery to subscribers. The system supports retained messages, Last Will and Testament (LWT) for client disconnect detection, and bridging for cross-broker communication.

## Use Cases

This demo is designed to illustrate how an MQTT cluster can be used in scenarios where:
- Network stability is unpredictable, and redundancy is essential for reliable communication.
- Real-time messaging is crucial, such as in IoT, smart city applications, remote monitoring, and industrial automation.
- Scalability and flexibility are required for growing data requirements and infrastructure.

## Features Demonstrated

- **Clustered MQTT Broker Setup**: Demonstrates high availability and fault tolerance using multiple synchronized brokers.
- **QoS Levels**: Shows the different Quality of Service levels (`0`, `1`, `2`) and their impact on message delivery and data integrity.
- **Retained Messages and LWT**: Illustrates the use of retained messages for initializing new clients and the Last Will and Testament feature for handling unexpected client disconnections.
- **Network Resilience and Failover**: Simulates network instability and shows how the MQTT system maintains client connectivity and data flow.

## Getting Started

The repository provides a Dockerized setup for easy deployment of the MQTT brokers, publishers, and client applications. Each component can be configured with a startup variable for the desired IP address, allowing for easy scaling and customization of the cluster.

## Next Steps

1. **Run the Demo Application**: Set up the Docker containers and run the demo to see the MQTT cluster in action.
2. **Test Different Scenarios**: Simulate network instability, broker failovers, and different QoS levels to understand the robustness of the setup.
3. **Customize and Extend**: Modify the setup to add more brokers, integrate with other systems, or use different security mechanisms.
4. **Review the Documentation**: Refer to the detailed documentation provided for setup guides, code samples, and configuration details.

## Contributing

Contributions are welcome! Please feel free to submit issues, pull requests, or suggestions for improvements.

