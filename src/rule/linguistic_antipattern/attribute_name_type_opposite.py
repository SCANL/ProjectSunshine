import itertools
from datetime import datetime

from src.common.enum import IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.util_parsing import get_all_class_fields
from src.model.issue import Issue
from src.nlp.related_terms import are_antonyms


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
        try:
            unique_combinations = list(itertools.product(identifier.name_terms, identifier.type_terms))
            result_antonyms = False
            matched_terms = 'Data Type: %s;' % identifier.type
            for combination in unique_combinations:
                if combination[0].isalpha() and combination[1].isalpha():
                    if combination[0].lower() != combination[1].lower():
                        if are_antonyms(combination[0], combination[1]):
                            result_antonyms = True
                            matched_terms = matched_terms + 'Antonyms: \'%s\' and \'%s\'' % (combination[0], combination[1])
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
                    issue.file_type = self.__entity.file_type
                    issue.line_number = identifier.line_number
                    issue.column_number = identifier.column_number
                    self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(type(identifier).__name__), self.__entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('F.1', error_message, ErrorSeverity.Error, False, e)

    def analyze(self, project, entity):
        # Analyze all attributes, variables and parameters in a class
        self.__project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            fields = get_all_class_fields(class_item)
            for field_item in fields:
                self.__process_identifier(field_item)

        return self.__issues
