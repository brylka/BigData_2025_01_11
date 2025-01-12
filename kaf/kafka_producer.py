from confluent_kafka import Producer


class WeatherStationMonitor:
    def __init__(self):
        conf = {
            'bootstrap.servers': 'localhost:9092'
        }
        self.producer = Producer(conf)
        self.topic = 'weather_data'
        self.monitored_stations = set()