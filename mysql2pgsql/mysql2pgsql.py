from __future__ import absolute_import

import argparse
import codecs
import sys

from .lib import print_red
from .lib.mysql_reader import MysqlReader
from .lib.postgres_file_writer import PostgresFileWriter
from .lib.postgres_db_writer import PostgresDbWriter
from .lib.converter import Converter
from .lib.config import Config
from .lib.errors import ConfigurationFileInitialized


class Mysql2Pgsql(object):
    def __init__(self, options):
        self.run_options = options
        try:
            self.file_options = Config(options.file, True).options
        except ConfigurationFileInitialized, e:
            print_red(e.message)
            raise e

    def convert(self):
        reader = MysqlReader(self.file_options['mysql'])

        if self.file_options['destination']['file']:
            writer = PostgresFileWriter(self._get_file(self.file_options['destination']['file']), 
                                        self.run_options.verbose, 
                                        tz=self.file_options.get('timezone', False),
                                        tz_of_naives=self.file_options.get('timezone_of_naives_from_mysql', None),
                                        index_prefix=self.file_options.get("index_prefix", ''))
        else:
            writer = PostgresDbWriter(self.file_options['destination']['postgres'], 
                                      self.run_options.verbose, 
                                      tz=self.file_options.get('timezone', False),
                                      tz_of_naives=self.file_options.get('timezone_of_naives_from_mysql', None),
                                      index_prefix=self.file_options.get("index_prefix", ''))

        Converter(reader, writer, self.file_options, self.run_options.verbose).convert()

    def _get_file(self, file_path):
        return codecs.open(file_path, 'wb', 'utf-8')


def main():
    description = 'Tool for migrating/converting data from mysql to postgresql.'
    epilog = 'https://github.com/philipsoutham/py-mysql2pgsql'

    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog)
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show progress of data migration.'
        )
    parser.add_argument(
        '-f', '--file',
        default='mysql2pgsql.yml',
        help='Location of configuration file (default: %(default)s). If none exists at that path, one will be created for you.',
        )
    parser.add_argument(
        '-V', '--version',
        action='store_true',
        help='Print version and exit.'
        )
    options = parser.parse_args()

    if options.version:
        # Someone wants to know the version, print and exit
        from . import __version__
        print(__version__)
        sys.exit(0)

    try:
        Mysql2Pgsql(options).convert()
    except ConfigurationFileInitialized:
        sys.exit(-1)
