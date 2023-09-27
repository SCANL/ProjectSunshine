from datetime import datetime
import re

from typing_extensions import override
from src.common.enum import IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.util_parsing import get_all_items_in_class
from src.model.issue import Issue
from src.rule.linguistic_antipattern.linguistic_antipattern import LinguisticAntipattern


class ContainsOnlySpecialCharacters(LinguisticAntipattern):

    ID = 'G.1'
    ISSUE_CATEGORY = 'Name contains only special characters'
    ISSUE_DESCRIPTION = 'The name of an identifier is composed of only special characters.'

    def __init__(self):
        super.__init__()

    @override
    def __process_identifier(self, identifier):
        # AntiPattern: All characters in the name are special character
        regex = r"^[^a-zA-Z0-9]+$"
        try:
            count = 0
            for character in identifier.name:
                if re.search(regex, character):
                    count = count + 1
            if count == len(identifier.name):
                issue = Issue(self, identifier)
                self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(type(identifier).__name__), self.__entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('G.1', error_message, ErrorSeverity.Error, False, e)

    @override
    def analyze(self, project, entity):
        # Analyze all attributes, variables and parameters in a class
        self.project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            fields = get_all_items_in_class(class_item)
            for field_item in fields:
                self.__process_identifier(field_item)

        return self.__issues
