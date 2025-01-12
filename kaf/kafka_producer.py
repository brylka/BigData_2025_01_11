from confluent_kafka import Producer
from datetime import datetime
import json
import time

class WeatherStationMonitor:
    def __init__(self):
        conf = {
            'bootstrap.servers': 'localhost:9092'
        }
        self.producer = Producer(conf)
        self.topic = 'weather_data'
        self.monitored_stations = set()

    def add_station(self, station_id):
        self.monitored_stations.add(station_id)
        print(f"Dodano stację: {station_id}")

    def delivery_report(self, err, msg):
        if err is not None:
            print(f"Błąd dostarczenia wiadomości: {err}")
        else:
            print(f"Wiadomość dostarczona do {msg.topic()}")

    def start_monitoring(self):
        while True:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

            for station_id in self.monitored_stations:
                message = {
                    'station_id': station_id,
                    'timestamp': timestamp,
                    'action': 'fetch_weather'
                }
                self.producer.produce(
                    self.topic,
                    json.dumps(message).encode("utf-8"),
                    callback=self.delivery_report
                )
                print(f"Wysłano zadanie dla stacji: {station_id}")

            self.producer.flush()
            time.sleep(60)


if __name__ == "__main__":
    monitor = WeatherStationMonitor()

    monitor.add_station("STACJA001")
    monitor.add_station("STACJA002")

    monitor.start_monitoring()