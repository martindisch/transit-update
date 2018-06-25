import requests
import json

def get_key():
    with open("apikey", "r") as f:
        key = f.read().strip()
    return key

def request_updates(api_key):
    r = requests.get(
        "https://api.opentransportdata.swiss/gtfs-rt?format=JSON",
        headers={'Authorization': api_key})
    return json.loads(r.text)

if __name__ == "__main__":
    api_key = get_key()
    updates = request_updates(api_key)
    print(updates['header'])
