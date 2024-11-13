# Pull-Melissa-Addresses

Pulls addresses from [Melissa.com](melissa.com) and exports address data into CSV files that can be imported into NW Scheduler.

## Files
- pull-melissa-addresses.py - Python script for pulling address data from [Melissa.com](https://melissa.com) and exporting address data to CSV files.
- TransylvaniaCounty.json - Data file containing all addresses pulled for Transylvania County NC.

## Usage

### Pull Addresses
Pull addresses by executing the pull-melissa-addresses.py script with the following arguments:

  a. 'pull' - This string indicates that the script should pull address data from [Melissa.com](https://melissa.com).

  b. Melissa License Key - License Key for [Melissa.com](https://melissa.com) account. To get a License Key, create a [Melissa.com](https://melissa.com) account. Once the account is created, log in to [Melissa.com](https://melissa.com), select "My Account", and use the value in the box titled "License Key Using Credits".

  c. Transaction ID - this can be any value.

  d. Latitude - Numerical latitude of the point at the center of the addresses that will be pulled.

  e. Longitude - Numerical longitude of the point at the center of the addresses that will be pulled.

  f. Radius - Distance in miles from the central point that addresses will be pulled for.

  g. Records - Number of addresses to pull (maximum of 100).

  h. Address File - Name of file that addresses will be stored in. If the file already exists, the new addresses will be appended. Duplicate addresses will be ignored so that the file only contains unique addresses.

#### Example
```(venv) python3 pull-melissa-addresses.py pull yafuh342rlc3van BrevardAddresses 35.223781 -82.729557 1 100 TransylvaniaCO```

The above command pulls up to 100 addresses within 1 mile of the point at latitude 35.223781 and longitude -82.729557. It saves the results to a file called TransylvaniaCO.json.

### Create New CSV Export
Export addresses to a new CSV file by executing the pull-melissa-addresses.py script with the following arguments:

  a. 'export' - This string indicates that the script should export data from the address file to a new CSV file.

  b. Street Name - The name of a street to export addresses for. Enter 'ALL' to get all addresses in the Address File.

  c. Address File - Name of file that addresses will be exported from.

  d. Destination File - Name of the file that will be created containing address data in CSV format.

#### Example
```(venv) python3 pull-melissa-addresses.py export "Main St" TransylvaniaCO ExportedAddresses```

The above command exports the addresses on Main St from the file called TransylvaniaCO.json to a file called ExportedAddresses.csv.

### Append to existing CSV Export
Append addresses to an existing CSV file by executing the pull-melissa-addresses.py script with the following arguments:

  a. 'append' - This string indicates that the script should append data from the address file to an existing CSV file.

  b. Street Name - The name of a street to export addresses for. Enter 'ALL' to get all addresses in the Address File.

  c. Address File - Name of file that addresses will be exported from.

  d. Destination File - Name of the file that the address data in CSV format will be appended to.

#### Example
```(venv) python3 pull-melissa-addresses.py append "Main St" TransylvaniaCO ExportedAddresses```

The above command exports the addresses on Main St from the file called TransylvaniaCO.json and appends them to a file called ExportedAddresses.csv.
