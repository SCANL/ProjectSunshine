from datetime import datetime

from common.util_parsing import get_all_return_statements
from model.identifier_type import get_type
from model.issue import Issue
from nlp import custom_terms


class IsNoReturnBool:

    def __init__(self):
        self.__entity = None
        self.__id = 'A.2'
        self.__issues = []
        self.__issue_category = '\'Is\' returns more than a Boolean'
        self.__issue_description = 'The name of a method is a predicate suggesting a true/false value in return. However the return type is not Boolean but rather a more complex type.'

    def __process_identifier(self, identifier):
        # Issue: starting term is a boolean term, but the method does not have a boolean return statement (i.e., true/false not returned)
        if identifier.name_terms[0].lower() in custom_terms.boolean_terms:
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
                issue.identifier_type = get_type(type(identifier).__name__)
                issue.category = self.__issue_category
                issue.details = self.__issue_description
                issue.analysis_datetime = datetime.now()
                self.__issues.append(issue)

    def analyze(self, entity):
        # Analyze all methods in a class
        self.__entity = entity
        for class_item in self.__entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
