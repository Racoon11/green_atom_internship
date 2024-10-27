
import requests

url = 'http://127.0.0.1:8000/eco/storage/all'
url2 = 'http://127.0.0.1:8000/eco'



data = {
    "name": "OO-1"
    }


response = requests.get(url2)
csrftoken = response.json()['csrf']

headers = {'X-CSRFToken': csrftoken}
cookies = {'csrftoken': csrftoken}

print(response.json()['csrf'])
response = requests.get(url, params=data, cookies=cookies)
