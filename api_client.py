import requests

response = requests.get("http://127.0.0.1:8000/weather/STATION001")
#print(response.reason)
#print(response.status_code)
#print(response.ok)

#print(response.text)
if response.ok:
    data = response.json()
    print(data)
    print(data['humidity'])
    print(data['temperature'])
    if float(data['temperature']) > 25:
        print("Wysoka temperatura")
else:
    print("Problem z komunikacją")

#print(response.content)
#print(response.encoding)

#print(response.headers)
#print(response.url)
#print(response.elapsed)

# print(response.request.method)
# print(response.request.url)
# print(response.request.headers)
# print(response.request.body)


#response = requests.get("http://127.0.0.1:8000/weather/?city=Toruń&format=xml")
#print(response.text)
