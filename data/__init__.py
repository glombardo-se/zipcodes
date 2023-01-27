from pathlib import Path
from countrycodes import countrycodes
from countrynames import countrynames

zipcodes = Path(__file__).parent / 'zipcodes.db'
zipcodes_IT = Path(__file__).parent / 'zipcodes_IT.db'
readme = Path(__file__).parent / 'ReadMe.md'

__all__ = [
    zipcodes,
    zipcodes_IT,
    readme,
]
