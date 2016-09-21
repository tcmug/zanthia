
from lettuce import *
from requests.auth import HTTPDigestAuth
import requests
import json

def rest_get(path):
    session = requests.Session()
    url = 'http://localhost:9999%s' % (path)
    return session.get(url, auth=HTTPDigestAuth('zanthia', 'password'))


@step('I query (.*)')
def rest_query(step, path):
    world.response = rest_get(path)
    world.response_json = json.loads(world.response.content)
    assert world.response.status_code == 200, "Request failed"


@step('I receive (.*)')
def rest_query(step, stuff):
    assert stuff in world.response_json, "Response should have: %s" % (stuff)


@step('I have the following in results:')
def fllowing(step):
    entries = step.hashes
    for entry in entries:
        found = False
        for obj in world.response_json['result']:
            if obj['name'] == entry['name']:
                found = True
        assert found == True, "No match: %s" % (entry['name'])
