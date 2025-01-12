from confluent_kafka import Consumer, KafkaError
import json


class WeatherDataConsumer:
    def __init__(self):
        conf = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'weather_group',
            'auto.offset.reset': 'latest'
        }
        self.consumer = Consumer(conf)
        self.consumer.subscribe(['weather_data'])
        print(f"Konsument zaincjowany...")

    def start_consuming(self):
        while True:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Błąd: {msg.error()}")
                    break

            data = json.loads(msg.value().decode("utf-8"))
            station_id = data['station_id']
            print(f"Otrzymano zadanie dla stacji: {station_id}")


if __name__ == "__main__":
    consumer = WeatherDataConsumer()
    consumer.start_consuming()