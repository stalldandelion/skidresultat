import json


def get_locations(jsondb):
    locations = list()

    with open(jsondb) as json_file:
        data = json.load(json_file)

    for i in data['competition']:
        locations.append(i)

    return locations


def get_highest_location_id():

    return max(
        [int(x.get('id')) for x in get_locations("/Users/micke/PycharmProjects/skidresultat/static/skid_db.json")]
    )
