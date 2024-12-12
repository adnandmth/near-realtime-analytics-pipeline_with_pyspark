
# Introduction

This project provides connectors for Kafka Connect to read data from Kinesis streams.

# Source Connectors


## KinesisSourceConnector

The KinesisSourceConnector is a :term:`Source Connector`_ that is used to pull data from Amazon Kinesis in realtime and persist the data to a Kafka topic.

### Configuration

##### `aws.access.key.id`
*Importance:* High

*Type:* String


aws.access.key.id
##### `aws.secret.key.id`
*Importance:* High

*Type:* Password


aws.secret.key.id
##### `kafka.topic`
*Importance:* High

*Type:* String


The kafka topic to write the data to.
##### `kinesis.stream`
*Importance:* High

*Type:* String


The Kinesis stream to read from.
##### `kinesis.shard.id`
*Importance:* High

*Type:* String

*Default Value:* .*


The shard of the Kinesis stream to read from. This is a regex which can be used to read all of the shards in the stream.
##### `kinesis.base.url`
*Importance:* Low

*Type:* String

Kinesis endpoint URL which overrides the signing region. Can be used to connect to VPC endpoints and non standard endpoints. 
##### `kinesis.credentials.provider.class`
*Importance:* Low

*Type:* String

Credentials provider or provider chain to use for authentication to AWS. By default the connector uses 'DefaultAWSCredentialsProviderChain'
##### `kinesis.empty.records.backoff.ms`
*Importance:* Medium

*Type:* Long

*Default Value:* 5000

*Validator:* [500,...,2147483647]


The number of milliseconds to backoff when the stream is empty.
##### `kinesis.position`
*Importance:* Medium

*Type:* String

*Default Value:* TRIM_HORIZON

*Validator:* ValidEnum{enum=ShardIteratorType, allowed=[AT_SEQUENCE_NUMBER, AFTER_SEQUENCE_NUMBER, TRIM_HORIZON, LATEST, AT_TIMESTAMP]}


The position in the stream to reset to if no offsets are stored.
##### `kinesis.record.limit`
*Importance:* Medium

*Type:* Int

*Default Value:* 500

*Validator:* [1,...,10000]


The number of records to read in each poll of the Kinesis shard.
##### `kinesis.region`
*Importance:* Medium

*Type:* String

*Default Value:* US_EAST_1

*Validator:* ValidEnum{enum=Regions, allowed=[GovCloud, US_EAST_1, US_EAST_2, US_WEST_1, US_WEST_2, EU_WEST_1, EU_WEST_2, EU_CENTRAL_1, AP_SOUTH_1, AP_SOUTHEAST_1, AP_SOUTHEAST_2, AP_NORTHEAST_1, AP_NORTHEAST_2, SA_EAST_1, CN_NORTH_1, CA_CENTRAL_1]}


The AWS region for the Kinesis stream.
##### `kinesis.throughput.exceeded.backoff.ms`
*Importance:* Medium

*Type:* Long

*Default Value:* 10000

*Validator:* [500,...,2147483647]


The number of milliseconds to backoff when a throughput exceeded exception is thrown.

#### Examples

##### Standalone Example

This configuration is used typically along with [standalone mode](http://docs.confluent.io/current/connect/concepts.html#standalone-workers).

```properties
name = KinesisSourceConnector1
connector.class = com.github.jcustenborder.kafka.connect.kinesis.KinesisSourceConnector
tasks.max =1
aws.access.key.id = < Optional Configuration >
aws.secret.key.id = < Optional Configuration >
kafka.topic = < Required Configuration >
kinesis.stream = < Required Configuration >
```

##### Distributed Example

This configuration is used typically along with [distributed mode](http://docs.confluent.io/current/connect/concepts.html#distributed-workers).
Write the following json to `connector.json`, configure all of the required values, and use the command below to
post the configuration to one the distributed connect worker(s).

```json
{
  "config" : {
    "name" : "KinesisSourceConnector1",
    "connector.class" : "com.github.jcustenborder.kafka.connect.kinesis.KinesisSourceConnector",
    "tasks.max" : "1",
    "aws.access.key.id" : "< Optional Configuration >",
    "aws.secret.key.id" : "< Optional Configuration >",
    "kafka.topic" : "< Required Configuration >",
    "kinesis.stream" : "< Required Configuration >"
  }
}
```

If you choose not to pass your ***aws.access.key*** and ***aws.secret.key*** through the source configuration, please configure your credentials as per the instructions [here](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/credentials.html).
    
Use curl to post the configuration to one of the Kafka Connect Workers. Change `http://localhost:8083/` the the endpoint of
one of your Kafka Connect worker(s).

Create a new instance.
```bash
curl -s -X POST -H 'Content-Type: application/json' --data @connector.json http://localhost:8083/connectors
```

Update an existing instance.
```bash
curl -s -X PUT -H 'Content-Type: application/json' --data @connector.json http://localhost:8083/connectors/TestSinkConnector1/config
```

## Integration Tests

To run integration tests from the terminal, [deploy AWS credentials](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/credentials.html) in your environment, and run the following command: 

```
$ mvn clean integration-test

...
output truncated
...
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running io.confluent.connect.kinesis.IntegrationTest.KinesisSourceIntegrationTest
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 68.489 s - in io.confluent.connect.kinesis.IntegrationTest.KinesisSourceIntegrationTest
...
```

To **skip** running integration tests when running maven commands, enable the `skipIntegrationTests` flag. For example: 

```
mvn clean install -DskipIntegrationTests
```

# Documentation

## Location
Documentation on the connector is hosted on Confluent's
[docs site](https://docs.confluent.io/current/connect/kafka-connect-kinesis/index.html).

Source code is located in Confluent's
[docs repo](https://github.com/confluentinc/docs/tree/master/connect/kafka-connect-kinesis).

## Configs
Documentation on the configurations for each connector can be autotomatically generated via Maven.

To generate documentation for the source connector:
```bash
mvn -Pdocs exec:java@source-config-docs
```
