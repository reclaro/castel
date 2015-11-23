""" Advanced counter.

This script is used to get some statistics from a text file.
The script parse a file and returns the number of words, line,
the most commom letter and the average number of letters per word.
The script has a mandatory argument which is the file to parse.
It is possible to pass different options to set a different
configuration file, the number of decimal digit returned in the
calculation and the encoding of the file
"""

import argparse
import logging
import sys

from configparser import SafeConfigParser
from configparser import NoOptionError
from configparser import NoSectionError
from stevedore import driver


def get_config_value(config_file, section, key):
    """
    Parse a configuration file and return the value associated
    to the given key.
    args:
        config_file: name of the configuration file
        secion: name of the section in the configuration file
                where the key is defined
        key: the name of the key fo lookup in the configuration
             file
    ret:
        the value corresponding to the associated given key
    """
    try:
        config = SafeConfigParser()
        config.read(config_file)
        return config.get(section, key)
    except NoOptionError:
        print("No Option %s in the section %s" % (key, section))
        sys.exit(1)
    except NoSectionError:
        print("No section %s defined " % (section))
        sys.exit(1)


def get_driver(config_file):
    """
    Load the backend driver according to the value specified in the
    configuration file.
    args:
        config_file: The name of the configuration file
    ret:
        The class to use as defined in the configuration file
    """
    driver_name = get_config_value(config_file, 'default', 'driver')
    mgr = driver.DriverManager(namespace='advcounter.plugin',
                               name=driver_name,
                               invoke_on_load=True,
                               )
    return mgr.driver


def get_iowrapper(engine_driver, stream_name, encoding):
    """
    Call the open method of the configured engine driver to
    open the input file specifying the encoding type of the file
    args:
        engine_driver: the class of the configured driver used to
                       perform the statistics
        stream_name: the name of the file to open
        encoding: the encoding to use for reading the file

    ret:
       The TextIOWrapper returned by the open file
    """
    try:
        return engine_driver.open_file(stream_name, encoding=encoding)
    except FileNotFoundError:
        print("File \'%s\' not found" % stream_name)
        sys.exit(1)


def configure_logging(config_file):
    """
    Configure the logging details according to the values
    defined in the configuration file.
    args:
        config_file: the name of the configuration file
    """
    debug_levels = {'debug': logging.DEBUG,
                    'error': logging.ERROR,
                    'critical':  logging.CRITICAL,
                    'fatal': logging.FATAL,
                    'info': logging.INFO,
                    'warning': logging.WARNING}
    log_file = get_config_value(config_file, 'default', 'log_file')
    log_level = get_config_value(config_file, 'default', 'log_level')
    logging.basicConfig(filename=log_file, level=debug_levels[log_level])


def parse_options():
    """ This function manage the options passed to the script

    The method uses the argparse library to parse the input
    options defined for the script
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Name of the file to parse")
    parser.add_argument("-d",
                        "--decimal",
                        metavar="integer",
                        default=1,
                        type=int,
                        help="Number of decimal digits returned by"
                             " calculations, default is 1")
    parser.add_argument("-c",
                        "--config",
                        default="advcounter.conf",
                        help="Path for the config file, default"
                              " is advcounter.conf")
    parser.add_argument("-e",
                        "--encoding",
                        default="utf-8",
                        help="Encoding of the input file")

    return parser.parse_args()


def get_and_print_results(engine_driver, file_obj):
    """Call the engine to get and print the results
    This method call the different method exposed by the driver
    engine to get back the results.
    The results are printed to the standard output
    args:
        engine_driver: the driver configured to parse the file
        file_obj: the TextIoWrapper to pass to the engine methods
    """

    print("number of lines",
         engine_driver.get_total_lines(file_obj))
    file_obj.seek(0)
    print("number of words",
         engine_driver.get_total_words(file_obj))
    file_obj.seek(0)
    print("most common letter",
         engine_driver.most_common_letter(file_obj))
    file_obj.seek(0)
    print("average letter per word",
         engine_driver.get_avg_letters_per_word(file_obj))


def main():
    """
    Main function which parses the options defined and call the
    methods to the engine driver configured to get the statistics
    results
    """
    args = parse_options()
    engine_driver = get_driver(args.config)
    engine_driver.precision = args.decimal
    configure_logging(args.config)

    file_obj = get_iowrapper(engine_driver, args.file, args.encoding)
    try:
        get_and_print_results(engine_driver, file_obj)
    except UnicodeDecodeError:
        print("File \'%s\' is not in the %s format" %
              (args.file, args.encoding))
        sys.exit(1)
    finally:
        file_obj.close()


if __name__ == '__main__':
    main()
