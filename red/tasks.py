import requests

def fetch_weather_data(station_id):

    print(f"Pobieranie danych dla stacji {station_id}...")

    response = requests.get(f"http://127.0.0.1:8000/weather/{station_id}")

    if response.status_code == 200:
        data = response.json()
        temp = float(data["temperature"])
        print(temp)

    else:
        pass

if __name__ == "__main__":
    fetch_weather_data("STACJA_TESTOWA")