from kafka import KafkaConsumer
from datetime import datetime
import boto3
import json
import os
import time
import csv
import io

# Kafka Consumer 설정
kafka_topic = "[Kafka Topic Name]"
consumer = KafkaConsumer(
    kafka_topic,
    bootstrap_servers='[Host]:9092',
    security_protocol="SASL_PLAINTEXT",
    sasl_mechanism="PLAIN",
    sasl_plain_username="[Username]",
    sasl_plain_password="[Password]",
    auto_offset_reset='earliest',                               # Offset Reset
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))  # Json
)


# S3 설정
s3 = boto3.client(
    's3',
    aws_access_key_id='[AWS_ACCESS_KEY]',
    aws_secret_access_key='[AWS_SECRET_KEY]',
    region_name='[Region]'
)
bucket_name = '[Bucket Name]'

# Kafka Connection Check
def check_kafka_connection():
    try:
        partitions = consumer.partitions_for_topic(kafka_topic)
        if partitions:
            print(f"[Kafka] Connection Success - Partition : {partitions}")
            return True
        else:
            print("[Kafka] Connection Fail - Not Found Topic, Partition")
            return False
    except Exception as e:
        print(f"[Kafka Error] {e}")
        return False

# S3 Connection Check
def check_s3_connection():
    try:
        s3.list_objects_v2(Bucket=bucket_name, MaxKeys=1)
        print("[S3] Connection Success")
        return True
    except Exception as e:
        print(f"[S3 Connection Error] {e}")
        return False

# S3 Log Save (Batch)
def flush_logs_to_s3(buffer):
    if not buffer:
        return

    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    today = datetime.utcnow().strftime('%Y-%m-%d')
    key = f'logs/{today}/log_batch_{timestamp}.json'    # 모든 서버의 로그를 Athena를 통해 쿼리하기 위헤 최상위 logs Directory 지정

    # JSON 객체를 줄바꿈으로 연결 (JSON Lines 포맷)
    body = '\n'.join(json.dumps(log) for log in buffer)

    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=body,
            ContentType='application/json'
        )
        print(f"[S3] {len(buffer)}EA Save Success : {key}")
    except Exception as e:
        print(f"[S3 Error] Save Fail : {e}")

# Main
if __name__ == '__main__':
    if not check_kafka_connection():
        exit(1)
    if not check_s3_connection():
        exit(1)

    print("[INFO] Kafka Connection, S3 Connection Success - Log PipeLine Start")

    # Bulk, Batch
    buffer = []
    BATCH_SIZE = 100     # Log Count
    FLUSH_INTERVAL = 10  # 초 단위
    last_flush_time = time.time()

    for message in consumer:
        log_data = message.value
        buffer.append(log_data)

        # 배치 크기 또는 시간 조건 만족 시 flush
        if len(buffer) >= BATCH_SIZE or (time.time() - last_flush_time) >= FLUSH_INTERVAL:
            flush_logs_to_s3(buffer)
            buffer = []
            last_flush_time = time.time()