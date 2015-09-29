from __future__ import with_statement, absolute_import

import os.path

from yaml import load

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from .errors import ConfigurationFileInitialized,\
    ConfigurationFileNotFound


class ConfigBase(object):
    def __init__(self, config_file_path):
        self.options = load(open(config_file_path))


class Config(ConfigBase):
    def __init__(self, config_file_path, generate_if_not_found=True):
        if not os.path.isfile(config_file_path):
            if generate_if_not_found:
                self.reset_configfile(config_file_path)
            if os.path.isfile(config_file_path):
                raise ConfigurationFileInitialized("""No configuration file found.
A new file has been initialized at: %s
Please review the configuration and retry...""" % config_file_path)
            else:
                raise ConfigurationFileNotFound("cannot load config file %s" % config_file_path)

        super(Config, self).__init__(config_file_path)

    def reset_configfile(self, file_path):
        with open(file_path, 'w') as f:
            f.write(CONFIG_TEMPLATE)

CONFIG_TEMPLATE = """
# a socket connection will be selected if a 'socket' is specified
# also 'localhost' is a special 'hostname' for MySQL that overrides the 'port' option
# and forces it to use a local socket connection
# if tcp is chosen, you can use compression

mysql:
 hostname: localhost
 port: 3306
 socket: /tmp/mysql.sock
 username: mysql2psql
 password: 
 database: mysql2psql_test
 compress: false
destination:
 # if file is given, output goes to file, else postgres
 file: 
 postgres:
  hostname: localhost
  port: 5432
  username: mysql2psql
  password: 
  database: mysql2psql_test

# if tables is given, only the listed tables will be converted.  leave empty to convert all tables.
#only_tables:
#- table1
#- table2
# if exclude_tables is given, exclude the listed tables from the conversion.
#exclude_tables:
#- table3
#- table4

# if supress_data is true, only the schema definition will be exported/migrated, and not the data
supress_data: false

# if supress_ddl is true, only the data will be exported/imported, and not the schema
supress_ddl: false

# if force_truncate is true, forces a table truncate before table loading
force_truncate: false

# If timezone is true, forces to append/convert to UTC tzinfo mysql data.
# When mysql data has no tzinfo but stores datetimes from another timezone
# than UTC then this will led to conversion errors. Because the naive datetimes
# from mysql will be treated as if they were UTC. If the timezone of the in
# mysql stored datetimes is known use timezone_of_naives_from_mysql option
# to get correctly converted UTC times.
timezone: false

# If timezone_of_naives_from_mysql is set then the naive datetime instances
# which were instantiated from the mysql data are localized to this timezone
# first. Together with the option timezone set to true it is possible to create
# a dump of a mysql database were datetimes have no tzinfo but the timezone
# of them is known from other source and convert them to correct recalculated
# datetimes with UTC tzinfo. This option has only influence on the dump when
# option timezone is set to true.
timezone_of_naives_from_mysql:

# if index_prefix is given, indexes will be created whith a name prefixed with index_prefix
index_prefix:

"""
