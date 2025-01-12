from confluent_kafka import Consumer, KafkaError
import json
from red.tasks import fetch_weather_data


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
        with open('weather_data.csv', 'a') as f:
            if f.tell() == 0:
                f.write("timestamp,station_id,temperature\n")
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
                try:
                    data = json.loads(msg.value().decode("utf-8"))
                    station_id = data['station_id']
                    print(f"Otrzymano zadanie dla stacji: {station_id}")

                    weather_data = fetch_weather_data(station_id, False)
                    if weather_data:
                        timestamp = weather_data['timestamp']
                        temp = weather_data['temperature']
                        f.write(f"{timestamp},{station_id},{temp}\n")
                        f.flush()
                        print(f"Pobrano dane: {weather_data}")
                except Exception as e:
                    print(f"Błąd przetwarzania wiadomości: {e}")


if __name__ == "__main__":
    consumer = WeatherDataConsumer()
    consumer.start_consuming()