from datetime import datetime

from app.common.enum import IdentifierType
from app.common.error_handler import handle_error, ErrorSeverity
from app.common.util_parsing import get_all_return_statements
from app.model.issue import Issue
from app.nlp import term_list


class IsNoReturnBool:

    def __init__(self):
        self.__entity = None
        self.__project = None
        self.__id = 'A.2'
        self.__issues = []
        self.__issue_category = '\'Is\' returns more than a Boolean'
        self.__issue_description = 'The name of a method is a predicate suggesting a true/false value in return. However the return type is not Boolean but rather a more complex type.'

    def __process_identifier(self, identifier):
        # AntiPattern: starting term is a boolean term, but the method does not have a boolean return statement (i.e., true/false not returned)
        try:
            if identifier.name_terms[0].lower() in term_list.get_boolean_terms(self.__project):
                returns = get_all_return_statements(identifier.source)
                return_boolean = 0
                for item in returns:
                    if len(item.xpath('.//src:expr/src:literal[@type="boolean"]',
                                      namespaces={'src': 'http://www.srcML.org/srcML/src'})) != 0:
                        return_boolean += 1

                if len(returns) != return_boolean:
                    issue = Issue()
                    issue.file_path = self.__entity.path
                    issue.identifier = identifier.get_fully_qualified_name()
                    issue.identifier_type = IdentifierType.get_type(type(identifier).__name__)
                    issue.category = self.__issue_category
                    issue.details = self.__issue_description
                    issue.additional_details = 'Starting term: %s' % identifier.name_terms[0]
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
            handle_error('A.2', error_message, ErrorSeverity.Error, False, e)

    def analyze(self, project, entity):
        # Analyze all methods in a class
        self.__project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
