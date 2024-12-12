# Gundala #

## Introduction

Gundala is a popular Indonesian superhero created by Harya Suraminata, also known as Hasmi. Gundala made his first appearance in 1969 in a comic book titled â€œGundala Putra Petirâ€ (Gundala, the Son of Thunder). The character is often compared to superheroes like The Flash and Thor due to his abilities and origin story.

Gundala has been a cultural icon in Indonesia, and his popularity was revived with the release of the 2019 film â€œGundala,â€ directed by Joko Anwar. The film is part of the BumiLangit Cinematic Universe, Indonesiaâ€™s first major superhero cinematic universe, and it has sparked renewed interest in the character and Indonesian superhero stories.

Gundala, the Indonesian superhero, has several abilities that are primarily based on his connection to lightning and thunder. One of those is -- Super Speed: After being struck by lightning, Gundala gains super speed, allowing him to move at incredible velocities, much like The Flash --, this ability is what made us decided to name this repository as Gundala.

## About Gundala

Gundala is a project aimed at providing a robust and scalable real-time data streaming pipeline using Kafka technology. The objective of this project is to facilitate efficient and reliable data streaming, enabling real-time data processing and analysis for various applications. With Gundala, you can seamlessly integrate and process data in real-time, ensuring that your systems stay responsive and up-to-date with the latest information.

## Dockerized Kafka, Spark, and Related Services

This setup uses Docker Compose to deploy a real-time data processing environment with Kafka, Zookeeper, Kafka Connect, Schema Registry, Control Center, and Spark.

### Pre-requisites

	•	Docker and Docker Compose should be installed on your machine.
	•	Make sure your AWS credentials (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY) are properly set in your environment.

### How to Run

1. Clone the Repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

2. Start the Services:
```bash
docker-compose up -d
or 
docker-compose up --build -d
```

3. Check the Logs:
Monitor logs to ensure services are starting correctly:
```bash
docker-compose logs -f
```

### Validating the Connections

1. Zookeeper Connection
Run the following command to check if Zookeeper is running correctly:
```bash
echo "ruok" | nc localhost 2181
```
Expected Output: imok.

2. Kafka Broker Connection
Use kafka-topics to list the available topics:
```bash
docker exec -it broker kafka-topics --list --bootstrap-server broker:9092
```

3. Schema Registry Connection
Visit the Schema Registry URL:
- http://localhost:8081/subjects
This should return a list of registered schemas or an empty list.

4. Kafka Connect Connection
Test the REST API for Kafka Connect by listing all connectors:
```bash
curl -X GET http://localhost:8083/connectors
```
This should return []%

Configure the Kinesis Source Connector:
```bash
curl -X POST -H "Content-Type: application/json" \
-d @kinesis-source-connector.json \
http://localhost:8083/connectors
```

5. Kafka Control Center
Open your browser and navigate to:
http://localhost:9021

You can monitor Kafka brokers, topics, and connectors through the UI.

6. Spark Master and Worker Connection
Visit the Spark Master Web UI:
- http://localhost:8080
You should see the Spark Worker registered under the “Workers” tab.

7. Testing Kafka Producer
To test the Kafka producer, ensure it is properly configured to produce messages to a topic.
Check the messages on the topic using:
```bash
docker exec -it broker kafka-console-consumer --bootstrap-server broker:9092 --topic <your-topic-name> --from-beginning
kafka-topics --create --topic spark-streaming-data-bi --bootstrap-server broker:9092 --replication-factor 1
```