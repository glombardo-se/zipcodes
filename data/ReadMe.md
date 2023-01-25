# Data package

## Contents
The data package contains the zipcode databases and the auxiliary files.
The zipcode data has been downloaded from `2` different sources:

1. [ComuniItaliani](http://lab.comuni-italiani.it/files/listacomuni.zip)
2. [OpenData](https://data.opendatasoft.com/explore/dataset/geonames-postal-code%40public/export/)

The first one contains the zipcodes of all the Italian cities, while the second one contains the 
zipcodes of all the cities in the world.

Other valuable resources suggested by GitHub Copilot on the topic of zipcodes:

1. [USPS](http://www.usps.com/ncsc/lookups/usps_abbreviations.html)
2. [GeoNames](http://download.geonames.org/export/zip/)
3. [OpenStreetMap](http://download.geonames.org/export/zip/)
4. [OpenAddresses](http://results.openaddresses.io/)
5. [OpenGeoDB](http://download.geonames.org/export/zip/)

## Procedure
The procedure to generate both the zipcode databases is the following:

1. Install and open `DB Browser for SQLite`.
2. Create a new database.
3. Use the import function to import the `CSV` file.
4. Create indexes.
5. Save the database.

## Usage
In order to retrieve the data in the `data` package, the controller
in the `datamodel` package should be used. Direct access to the dbs
is not recommended, since the data is not normalized.
