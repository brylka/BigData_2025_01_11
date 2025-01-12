from confluent_kafka import Consumer
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
