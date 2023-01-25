# zipcodes

### Description
The purpose of this python package is to allow easy retrieval of World's 
postal codes (aka zipcodes). It allows both, retrieval of postal codes
by placename and retrieval of placenames by postal code.

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

### License
The MIT License (MIT). Please see [License File](License.md) for more 
information.
