import requests
from redis import Redis

def fetch_weather_data(station_id):

    redis_conn = Redis()

    try:
        print(f"Pobieranie danych dla stacji {station_id}...")

        response = requests.get(f"http://127.0.0.1:8000/weather/{station_id}")

        if response.status_code == 200:
            data = response.json()
            temp = float(data["temperature"])

            if temp > 30:
                print(f"Wysoka temperatura {temp}'C na stacji {station_id}")

            redis_conn.lpush(f"temps:{station_id}", temp)
            redis_conn.ltrim(f"temps:{station_id}", 0, 99)

            return data

        else:
            print(f"Błąd API, kod odpowiedzi: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        print(f"Nie można połączyć się z API dla stacji {station_id}")
        return None
    except Exception as e:
        print(f"Błąd dla stacji {station_id} {e}")
        return None

if __name__ == "__main__":
    print(fetch_weather_data("STACJA_TESTOWA"))