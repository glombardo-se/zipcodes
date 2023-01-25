"""
It allows loading and checking of Italian zip codes, cities and regions.
"""

from io import BytesIO
from logging import getLogger
from pandas import read_csv, DataFrame
from pathlib import Path
from typing import Optional as Opt
from urllib.request import Request
from urllib.request import urlopen
from zipfile import ZipFile

from data import zipcodes


class Italy:
    """
    It allows italian zip code, city and province retrieval.
    """

    def __init__(self) -> None:
        """
        Constructor.
        """
        self._logger = getLogger(__name__)
        self._data_path = Path('../data')
        self._archive_name = Path(__file__).parent.parent / 'data' / 'listacomuni.zip'
        self._filename = 'listacomuni.txt'
        self._uri = 'http://lab.comuni-italiani.it/files/listacomuni.zip'
        self._file = 'listacomuni.txt'
        self._data_frame = None

    def uri_filename(self) -> Opt[str]:
        """
        It gets the filename of the self._uri resource by performing an HTTP head.

        :return: See description.
        :rtype: str.
        """
        return self._uri[self._uri.rfind('/')+1:]

    def local_check(self) -> bool:
        """
        It checks whether the compressed archive or the text file are present in the data folder.

        :return: It returns True if one of the two files is present, False otherwise.
        :rtype: bool.
        """
        return zipcodes.absolute().exists() or (self._data_path / self.uri_filename()).exists()

    def remote_check(self) -> bool:
        """
        It checks whether the compressed archive can be reached and downloaded through the network.

        :return: It returns True if the compressed archived can be reached through the network, False otherwise.
        :rtype: bool.
        """
        return self.uri_filename() is not None

    def download(self) -> bool:
        """
        It downloads the compressed archive on the data folder and uncompress it.

        :return: It returns True upon success, False otherwise.
        :rtype: bool.
        """
        try:
            data = BytesIO(urlopen(Request(self._uri)).read())
            with open(self._archive_name, 'wb') as target:
                target.write(data.read())

            with ZipFile(self._archive_name, 'r') as archive:
                with archive.open(self._file, 'r') as target:
                    target_file = zipcodes.absolute().open('wb')
                    target_file.write(target.read())
                    target_file.close()

            return True
        except IOError as e:
            self._logger.error(f'{str(e)}')
            return False

    def load(self) -> bool:
        """
        It loads zip code's data into the current instance object.

        :return: It returns True upon success, False otherwise.
        :rtype: bool.
        """
        try:
            self._data_frame = read_csv(
                zipcodes.absolute().__str__(),
                sep=';',
                encoding='utf-8',
                encoding_errors='ignore',
                keep_default_na=False
            )
            return True
        except (Exception, IOError) as e:
            self._logger.error(f'{str(e)}')
            return False

    def parse(self) -> bool:
        """
        It parses the raw data and organize it in an easy-to-access format.

        :return: It returns True upon successful parsing, False otherwise.
        :rtype: bool.
        """
        return self._data_frame is not None

    def ready(self) -> bool:
        """
        It returns True if the current instance is ready to serve data, False otherwise.

        :return: See description.
        :rtype: bool.
        """
        if None is not self._data_frame:
            return True

        if self.local_check():
            if self.load() and self.parse():
                return True

        if self.remote_check():
            if self.download() and self.load() and self.parse():
                return True

        return False

    @property
    def dataframe(self) -> DataFrame:
        """
        Getter for the dataframe member of the current instance.

        :return: See description.
        :rtype DataFrame.
        """
        return self._data_frame


if __name__ == '__main__':
    it = Italy()
    it.ready()
    it.dataframe.to_csv(
        Path(__file__).parent.parent / 'data'/'listacomuni.csv',
        sep=';',
        encoding='utf-8',
        index=False)
