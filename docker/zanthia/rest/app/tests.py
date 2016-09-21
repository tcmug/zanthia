

from requests.auth import HTTPBasicAuth
import requests

url = 'http://rest:8888/'
response = requests.get(url, auth=HTTPBasicAuth('zanthia', 'password'))
print response.json()
