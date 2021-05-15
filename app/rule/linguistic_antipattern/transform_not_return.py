from datetime import datetime

from app.common.enum import IdentifierType
from app.model.issue import Issue

# Impacted identifier: All
# Impacted identifier: Method
from app.nlp import term_list


class TransformNotReturn:

    def __init__(self):
        self.__entity = None
        self.__project = None
        self.__id = 'B.5'
        self.__issues = []
        self.__issue_category = 'Transform method does not return'
        self.__issue_description = 'The name of a method suggests the transformation of an object but there is no return value.'

    def __process_identifier(self, identifier):
        # AntiPattern: The name starts with or inner term contains transformation term and return type is void
        inner_terms = [x.lower() for x in identifier.name_terms[1:-1]]
        if (identifier.name_terms[0].lower() in term_list.get_transform_terms_staring(self.__project) or
            any(item in inner_terms for item in term_list.get_transform_terms_inner(self.__project))) \
                and identifier.return_type == 'void':
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

    def analyze(self, project, entity):
        # Analyze all methods in a class
        self.__project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
