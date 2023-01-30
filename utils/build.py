"""
It builds the project.
"""

from argparse import ArgumentParser, Namespace
from colorama import AnsiToWin32, Fore, Style, init as colorama_init
from timeit import timeit
from logging import NOTSET, INFO, WARNING, ERROR, DEBUG
from logging import getLogRecordFactory, setLogRecordFactory, basicConfig, getLogger, LogRecord
from os import environ
from os.path import basename
from pathlib import Path
from platform import system as system_platform
from re import sub
from signal import signal, SIGINT
from subprocess import check_output, CalledProcessError
from sys import argv, stdout
from typing import Any, Dict, List, Optional as Opt
from types import FrameType

major = 1
minor = 0
fixes = 0


class LoggingRecordFactoryColorama:
    """
    It adds the 'color' and 'reset' attributes to the LogRecord instance produced by the existing LogRecord.
    """

    levels_map = {
        INFO: Fore.LIGHTBLUE_EX + Style.DIM,
        DEBUG: Fore.GREEN + Style.BRIGHT,
        WARNING: Fore.LIGHTYELLOW_EX + Style.DIM,
        ERROR: Fore.LIGHTRED_EX + Style.DIM,
        NOTSET: Fore.RESET
    }

    color_attr = 'color'
    reset_attr = 'reset'

    def __init__(self, level_map: Opt[Dict[int, str]] = None, existing_factory: Any = getLogRecordFactory()) -> None:
        """
        It creates an instance of the LoggingRecordFactoryColorama class with the given level_map and existing_factory.

        :param level_map:           The dictionary mapping levels to colors.
        :type level_map:            Opt[Dict[int, str]].
        
        :param existing_factory:    The default LogRecordFactory to be used.
        :type existing_factory:     Any.
        """
        self.levels_map = level_map if level_map else self.__class__.levels_map
        self.existing_factory = existing_factory
        setLogRecordFactory(self)

    def __call__(self, *args: Any, **kwargs: Any) -> LogRecord:
        """
        It adds the color_attr and reset_attr attribute's values according to the given levels_map, to the kwargs of the
        record built and returned by the existing_factory, and returns it to the caller.

        :param args:    The positional args to pass to the existing_factory.
        :type args:     Any.
        
        :param kwargs:  The keyword arguments to pass to the existing_factory.
        :type kwargs:   Any.

        :return: The record with the new arguments added.
        :rtype: LogRecord.
        """
        record = self.existing_factory(*args, **kwargs)
        setattr(record, self.__class__.color_attr, self.levels_map[record.levelno])
        setattr(record, self.__class__.reset_attr, self.levels_map[NOTSET])
        return record


def logging_console_init(level: int = INFO) -> None:
    """
    It initializes the default logging configuration.
    
    :param level:   The wanted logging level.
    :type level:    int.

    :return: None.
    :rtype: None.
    """

    color_attr = LoggingRecordFactoryColorama.color_attr
    reset_attr = LoggingRecordFactoryColorama.reset_attr
    stream = stdout if 'Windows' not in system_platform() else AnsiToWin32(stdout).stream
    colorama_init()

    # Removed from the format key of config for efficiency in space and time:
    #   [%(asctime)s.%(msecs)03d]         --> date and time in the given datefmt
    #   [%(processName)s.%(process)d]     --> process name dot process id
    #   [%(levelname)s]                   --> level name

    # Removed from the datefmt key of config for efficiency in space and time:
    #   %Y/%m/%d %H:%M:%S'                --> the format of the date in asctime when given

    config = dict(
        level=level,
        stream=stream,
        format=f'%({color_attr})s%(message)s%({reset_attr})s',
    )

    basicConfig(**config)
    LoggingRecordFactoryColorama()


def author() -> str:
    """
    It returns a brief string giving credits to the authors.

    :return: See description.
    :rtype: str.
    """
    return '(c) 2023 Giovanni Lombardo mailto://g.lombardo@protonmail.com'


def version() -> str:
    """
    It returns a version string for the current program.

    :return: See description.
    :rtype: str.
    """
    global major, minor, fixes
    return '{0} version {1}\n'.format(basename(argv[0]), '.'.join(map(str, [major, minor, fixes])))


def sigint_handler(signum: int, frame: FrameType) -> None:
    """
    The handler registered for SIGINT signal handling. It terminates the application.

    :param signum:  The signal.
    :type signum:   int.
    
    :param frame:   The frame.
    :type frame:    FrameType.

    :return: None.
    :rtype: None.
    """

    _, _ = frame, signum
    getLogger(__name__).warning('Interrupt received..')
    exit(0)


def usage(args: List[str]) -> Namespace:
    """
    It parses the given args (usually from sys.argv) and checks they conform to the rules of the application.
    It then returns a namedtuple with a field for any given or defaulted argument.

    :param args:    The command line arguments to be parsed.
    :type args:     List[str].

    :return: See description.
    :rtype: NamedTuple.
    """
    helps = dict(
        description=__doc__,
        arg='arg description',
    )

    getLogger(__name__)
    parser = ArgumentParser(description=helps['description'])
    # parser.add_argument('arg', help=helps['arg'])

    args = parser.parse_args(args)

    return args


def main(args: Namespace) -> None:
    """
    It starts the application.

    :param args:    The parsed command line arguments as returned by usage();
    :type args:     Namespace.

    :return: None.
    :rtype: None.
    """
    _ = args
    logger = getLogger(__name__)
    setup = Path(__file__).parent.parent / 'setup.py'
    logger.info(f'Updating {setup} version...')
    release = environ['APPVEYOR_BUILD_RELEASE']
    logger.info(f'New version: {release}')

    try:
        with setup.open('r') as f:
            data = f.read()

        data = sub('"1\.0\.0"', f'"{release}"', data)
        with setup.open('w') as f:
            f.write(data)
        logger.info(f'Updated {setup} version.')
    except (IOError, OSError) as e:
        logger.error(f'{str(e)}')
        logger.exception(f'Failed to update {setup} version.')
        exit(1)

    try:
        out = check_output(f'$(which python3) {setup} sdist bdist_wheel', shell=True)
        logger.info(out.decode('utf-8'))
        logger.info(f'Created {setup} distribution.')
    except CalledProcessError as e:
        logger.error(f'{str(e)}')
        logger.exception(f'Failed to create zipcode package.')
        exit(1)


def external_main(args: List[str]) -> int:
    """
    The procedure that allows realization of standalone applications.

    :param args:    The command line arguments to be parsed by the application.
    :type args:     List[str].

    :return: The value returned to the OS.
    :rtype: int.
    """
    logging_console_init()
    signal(SIGINT, sigint_handler)
    print(author())
    print(version())
    print(f'Elapsed time: {timeit(stmt=lambda: main(usage(args)), number=1)} s.')
    return 0


if __name__ == '__main__':
    external_main(argv[1:])
