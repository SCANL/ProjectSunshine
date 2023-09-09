import configparser
import os

from src.common.util import log


class ConfigReader:
    """
        Deprecated utility class for reading configuration settings.
        Something was wrong with this class anyways.
        VSCode will complain about types cause `__get_config_setting` should accept self as first argument.
    """

    def __get_config_setting(section, name):
        directory_path = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(directory_path, 'config.txt')

        config = configparser.ConfigParser()
        config.read(config_path)
        try:
            return config[section][name]
        except:
            log.exception(msg='Config setting %s not available.' %
                          str(section + name), exc_info=True)

    def read_config(self, section, name):
        self.__get_config_setting('srcml', 'directory')
