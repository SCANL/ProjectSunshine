from datetime import datetime

from common.enum import IdentifierType
from common.util_parsing import get_all_conditional_statements
from model.issue import Issue


class GetMoreThanAccessor:

    def __init__(self):
        self.__entity = None
        self.__id = 'A.1'
        self.__issues = []
        self.__issue_category = '\'Get\' more than accessor'
        self.__issue_description = 'A getter that performs actions other than returning the corresponding attribute.'
        self.__class_attributes = None

    def __process_identifier(self, identifier):
        # AntiPattern: The method name starts with 'get' AND the method is a getter for an attribute AND the method body contains conditional statements (if, loops, switch)
        if identifier.name_terms[0].lower() == 'get':
            for attribute in self.__class_attributes:
                if identifier.name.lower().endswith(attribute.name.lower()) and identifier.return_type == attribute.type:
                    conditional_statements, conditional_statements_total = get_all_conditional_statements(identifier.source)
                    if conditional_statements_total != 0:
                        issue = Issue()
                        issue.file_path = self.__entity.path
                        issue.identifier = identifier.get_fully_qualified_name()
                        issue.identifier_type = IdentifierType.get_type(type(identifier).__name__)
                        issue.category = self.__issue_category
                        issue.details = self.__issue_description
                        issue.analysis_datetime = datetime.now()
                        self.__issues.append(issue)

    def analyze(self, entity):
        # Analyze all methods in a class
        self.__entity = entity
        for class_item in self.__entity.classes:
            self.__class_attributes = class_item.attributes
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
