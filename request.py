
import requests

url = 'http://127.0.0.1:8000/eco/create_org'
url2 = 'http://127.0.0.1:8000/eco'



data = {
    "name": "OO-1",
    "coord_x": 12.3,
    "coord_y": 5.4,
    }


response = requests.get(url2)
csrftoken = response.json()['csrf']

headers = {'X-CSRFToken': csrftoken}
cookies = {'csrftoken': csrftoken}

print(response.json()['csrf'])
response = requests.post(url, headers=headers, data=data, cookies=cookies)
