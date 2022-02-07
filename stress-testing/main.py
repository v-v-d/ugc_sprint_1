from kafka import KafkaProducer
from common_settings import CommonSettings


def send(producer: KafkaProducer, topic: str):
    data_count = 0
    example_user_id = 1
    timestamp = 1611039931
    move_id = 1
    while True:
        producer.send(
            topic=topic,
            value=bytes(f"{timestamp}", encoding='utf-8'),
            key=bytes(f"{example_user_id}+tt{move_id}", encoding='utf-8')
        )
        example_user_id += 1
        timestamp += 1
        move_id += 1
        data_count += 1
        if data_count == 10000000:
            break


if __name__ == "__main__":
    settings = CommonSettings()
    producer = KafkaProducer(bootstrap_servers=[f"{settings.KAFKA.HOST}:{settings.KAFKA.PORT}"])
    send(producer, settings.KAFKA.TOPIC)