# NW Scheduler Address Exporters

Python scripts for pulling addresses from web APIs and exporting the address data into CSV files that can be imported into NW Scheduler.

- [gis.transylvaniacounty.org](https://github.com/darylfoster/NWS-AddressExporter/tree/main/gis.transylvaniacounty.org) - Pulls addresses from the [Transylvania County Hub Site's](https://gis.transylvaniacounty.org/portal/apps/sites/#/transylvania-county-hub-site/search?collection=Dataset) API.
- [melissa.com](https://github.com/darylfoster/NWS-AddressExporter/tree/main/melissa.com) - Pulls addresses from the [melissa](melissa.com) API. (Requires site registration and a license key.)

## Setup

1. Download and install Python version 3 or later from [www.python.org](https://www.python.org/downloads/).
2. Create a [virtual environment](https://docs.python.org/3/library/venv.html) by executing the following command:
    ```bash
    python3 -m venv /path/to/new/virtual/environment
    ```
3. Activate the virtual environment

    a. Unix/Linux/MacOS

    ```bash
    > source /path/to/new/virtual/environment/bin/activate
    ```
    b. Windows

    ```> C:\path\to\new\virtual\environment\Scripts\activate```
4. Install Python "requests" package with the following command:

    ```(venv) python3 -m pip install requests```

