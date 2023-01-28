from datetime import datetime
from typing import Optional as Opt, List
from logging import getLogger, INFO
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from configuration import configuration as cfg
from model import ZipCodes, ZipCodesIT
from sqlengine import SqlEngine


class Controller:
    """
    It mediates access to the database data through
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        self.logger = getLogger(__name__)
        self.logger.debug(f'Controller created at: {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}')
        self.dbname_it = cfg['db_folder'] / 'zipcodes_IT.db'
        self.engine_it = SqlEngine.get_sqlite_engine(self.dbname_it.__str__())
        self.logger.debug(f'SqlEngine created at: {datetime.now().strftime("%Y/%m/%d %H:%M:%S")}')

    def zipcode_by_placename(self, placename: str, countrycode: str) -> Opt[int]:
        """
        It gets the zipcode of the place in placename or None.

        :param placename: The name of the place to retrieve the zipcode from.
        :type placename: str.

        :param countrycode: The country code.
        :type countrycode: str.

        :return: It returns the zipcode for the given placename if it exists or None.
        :rtype: Opt[int].
        """
        try:
            if countrycode == 'IT':
                with Session(bind=self.engine_it) as session, session.begin():
                    data = session.query(ZipCodesIT).\
                        filter(ZipCodesIT.Comune == f'{placename}').all()
                    return data[0].CAP if data else None

            dbname = cfg['db_folder'] / f'zipcodes_{countrycode}.db'
            engine = SqlEngine.get_sqlite_engine(dbname.__str__())
            with Session(bind=engine) as session, session.begin():
                data = session.query(ZipCodes).filter(
                    ZipCodes.placename == f'{placename}',
                    ZipCodes.countrycode == f'{countrycode}').all()
                return data[0].postalcode if data else None
        except SQLAlchemyError as e:
            self.logger.error(f'{e.__str__()}')
            return None

    def placenames_by_zipcode(self, countrycode: str, zipcode: int) -> Opt[List[str]]:
        """
        It gets the names of the places in the country with the given pair (countrycode, zipcode) or None.

        :param countrycode: The country code.
        :type countrycode: str.

        :param zipcode: The zipcode.
        :type zipcode: int.

        :return: It returns the place's name in the country with the given countrycode having the given zipcode or None.
        :rtype: Opt[List[str]].
        """
        try:
            if countrycode == 'IT':
                with Session(bind=self.engine_it) as session, session.begin():
                    data = session.query(ZipCodesIT).filter(
                        ZipCodesIT.CAP == f'{zipcode}'
                    ).all()
                    return [item.Comune for item in data] if data else None

            dbname = cfg['db_folder'] / f'zipcodes_{countrycode}.db'
            engine = SqlEngine.get_sqlite_engine(dbname.__str__())
            with Session(bind=engine) as session, session.begin():
                data = session.query(ZipCodes).filter(
                    ZipCodes.countrycode == f'{countrycode}',
                    ZipCodes.postalcode == f'{zipcode}'
                ).all()
                return [item.placename for item in data] if data else None
        except SQLAlchemyError as e:
            self.logger.error(f'{e.__str__()}')
            return None


if __name__ == '__main__':
    getLogger(__name__).setLevel(INFO)
    ctr = Controller()
    print(ctr.zipcode_by_placename('Leggiuno', 'IT'))
    print(ctr.placenames_by_zipcode('IT', 21038))
