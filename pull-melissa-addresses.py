import sys
import requests
import csv
import re
import json

url = 'https://reversegeo.melissadata.net/v3/web/ReverseGeoCode/doLookup'
melissa_key = 'Q5S2W3lAlvClBjtiVV9jxl**nSAcwXpxhQ0PC2lXxuDAZ-**'
territory = sys.argv[1]
latitude = sys.argv[2]
longitude = sys.argv[3]
radius = sys.argv[4]
params = {
    't': territory,
    'id': melissa_key,
    'lat': latitude,
    'long': longitude,
    'dist': radius,
    'opt': 'IncludeApartments:on;IncludeUndeliverable:on',
    'format': 'json',
    'recs': '20'
}
response = requests.get(url, params=params)

with open(territory + '.json', 'w') as json_file:
    json.dump(response.json(), json_file)

with open(territory + '.json', 'r') as json_file:
    response = json.load(json_file)

with open(territory + '.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(['Number', 'Street', 'City', 'State', 'PostalCode', 'Latitude', 'Longitude'])
    for address in response.json()['Records']:
        match_number = re.search(r'\d+', address['AddressLine1'])
        number = match_number.group(0)
        match_street = re.search(r'\d+\s(.*)', address['AddressLine1'])
        street = match_street.group(1)
        city = address['City']
        state = address['State']
        postal_code = address['PostalCode']
        latitude = address['Latitude']
        longitude = address['Longitude']
        csv_writer.writerow([number, street, city, state, postal_code, latitude, longitude])
