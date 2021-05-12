import itertools
from datetime import datetime

from app.common.enum import IdentifierType
from app.common.util_parsing import get_all_class_fields
from app.model.issue import Issue
from app.nlp.related_terms import are_antonyms


class AttributeNameTypeOpposite:

    def __init__(self):
        self.__entity = None
        self.__project = None
        self.__id = 'F.1'
        self.__issues = []
        self.__issue_category = 'Attribute name and type are opposite'
        self.__issue_description = 'The name of an attribute is in contradiction with its type as they contain antonyms.'

    def __process_identifier(self, identifier):
        # AntiPattern: The identifier name and return type name contain antonyms
        unique_combinations = list(itertools.product(identifier.name_terms, identifier.type_terms))
        result_antonyms = False
        matched_terms = ''
        for combination in unique_combinations:
            if are_antonyms(combination[0], combination[1]):
                result_antonyms = True
                matched_terms = 'Antonyms: \'%s\' and \'%s\'' % (combination[0], combination[1])
                break

        if result_antonyms:
                issue = Issue()
                issue.file_path = self.__entity.path
                issue.identifier = identifier.get_fully_qualified_name()
                issue.identifier_type = IdentifierType.get_type(type(identifier).__name__)
                issue.category = self.__issue_category
                issue.details = self.__issue_description
                issue.additional_details = matched_terms
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
