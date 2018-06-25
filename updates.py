import requests
import json

def get_key():
    with open("apikey", "r") as f:
        key = f.read().strip()
    return key


def request_gtfs_rt_updates(api_key):
    r = requests.get(
        "https://api.opentransportdata.swiss/gtfs-rt?format=JSON",
        headers={'Authorization': api_key})
    # TODO: exception for unauthorized access and unknown errors
    return json.loads(r.text)


def get_trip_updates(gtfs_updates):
    entity = gtfs_updates['entity']
    trip_updates = {item['id']: item['trip_update'] for item in entity}
    return trip_updates


if __name__ == "__main__":
    api_key = get_key()
    gtfs_rt_updates = request_gtfs_rt_updates(api_key)
    trip_updates = get_trip_updates(gtfs_rt_updates)
