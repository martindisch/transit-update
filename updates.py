import requests
import json
import csv

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


def get_trips():
    with open("gtfs/trips.txt", "r") as f:
        csv_reader = csv.reader(f)
        trips = {
            row[2]: {
                'route_id': row[0],
                'trip_headsign': row[3],
                'trip_short_name': row[4]
            } for row in csv_reader
        }
    return trips


def get_routes():
    with open("gtfs/routes.txt", "r") as f:
        csv_reader = csv.reader(f)
        routes = {
            row[0]: {
                'agency_id': row[1],
                'route_desc': row[4]
            } for row in csv_reader
        }
    return routes


def get_agencies():
    with open("gtfs/agency.txt", "r") as f:
        csv_reader = csv.reader(f)
        agencies = {row[0]: row[1] for row in csv_reader}
    return agencies


def show_updates(api_key):
    print("Requesting updates from API...")
    gtfs_rt_updates = request_gtfs_rt_updates(api_key)
    print("Converting updates...")
    trip_updates = get_trip_updates(gtfs_rt_updates)
    print("Loading GTFS static data...")
    trips = get_trips()
    routes = get_routes()
    agencies = get_agencies()
    print("Done.")

    for trip_id, update in trip_updates.items():
        print()
        if trip_id in trips:
            trip_update = update['trip']
            route_id = trip_update['route_id']
            start_time = trip_update['start_time']
            status = trip_update['schedule_relationship']

            trip = trips[trip_id]
            trip_headsign = trip['trip_headsign']
            trip_short_name = trip['trip_short_name']

            route = routes[route_id]
            agency_id = route['agency_id']
            route_desc = route['route_desc']

            agency = agencies[agency_id]

            print("{} with status {}".format(trip_id, status))
            print("{}: {}".format(trip_short_name, trip_headsign))
            print("{}, start time {}".format(route_desc, start_time))
            print("Operated by {}".format(agency))
        else:
            print("{} with status {}".format(trip_id, status))
            print("Not a standard trip, no further information found.")


if __name__ == "__main__":
    api_key = get_key()
    show_updates(api_key)
