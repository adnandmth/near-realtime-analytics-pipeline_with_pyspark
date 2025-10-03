# 🚀 Data Infrastructure Health Checks

This repository contains guides and utilities to perform **health checks** on a containerized **data infrastructure stack** built with **Docker Compose**.

---

## 🏗️ Architecture Overview

The setup consists of:

- **Apache ZooKeeper** → Coordinates distributed systems, ensures consistency across Kafka brokers.  
- **Apache Kafka** → Message broker for real-time data streaming, integrated with ZooKeeper for cluster management.  
- **Apache Spark** → Distributed processing engine for batch & streaming analytics.  
- **Docker Compose** → Orchestrates multi-container deployment for local development & testing.  

### 🔗 High-Level Workflow

1. **ZooKeeper** manages broker metadata and leader election.  
2. **Kafka Brokers** handle messaging (produce/consume).  
3. **Spark Cluster** (master + workers) processes streaming or batch jobs, consuming data from Kafka if needed.  
4. All services run as Docker containers, exposing UIs and CLI tools for monitoring and debugging.  

---

## 📖 Health Check Guides

Each component has its own dedicated step-by-step guide:  

- [Kafka & ZooKeeper Health Checks](./README-kafka.md)  
- [Spark Cluster Health Checks](./README-spark.md)  

---

## ✅ Use Cases

- Verify cluster setup after deployment.  
- Debug connection or configuration issues.  
- Confirm messaging pipeline (Kafka) and computation pipeline (Spark) are functional.  

---

## 📚 References

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)  
- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)  