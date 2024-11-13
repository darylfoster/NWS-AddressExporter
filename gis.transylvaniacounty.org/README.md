# Pull-GIS-Transylvania-County-Addresses

Pulls addresses from the [Transylvania County Hub Site](https://gis.transylvaniacounty.org/portal/apps/sites/#/transylvania-county-hub-site/search?collection=Dataset) and exports address data into CSV files that can be imported into NW Scheduler.

## Files
- pull-transylvaniacounty-addresses.py - Python script for pulling address data from the [Transylvania County Hub Site](https://gis.transylvaniacounty.org/portal/apps/sites/#/transylvania-county-hub-site/search?collection=Dataset) and exporting address data to CSV files.
- TransylvaniaCounty.json - Data file containing all addresses pulled for Transylvania County NC.
- TransylvaniaCounty-Exported.json - Data file containing all addresses exported using other scripts/APIs.

## Usage

### Pull Addresses
Pull addresses by executing the pull-transylvaniacounty-addresses.py script with the following arguments:

  a. 'pull' - This string indicates that the script should pull address data from the [Transylvania County Hub Site](https://gis.transylvaniacounty.org/portal/apps/sites/#/transylvania-county-hub-site/search?collection=Dataset).

  b. Min Longitude - Numerical longitude of the western edge of the area for which the addresses will be pulled.

  c. Max Longitude - Numerical longitude of the eastern edge of the area for which the addresses will be pulled.

  d. Min Latitude - Numerical latitude of the southern edge of the area for which the addresses will be pulled.

  e. Max Latitude - Numerical latitude of the northern edge of the area for which the addresses will be pulled.

#### Example
```(venv) python3 pull-transylvaniacounty-addresses.py pull -82.728564 -82.656850 35.210000 35.233803```

The above command pulls addresses within the rectangular area described by the longitude and latitude coordinates. It appends the results to a file called TransylvaniaCounty.json.

Note: The API has a transfer limit of around 2000 addresses. The script will not return the results if that limit is exceeded.

### Create New CSV Export
Export addresses to a new CSV file by executing the pull-transylvaniacounty-addresses.py script with the following arguments:

  a. 'export' - This string indicates that the script should export data from the TransylvaniaCounty.json file to a new CSV file.

  b. Destination File - Name of the file that will be created containing address data in CSV format.

#### Example
```(venv) python3 pull-transylvaniacounty-addresses.py export ExportedAddresses```

The above command exports the non-exported addresses from the file called TransylvaniaCounty.json to a file called ExportedAddresses.csv.

Note: If more than 300 addresses are exported, then multiple export files will be created. Once an address is exported, it is marked as "Exported" in the TransylvaniaCounty.json file. As a result each address can be exported only one time.
