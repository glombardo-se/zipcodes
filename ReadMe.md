# zipcodes

### Description
The purpose of this package is to allow to retrieve zipcodes also known
as postal codes from a given city in a given country.

### License
The MIT License (MIT). Please see [License File](License.md) for more 
information.


### Installation
```bash
pip install ./zipcodes.wheel
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
