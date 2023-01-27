from sqlalchemy import Column, Integer, String, REAL
from .sqlengine import Base, SqlEngine
from typing import Tuple, Any


class ZipCodes(Base):
    """
    It represents the Users of the system.
    """

    __tablename__ = 'geonames-postal-code'
    __table_args__ = {'extend_existing': True}

    countrycode = Column(String, nullable=True)
    postalcode = Column(Integer, nullable=False, primary_key=True)
    placename = Column(String, nullable=True)
    adminname1 = Column(String, nullable=True)
    admincode1 = Column(Integer, nullable=True)
    adminname2 = Column(String, nullable=True)
    admincode2 = Column(Integer, nullable=True)
    adminname3 = Column(String, nullable=True)
    admincode3 = Column(Integer, nullable=True)
    latitude = Column(REAL, nullable=True)
    longitude = Column(REAL, nullable=True)
    accuracy = Column(Integer, nullable=True)
    coordinates = Column(String, nullable=True)

    def to_tuple(self) -> Tuple[Any]:
        """
        It returns a tuple representation of the current object.

        :return: See description.
        :rtype: Tuple[Any].
        """
        return self.postalcode, self.countrycode, self.placename, self.adminname1, self.admincode1,\
                self.adminname2, self.admincode2, self.adminname3, self.admincode3, self.latitude,\
                self.longitude, self.accuracy, self.coordinates

    def __repr__(self) -> str:
        """
        It returns a representation of the current object in form of string.

        :return: See description.
        :rtype: str.
        """
        return f"<ZipCode(zip='{self.postalcode}', countrycode='{self.countrycode}', placename='{self.placename}')>"


class ZipCodesIT(Base):
    """
    It represents the Users of the system.
    """

    __tablename__ = 'listacomuni'
    __table_args__ = {'extend_existing': True}

    Istat = Column(Integer, nullable=False, primary_key=True)
    Comune = Column(String, nullable=True)
    Provincia = Column(String, nullable=True)
    Regione = Column(String, nullable=True)
    Prefisso = Column(Integer, nullable=True)
    CAP = Column(Integer, nullable=True)
    CodFisco = Column(String, nullable=True)
    Abitanti = Column(Integer, nullable=True)
    Link = Column(String, nullable=True)

    def __repr__(self) -> str:
        """
        It returns a representation of the current object in form of string.

        :return: See description.
        :rtype: str.
        """
        return f"<ZipCodeIT(zip='{self.CAP}', placename='{self.Comune}')>"


if __name__ == '__main__':
    from sqlalchemy.orm import Session
    from configuration import configuration as cfg

    dbname = cfg['db_folder'] / 'zipcodes.db'
    engine = SqlEngine.get_sqlite_engine(dbname.__str__())

    dbnameItaly = cfg['db_folder'] / 'zipcodes_IT.db'
    engineItaly = SqlEngine.get_sqlite_engine(dbnameItaly.__str__())

    # create session and add objects
    with Session(bind=engine) as session, session.begin():
        data = session.query(ZipCodes).all()
        for item in data:
            print(item)

    with Session(bind=engineItaly) as session, session.begin():
        data = session.query(ZipCodesIT).all()
        for item in data:
            print(item)
