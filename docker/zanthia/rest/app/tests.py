

from requests.auth import HTTPDigestAuth
import requests

url = 'http://localhost:9999/'
response = requests.get(url, auth=HTTPDigestAuth('bob', 'dole'))
print response.json()
