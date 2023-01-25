from logging import getLogger, DEBUG
from typing import Optional as Opt, Any
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base
from sqlite3 import Connection as SQLite3Connection

Base = declarative_base()


@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection: Any, connection_record: Any) -> None:
    """
    It sets relationship checking to state on for the sqlite backend.

    :param dbapi_connection: The handle to the connection object.
    :type dbapi_connection: Any.

    :param connection_record: The connection record.
    :type connection_record: Any.

    :return: None.
    :rtype: None.
    """
    _ = connection_record
    logger = getLogger(__name__)
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON').fetchone()
        logger.setLevel(DEBUG)
        logger.info(f'PRAGMA foreign_key=ON')
        cursor.close()


class SqlEngine:
    """
    It groups data and methods needed in order to work with databases.
    """

    # The class logger instance
    logger = getLogger(__name__)

    @staticmethod
    def get_sqlite_encrypted_engine(dbname: str, key: str) -> Opt[Engine]:
        """
        It returns the encrypted sqlite engine for the given dbname_all by using the given key.

        :param dbname: The name of the database.
        :type dbname: str.

        :param key: The key of the database.
        :type key: str.

        :return: Upon success, it returns the just created Engine instance object, None otherwise.
        """
        # noinspection PyBroadException
        try:

            engine = create_engine(
                'sqlite+pysqlcipher://:{0}@/{1}?'
                'cipher=aes-256-cfb&kdf_iter=64000'.format(key, dbname),
                echo=True
            )
            return engine
        except Exception as e:
            SqlEngine.logger.error(f'{str(e)}')
            return None

    @staticmethod
    def get_sqlite_engine(dbname: str) -> Opt[Engine]:
        """
        It returns the sqlite engine for the given dbname_all.

        :param dbname: The name of the database.
        :type dbname: str.

        :return: Upon success, it returns the just created Engine instance object, None otherwise.
        """
        try:
            engine = create_engine(
                'sqlite+pysqlite:///{0}'.format(dbname),
                echo=True,
                future=True
            )
            return engine
        except Exception as e:
            SqlEngine.logger.error(f'{str(e)}')
            return None
