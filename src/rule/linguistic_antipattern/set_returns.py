from datetime import datetime

from typing_extensions import override
from src.common.enum import IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.model.issue import Issue
from linguistic_antipattern import LinguisticAntipattern

# Impacted identifier: All
# Impacted identifier: Method
from src.nlp import term_list


class SetReturns(LinguisticAntipattern):

    ID = 'A.3'
    ISSUE_CATEGORY = '\'Set\' method returns'
    ISSUE_DESCRIPTION = 'A set method having a return type different than \'void\'.'

    def __init__(self):
        super.__init__()

    @override
    def __process_identifier(self, identifier):
        # AntiPattern: The name starts with a set, but the method return type is not void
        try:
            if identifier.name_terms[0].lower() in term_list.get_set_terms(self.__project):
                if identifier.return_type != 'void':
                    issue = Issue()
                    issue.file_path = self.__entity.path
                    issue.identifier = identifier.get_fully_qualified_name()
                    issue.identifier_type = IdentifierType.get_type(type(identifier).__name__)
                    issue.category = self.__issue_category
                    issue.details = self.__issue_description
                    issue.additional_details = 'Return type: %s%s' % (identifier.return_type,'(array)' if identifier.is_array else '')
                    issue.id = self.__id
                    issue.analysis_datetime = datetime.now()
                    issue.file_type = self.__entity.file_type
                    issue.line_number = identifier.line_number
                    issue.column_number = identifier.column_number
                    self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(type(identifier).__name__), self.__entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('A.3', error_message, ErrorSeverity.Error, False, e)

    @override
    def analyze(self, project, entity):
        # Analyze all methods in a class
        self.__project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
