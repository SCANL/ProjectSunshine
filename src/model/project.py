import configparser
import enum
import json
from os import path

from src.common.error_handler import handle_error, ErrorSeverity


class Project:

    initialize_stanford_tagger = None
    config_custom_terms_file = None
    config_custom_code_file = None

    def __init__(self, configuration_file):
        config = configparser.ConfigParser()
        try:
            config.read(configuration_file)
        except configparser.MissingSectionHeaderError as error:
            error_message = "%s" % str(error)
            handle_error('ConfigReader', error_message,
                         ErrorSeverity.Critical, True)

        section_files = 'Files'
        section_properties = 'Properties'

        try:
            self.output_directory = config[section_files]['output_directory']
            self.input_file = config[section_files]['input_file']
        except KeyError as error:
            error_message = "Missing key in the configuration file: %s" % str(
                error)
            handle_error('ConfigReader', error_message,
                         ErrorSeverity.Critical, True)

        try:
            self.junit_version = config[section_properties]['junit_version']
            self.junit_version = float(self.junit_version)
        except ValueError as error:
            self.junit_version = None
        except KeyError as error:
            error_message = "Missing key in the configuration file: %s" % str(
                error)
            handle_error('ConfigReader', error_message,
                         ErrorSeverity.Error, False)
            self.junit_version = None

        try:
            self.custom_code_file = config[section_files]['custom_code']
            self.custom_terms_file = config[section_files]['custom_terms']
        except KeyError as error:
            error_message = "Missing key in the configuration file: %s" % str(
                error)
            handle_error('ConfigReader', error_message,
                         ErrorSeverity.Error, False)

        if not path.exists(self.output_directory) or not path.isdir(self.output_directory):
            error_message = "Invalid \'Output Directory\': \'%s\'" % str(
                self.output_directory)
            handle_error('ConfigReader', error_message,
                         ErrorSeverity.Critical, True)

        if not path.exists(self.input_file) or not path.isfile(self.input_file):
            error_message = "Invalid \'Input File\': \'%s\'" % str(
                self.input_file)
            handle_error('ConfigReader', error_message,
                         ErrorSeverity.Critical, True)

        if not path.exists(self.custom_code_file) or not path.isfile(self.custom_code_file):
            error_message = "Invalid \'Custom Code File\': \'%s\'" % str(
                self.custom_code_file)
            handle_error('ConfigReader', error_message,
                         ErrorSeverity.Warning, False)
        else:
            self.config_custom_code_file = configparser.ConfigParser()
            self.config_custom_code_file.read(self.custom_code_file)

        if not path.exists(self.custom_terms_file) or not path.isfile(self.custom_terms_file):
            error_message = "Invalid \'Custom Terms File\': \'%s\'" % str(
                self.custom_terms_file)
            handle_error('ConfigReader', error_message,
                         ErrorSeverity.Warning, False)
        else:
            self.config_custom_terms_file = configparser.ConfigParser()
            self.config_custom_terms_file.read(self.custom_terms_file)

    def __get_config_value(self, file_type, config_file: configparser.ConfigParser, section: str, key: str):
        """
            Get the value from the configuration file based on the provided section and key.

            Args:
                file_type (ConfigCustomFileType): The type of configuration file (e.g., Terms, Other).
                config_file (configparser.ConfigParser): The configuration file object.
                section (str): The section within the configuration file.
                key (str): The key for the configuration value.

            Returns:
                Any: The configuration value found in the specified section and key.

            Raises:
                Warning: If the specified key or section is not found in the configuration file.
        """
        try:
            return json.loads(config_file.get(section, key))
        except configparser.NoOptionError as key_error:
            error_message = "%s in the %s configuration file \'%s\'" % (
                str(key_error), file_type.name, config_file)
            handle_error('ConfigReader', error_message,
                         ErrorSeverity.Warning, False)
        except configparser.NoSectionError as section_error:
            error_message = "%s in the %s configuration file \'%s\'" % (
                str(section_error), file_type.name, config_file)
            handle_error('ConfigReader', error_message,
                         ErrorSeverity.Warning, False)

    def get_config_value(self, file_type, section: str, key: str):
        """
            Get the value from the appropriate custom configuration file based on the provided file type.

            Args:
                file_type (ConfigCustomFileType): The type of configuration file to use (e.g., Code, Terms).
                section (str): The section within the configuration file.
                key (str): The key for the configuration value.

            Returns:
                Any: The configuration value found in the specified section and key, or None if the file is not available.

            Raises:
                Warning: If the specified key or section is not found in the configuration file.
        """
        if file_type == ConfigCustomFileType.Code and self.config_custom_code_file is not None:
            return self.__get_config_value(file_type, self.config_custom_code_file, section, key)

        if file_type == ConfigCustomFileType.Terms and self.config_custom_terms_file is not None:
            return self.__get_config_value(file_type, self.config_custom_terms_file, section, key)


class ConfigCustomFileType(enum.Enum):
    Code = 1
    Terms = 2
