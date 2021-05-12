import configparser
import os

from common.util import log


class ConfigReader:

    def __get_config_setting(section, name):
        directory_path = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(directory_path, 'config.txt')

        config = configparser.ConfigParser()
        config.read(config_path)
        try:
            return config[section][name]
        except:
            log.exception(msg='Config setting %s not available.' % str(section + name), exc_info=True)

    def read_config(self, section, name):
        self.__get_config_setting('srcml', 'directory')
