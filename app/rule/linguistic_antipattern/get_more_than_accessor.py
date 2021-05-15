from datetime import datetime

from app.common.enum import IdentifierType
from app.common.error_handler import handle_error, ErrorSeverity
from app.common.util_parsing import get_all_conditional_statements
from app.model.issue import Issue


class GetMoreThanAccessor:

    def __init__(self):
        self.__entity = None
        self.__project = None
        self.__id = 'A.1'
        self.__issues = []
        self.__issue_category = '\'Get\' more than accessor'
        self.__issue_description = 'A getter that performs actions other than returning the corresponding attribute.'
        self.__class_attributes = None

    def __process_identifier(self, identifier):
        # AntiPattern: The method name starts with 'get' AND the method is a getter for an attribute AND the method body contains conditional statements (if, loops, switch)
        try:
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
                            issue.additional_details = 'Count of conditional statements: %s' % conditional_statements_total
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
            handle_error('A.1', error_message, ErrorSeverity.Error, False, e)

    def analyze(self, project, entity):
        # Analyze all methods in a class
        self.__project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            self.__class_attributes = class_item.attributes
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
