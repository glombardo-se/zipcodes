# zipcodes

### Description
The purpose of this `Python` package is to allow easy retrieval of the world's 
postal codes (aka zipcodes). At the current release it consents:

+ to retrieve the postal code of a given placename
+ to retrieve the placenames of a given postal code

### Installation
```bash
pip install ./zipcodes.zip
```

### Usage
```python
from zipcodes import Controller

controller = Controller()
controller.zipcode_by_placename('Leggiuno', 'IT')
# ['21038']

controller.placenames_by_zipcode('IT', '21038')
# ['Leggiuno', 'Sangiano']
```

### License
The MIT License (MIT). Please see [License File](License.md) for more 
information.
