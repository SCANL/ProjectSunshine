from src.common.enum import IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.util_parsing import get_all_return_statements, is_test_method
from src.model.entity import Entity
from src.model.issue import Issue
from src.nlp import term_list


class GetNoReturn:

    ID = 'B.3'
    ISSUE_CATEGORY = '\'Get\' method does not return'
    ISSUE_DESCRIPTION = 'The name suggests that the method returns something (e.g., name starts with \'get\' or \'return\').'

    def __init__(self):
        self.__issues = []

    # Override
    def __process_identifier(self, identifier):
        # AntiPattern: The name starts with a get term, but the return type is void
        try:
            if not is_test_method(self.__project, self.entity, identifier):
                if identifier.name_terms[0].lower() in term_list.get_get_terms(self.__project):
                    if identifier.return_type == 'void':
                        issue = Issue(self, identifier)
                        self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(
                    type(identifier).__name__), self.entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('B.3', error_message, ErrorSeverity.Error, False, e)

    def analyze(self, project, entity: Entity):
        # Analyze all methods in a class
        self.__project = project
        self.entity = entity
        for class_item in self.entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
