
# ✅ Step-by-Step Health Checks for Kafka & ZooKeeper Cluster

This guide covers how to perform health checks and connection verification for a multi-node Apache Kafka and ZooKeeper cluster using Docker Compose.

---

## 🔍 ZooKeeper Cluster Health Check

### 1. **Check ZooKeeper Containers Are Running**

```bash
docker ps | grep zookeeper
```

You should see all three ZooKeeper containers: `zookeeper1`, `zookeeper2`, `zookeeper3`.

### 2. **Check ZooKeeper Status Individually**

Execute into each ZooKeeper container and run the command:

```bash
docker exec -it zookeeper1 bash
echo srvr | nc zookeeper1 2181
```

Expected output: 
Zookeeper version: 3.9.3-c26634f34490bb0ea7a09cc51e05ede3b4e320ee, built on 2024-10-17 23:21 UTC
Latency min/avg/max: 0/0.0/0
Received: 6
Sent: 5
Connections: 1
Outstanding: 0
Zxid: 0x0
Mode: follower
Node count: 5

Repeat for `zookeeper2` and `zookeeper3`.

---

## 🔍 Kafka Brokers Health Check

### 1. **Check Kafka Containers Are Running**

```bash
docker ps | grep broker
```

You should see all brokers, e.g., `broker1`, `broker2`, `broker3`.

### 2. **Verify Environment Variables Set Correctly**

Ensure that each broker has these variables set:

```env
KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper1:2181,zookeeper2:2181,zookeeper3:2181
KAFKA_CFG_LISTENERS=PLAINTEXT://:9092
KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://brokerX:9092
KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT
KAFKA_CFG_INTER_BROKER_LISTENER_NAME=PLAINTEXT
```

### 3. **Check Kafka Logs for Errors**

```bash
docker logs broker1 | less
```

Look for errors or misconfiguration messages.

### 4. **Connect with Kafka CLI**

Use Kafka's CLI tools (inside a container or host) to list topics:

```bash
docker exec -it broker1 kafka-topics.sh \
  --bootstrap-server broker1:9092 \
  --list
```

If successful, the broker is healthy and connected to ZooKeeper.

### 5. **Create a Test Topic**

```bash
docker exec -it broker1 kafka-topics.sh \
  --create \
  --topic test-topic \
  --bootstrap-server broker1:9092 \
  --replication-factor 3 \
  --partitions 1
```

### 6. **Produce & Consume Test Messages**

```bash
# Producer
docker exec -it broker1 kafka-console-producer.sh \
  --broker-list broker1:9092 \
  --topic test-topic
```

Type some messages and press enter.

```bash
# Consumer
docker exec -it broker2 kafka-console-consumer.sh \
  --bootstrap-server broker2:9092 \
  --topic test-topic \
  --from-beginning
```

---

## ✅ Summary

| Component | Check                      | Expected Output       |
| --------- | -------------------------- | --------------------- |
| ZooKeeper | `stat` mode                | `leader` / `follower` |
| Kafka     | Broker logs                | No errors             |
| Kafka     | Topic list command         | List of topics        |
| Kafka     | Produce & consume messages | Echoed messages       |

---

## 📚 References

* Bitnami Kafka Docs: [https://github.com/bitnami/containers/tree/main/bitnami/kafka](https://github.com/bitnami/containers/tree/main/bitnami/kafka)
* Bitnami ZooKeeper Docs: [https://github.com/bitnami/containers/tree/main/bitnami/zookeeper](https://github.com/bitnami/containers/tree/main/bitnami/zookeeper)
* Apache Kafka Official Docs: [https://kafka.apache.org/documentation/](https://kafka.apache.org/documentation/)
