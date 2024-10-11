import sys
import requests
import csv
import re

class Address:
    def __init__(self):
        self.AddressLine1 = ''
        self.SuiteName = ''
        self.SuiteCount = 0
        self.City = ''
        self.State = ''
        self.PostalCode = ''
        self.AddressKey = None
        self.Latitude = None
        self.Longitude = None
        self.Distance = 0
        self.MelissaAddressKey = None
        self.MelissaAddressKeyBase = None

class ReverseGeoCodeResponse:
    def __init__(self):
        self.Version = None
        self.TransmissionReference = None
        self.TransmissionResults = None
        self.Results = None
        self.TotalRecords = 0
        self.Records = []

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
    'format': 'json'
}
response = requests.get(url, params=params)

with open(territory + '.json', 'w') as json_file:
    json_file.write(response.json())

with open(territory + '.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimeter=',')
    csv_writer.writerow(['Number', 'Street', 'City', 'State', 'PostalCode', 'Latitude', 'Longitude'])
    for address in response.json()['Records']:
        match_number = re.search('\d+', address['AddressLine1'])
        number = match_number.group(0)
        match_street = re.search('\d+\s(.*)', address['AddressLine1'])
        street = match_street.group(1)
        city = address['City']
        state = address['State']
        postal_code = address['PostalCode']
        latitude = address['Latitude']
        longitude = address['Longitude']
        csv_writer.writerow([number, street, city, state, postal_code, latitude, longitude])
