from src.common.enum import IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.util_parsing import get_all_return_statements, is_boolean_type, is_test_method
from src.model.entity import Entity
from src.model.issue import Issue
from src.nlp import term_list


class IsNoReturnBool:

    ID = 'A.2'
    ISSUE_CATEGORY = '\'Is\' returns more than a Boolean'
    ISSUE_DESCRIPTION = 'The name of a method is a predicate suggesting a true/false value in return. However the return type is not Boolean but rather a more complex type.'

    def __init__(self):
        self.__issues = []

    # Override
    def __process_identifier(self, identifier):
        # AntiPattern: starting term is a boolean term, but the method does not have a boolean return statement (i.e., true/false not returned)
        try:
            if not is_test_method(self.__project, self.entity, identifier):
                if identifier.name_terms[0].lower() in term_list.get_boolean_terms(self.__project):
                    if not is_boolean_type(self.entity, identifier):
                        issue = Issue(self, identifier)
                        issue.additional_details = 'Starting term: %s; Return type: %s%s' % (
                            identifier.name_terms[0], identifier.return_type, '(array)' if identifier.is_array else '')
                        self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(
                    type(identifier).__name__), self.entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('A.2', error_message, ErrorSeverity.Error, False, e)

    def analyze(self, project, entity: Entity):
        # Analyze all methods in a class
        self.__project = project
        self.entity = entity
        for class_item in self.entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
