from src.common.enum import IdentifierType
from src.common.error_handler import ErrorSeverity, handle_error
from src.common.util_parsing import get_all_exception_throws, is_test_method, is_boolean_type
from src.model.entity import Entity
from src.model.issue import Issue
from src.nlp import term_list

# Impacted identifier: All
# Impacted identifier: Method


class ValidateNotConfirm:

    ID = 'B.2'
    ISSUE_CATEGORY = 'Validation method does not confirm'
    ISSUE_DESCRIPTION = 'A validation method does not provide a return value informing whether the validation was successful.'

    def __init__(self):
        self.__issues = []

    # Override
    def __process_identifier(self, identifier):
        # AntiPattern: The name starts with validate and return type is not void and no exception thrown. Not applicable to test methods
        try:
            if not is_test_method(self.__project, self.entity, identifier):
                if identifier.name_terms[0].lower() in term_list.get_validate_terms(self.__project):
                    if (identifier.return_type == 'void') and (len(get_all_exception_throws(identifier.source)) == 0):
                        issue = Issue(self, identifier)
                        self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(
                    type(identifier).__name__), self.entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('B.2', error_message, ErrorSeverity.Error, False, e)

    def analyze(self, project, entity: Entity):
        # Analyze all methods in a class
        self.__project = project
        self.entity = entity
        for class_item in self.entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
