from datetime import datetime

from app.common.enum import IdentifierType
from app.common.util_parsing import get_all_class_fields
from app.model.issue import Issue
from app.nlp import term_list


class NameSuggestBooleanTypeNot:

    def __init__(self):
        self.__entity = None
        self.__project = None
        self.__id = 'D.2'
        self.__issues = []
        self.__issue_category = 'Name suggests boolean but type is not'
        self.__issue_description = 'The name of an attribute suggests that its value is true or false, but its declaring type is not Boolean.'

    def __process_identifier(self, identifier):
        # AntiPattern: The starting term in the name should be a boolean term AND the data type is not a boolean
        if identifier.name_terms[0].lower() in term_list.get_boolean_terms(self.__project):
            if identifier.type != 'boolean' and identifier.type != 'Boolean':
                issue = Issue()
                issue.file_path = self.__entity.path
                issue.identifier = identifier.get_fully_qualified_name()
                issue.identifier_type = IdentifierType.get_type(type(identifier).__name__)
                issue.category = self.__issue_category
                issue.details = self.__issue_description
                issue.additional_details = 'Starting term: \'%s\' Data type: \'%s\'' % (identifier.name_terms[0], identifier.type)
                issue.id = self.__id
                issue.analysis_datetime = datetime.now()
                self.__issues.append(issue)

    def analyze(self, project, entity):
        # Analyze all attributes, variables and parameters in a class
        self.__project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            fields = get_all_class_fields(class_item)
            for field_item in fields:
                self.__process_identifier(field_item)

        return self.__issues
