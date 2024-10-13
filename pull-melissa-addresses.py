import sys
import requests
import csv
import re
import json

master_file = 'TransylvaniaCounty.json'
function = sys.argv[1]

def append_master_address(records, filename):
    with open(filename, 'r') as source_file:
        addresses = json.load(source_file)
    for record in records:
        addresses[record['AddressKey']] = record
    with open(filename, 'w') as output_file:
        json.dump(addresses, output_file)

def request_addresses(melissa_key, territory, latitude, longitude, radius, records, filename):
    url = 'https://reversegeo.melissadata.net/v3/web/ReverseGeoCode/doLookup'
    params = {
        't': territory,
        'id': melissa_key,
        'lat': latitude,
        'long': longitude,
        'dist': radius,
        'opt': 'IncludeApartments:on;IncludeUndeliverable:on',
        'format': 'json',
        'recs': records
    }
    response = requests.get(url, params=params)

    if response.ok:
        with open(territory + '.json', 'w') as json_file:
            json.dump(response.json(), json_file)

        append_master_address(response.json()['Records'], filename)
    else:
        print('Response code: ' + str(response.status_code) + '\nResponse detail: ' + response.text)

def extract_street_addresses(street_name, master_source, destination_file, flag):
    with open(master_source, 'r') as source_file:
        addresses = json.load(source_file)

    street_addresses = []
    if street_name == 'ALL':
        pattern = '.*'
    else:
        pattern = re.compile(street_name)
    for address in addresses.values():
        if re.search(pattern, address['AddressLine1']):
            street_addresses.append(address)

    with open(destination_file + '.csv', flag, newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        if flag == 'w':
            csv_writer.writerow(['Number', 'Street', 'City', 'State', 'PostalCode', 'Latitude', 'Longitude', 'Type', 'ApartmentNumber'])
        for address in street_addresses:
            match_number = re.search(r'\d+', address['AddressLine1'])
            number = match_number.group(0)
            match_street = re.search(r'\d+\s(.*)', address['AddressLine1'])
            street = match_street.group(1)
            city = address['City']
            state = address['State']
            postal_code = address['PostalCode']
            latitude = address['Latitude']
            longitude = address['Longitude']
            if address['SuiteCount'] != '0' or address['SuiteName']:
                address_type = 'Apartment'
                apartment = address['SuiteName']
            else:
                address_type = 'House'
                apartment = None
            csv_writer.writerow([number, street, city, state, postal_code, latitude, longitude, address_type, apartment])

match sys.argv[1]:
    case 'pull':
        request_addresses(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], master_file)
    case 'export':
        extract_street_addresses(sys.argv[2], master_file, sys.argv[3], 'w')
    case 'append':
        extract_street_addresses(sys.argv[2], master_file, sys.argv[3], 'a')
    case default:
        print('Unknown argument: ' + sys.argv[1])
