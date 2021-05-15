from datetime import datetime

from app.common.enum import IdentifierType
from app.common.error_handler import handle_error, ErrorSeverity
from app.model.issue import Issue
from app.nlp import term_list


class NotAnsweredQuestion:

    def __init__(self):
        self.__entity = None
        self.__project = None
        self.__id = 'B.4'
        self.__issues = []
        self.__issue_category = 'Not answered question'
        self.__issue_description = 'The name of a method is in the form of predicate whereas the return type is not Boolean.'

    def __process_identifier(self, identifier):
        # AntiPattern: starting term is a boolean term, but the method return type is void
        try:
            if identifier.name_terms[0].lower() in term_list.get_boolean_terms(self.__project) and identifier.return_type == 'void':
                issue = Issue()
                issue.file_path = self.__entity.path
                issue.identifier = identifier.get_fully_qualified_name()
                issue.identifier_type = IdentifierType.get_type(type(identifier).__name__)
                issue.category = self.__issue_category
                issue.details = self.__issue_description
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
            handle_error('B.4', error_message, ErrorSeverity.Error, False, e)

    def analyze(self, project, entity):
        # Analyze all methods in a class
        self.__project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
