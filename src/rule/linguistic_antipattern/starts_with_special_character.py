import re

from src.common.enum import IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.util_parsing import get_all_items_in_class
from src.model.issue import Issue
from src.rule.linguistic_antipattern.linguistic_antipattern import LinguisticAntipattern

class StartsWithSpecialCharacter(LinguisticAntipattern):

    ID = 'X.5'
    ISSUE_CATEGORY = 'Name starts with special character'
    ISSUE_DESCRIPTION = 'The name of an identifier starts with a special character.'

    def __init__(self):
        super.__init__()

    #Override
    def __process_identifier(self, identifier):
        # AntiPattern: The first character in the name is a special character
        regex = r"^[^a-zA-Z0-9]+$"
        try:
            matches = re.search(regex, identifier.name[0])
            if matches:
                issue = Issue(self, identifier)
                issue.additional_details = 'Starting character: \'%s\'' % (identifier.name[0])
                self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(type(identifier).__name__), self.__entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('X.5', error_message, ErrorSeverity.Error, False, e)

    #Override
    def analyze(self, project, entity):
        # Analyze all attributes, variables and parameters in a class
        self.project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            fields = get_all_items_in_class(class_item)
            for field_item in fields:
                self.__process_identifier(field_item)

        return self.__issues
