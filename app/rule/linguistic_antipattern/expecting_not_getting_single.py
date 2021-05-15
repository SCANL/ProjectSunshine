from datetime import datetime

from app.common.enum import IdentifierType
from app.common.error_handler import ErrorSeverity, handle_error
from app.common.types_list import get_collection_types
from app.model.issue import Issue
from app.nlp.term_property import is_singular


# Impacted File: All
# Impacted identifier: Method


class ExpectingNotGettingSingle:

    def __init__(self):
        self.__entity = None
        self.__project = None
        self.__id = 'A.4'
        self.__issues = []
        self.__issue_category = 'Expecting but not getting single instance'
        self.__issue_description = 'The name of a method indicates that a single object is returned but the return type is a collection.'

    def __process_identifier(self, identifier):
        # AntiPattern: if the last term is singular and the return type is a collection
        try:
            if is_singular(self.__project, identifier.name_terms[-1]):
                if identifier.return_type in get_collection_types(self.__project, self.__entity.language) or identifier.is_array == True:
                    issue = Issue()
                    issue.file_path = self.__entity.path
                    issue.identifier = identifier.get_fully_qualified_name()
                    issue.identifier_type = IdentifierType.get_type(type(identifier).__name__)
                    issue.category = self.__issue_category
                    issue.details = self.__issue_description
                    issue.additional_details = 'Return type: %s' % identifier.return_type
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
            handle_error('A.4', error_message, ErrorSeverity.Critical, False, e)

    def analyze(self, project, entity):
        # Analyze all methods in a class
        self.__project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
