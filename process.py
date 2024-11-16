import json

def is_killer_whale(data):
    return 'sex' in data

def was_captured(data):
    return 'place_of_capture' in data

def born_in_captivity(data):
    return 'place_of_birth' in data and 'latest_sighting' not in data

def is_captive_whale(data):
    return is_killer_whale(data) and (born_in_captivity(data) or was_captured(data))

filename = "killerwhales_fandom.json"

# Open and read the JSON file
with open(filename, 'r') as file:
    data = json.load(file)

for item in data:

    if is_captive_whale(item):

        name = item['title1'].split('-')[0].strip()
        sex = item['sex']

        mother = 'Unknown'
        if "mother" in item:
            mother = item['mother']

        father = 'Unknown'
        if "father" in item:
            father = item['father']

        url = item['url']

        born_or_caught = "Born"
        if (was_captured(item)):
            born_or_caught = 'Caught'

        status = 'Undefined'
        if 'status' in item:
            status = item['status']
        elif 'place_of_death' in item:
            status = 'Deceased'
        elif 'date_of_release' in item:
            status = "Released"


        print(f"{name:<28} {sex:<11} {born_or_caught:<8} {mother:<20} {father:<20} {status:<10} {url}")

