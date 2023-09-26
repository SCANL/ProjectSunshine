from datetime import datetime

from src.rule.linguistic_antipattern.linguistic_antipattern import LinguisticAntipattern
from src.common.enum import IdentifierType
class Issue:

    def __init__(self, linguistic_antipattern: LinguisticAntipattern, identifier):
        self.__details = linguistic_antipattern.ISSUE_DESCRIPTION
        self.__additional_details = ''
        self.__category = linguistic_antipattern.ISSUE_CATEGORY
        self.__identifier_type = IdentifierType.get_type(type(identifier).__name__)
        self.__identifier = identifier.get_fully_qualified_name()
        self.__file_path = linguistic_antipattern.entity.path
        self.__analysis_datetime = datetime.now()
        self.__id = linguistic_antipattern.ID
        self.__file_type = linguistic_antipattern.entity.file_type
        self.__line_number = identifier.line_number
        self.__column_number = identifier.column_number

    @property
    def details(self):
        return self.__details
    
    @details.setter
    def details(self, value):
        self.__details = value

    @property
    def additional_details(self):
        return self.__additional_details 

    @additional_details.setter
    def additional_details(self, value):
        self.__additional_details = value

    @property
    def category(self):
        return self.__category
    
    @category.setter
    def category(self, value):
        self.__category = value

    @property
    def identifier_type(self):
        return self.__identifier_type
    
    @identifier_type.setter
    def identifier_type(self, value):
        self.__identifier_type = value

    @property
    def identifier(self):
        return self.__identifier
    
    @identifier.setter
    def identifier(self, value):
        self.__identifier = value

    @property
    def file_path(self):
        return self.__file_path

    @file_path.setter
    def file_path(self, value):
        self.__file_path = value

    @property
    def analysis_datetime(self):
        return self.__analysis_datetime

    @analysis_datetime.setter
    def analysis_datetime(self, value):
        self.__analysis_datetime = value

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def file_type(self):
        return self.__file_type
    
    @file_type.setter
    def file_type(self, value):
        self.__file_type = value

    @property
    def line_number(self):
        return self.__line_number
    
    @line_number.setter
    def line_number(self, value):
        self.__line_number = value

    @property
    def collumn_number(self):
        return self.__column_number
    
    @collumn_number.setter
    def collumn_number(self, value):
        self.__column_number = value