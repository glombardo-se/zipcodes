from argparse import ArgumentParser, Namespace
from logging import getLogger
from sqlite3 import connect
from sys import exit, argv
from typing import List, Optional as Opt

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from countrycodes import countrycodes
from datamodel import SqlEngine
from datamodel import ZipCodes
from datamodel.configuration import configuration as cfg

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# noinspection SqlNoDataSourceInspection
TABLE = '''
CREATE TABLE "geonames-postal-code" (
    "countrycode"	TEXT,
    "postalcode"	INTEGER,
    "placename"	    TEXT,
    "adminname1"	TEXT,
    "admincode1"	INTEGER,
    "adminname2"	TEXT,
    "admincode2"	INTEGER,
    "adminname3"	TEXT,
    "admincode3"	TEXT,
    "latitude"	    REAL,
    "longitude"	    REAL,
    "accuracy"	    INTEGER,
    "coordinates"	TEXT);
'''


def usage(args: List[str]) -> Opt[Namespace]:
    """
    Parse command line arguments.

    :arg args: Command line arguments
    :type args: List[str].

    :return: Parsed arguments if successful, None otherwise.
    :rtype: Optional[Namespace].
    """
    helps = {
        'mode': 'Mode of operation',
    }

    parser = ArgumentParser(description='Split the database into chunks divided by countrycode.')
    parser.add_argument('mode', choices=['split'], help=helps['mode'])
    return parser.parse_args(args)


def main(args: Namespace) -> int:
    """
    Main entry point.

    :arg args: Parsed command line arguments.
    :type args: Namespace.

    :return: Exit status code.
    :rtype: int.
    """
    logger = getLogger(__name__)
    if args.mode == 'split':
        try:
            engine = SqlEngine.get_sqlite_engine(cfg['db_folder'] / 'zipcodes.db')
            for code, name in countrycodes.items():
                if code == 'IT':
                    continue
                with Session(bind=engine) as session, session.begin():
                    data = session.query(ZipCodes).filter(ZipCodes.countrycode == code).all()
                    if not data:
                        continue
                    connection = connect(cfg['db_folder'] / f'zipcodes_{code}.db')
                    cursor = connection.cursor()
                    cursor.execute(TABLE)
                    cursor.executemany('INSERT INTO "geonames-postal-code" '
                                       'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                       [d.to_tuple() for d in data])
                    connection.commit()
                    connection.close()
        except SQLAlchemyError as e:
            logger.error(f'{e.__str__()}')
            return EXIT_FAILURE

    return EXIT_SUCCESS


if __name__ == '__main__':
    exit(main(usage(argv[1:])))
