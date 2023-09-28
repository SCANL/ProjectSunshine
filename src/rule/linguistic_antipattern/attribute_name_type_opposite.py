import itertools

from src.common.enum import IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.util_parsing import get_all_class_fields
from src.model.entity import Entity
from src.model.issue import Issue
from src.nlp.related_terms import are_antonyms


class AttributeNameTypeOpposite:

    ID = 'F.1'
    ISSUE_CATEGORY = 'Attribute name and type are opposite'
    ISSUE_DESCRIPTION = 'The name of an attribute is in contradiction with its type as they contain antonyms.'

    def __init__(self):
        self.__issues = []

    # Override
    def __process_identifier(self, identifier):
        # AntiPattern: The identifier name and return type name contain antonyms
        try:
            unique_combinations = list(itertools.product(
                identifier.name_terms, identifier.type_terms))
            result_antonyms = False
            matched_terms = 'Data Type: %s;' % identifier.type
            for combination in unique_combinations:
                if combination[0].isalpha() and combination[1].isalpha():
                    if combination[0].lower() != combination[1].lower():
                        if are_antonyms(combination[0], combination[1]):
                            result_antonyms = True
                            matched_terms = matched_terms + \
                                'Antonyms: \'%s\' and \'%s\'' % (
                                    combination[0], combination[1])
                            break

            if result_antonyms:
                issue = Issue(self, identifier)
                issue.additional_details = matched_terms
                self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(
                    type(identifier).__name__), self.entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('F.1', error_message, ErrorSeverity.Error, False, e)

    # Override
    def analyze(self, project, entity: Entity):
        # Analyze all attributes, variables and parameters in a class
        self.project = project
        self.entity = entity
        for class_item in self.entity.classes:
            fields = get_all_class_fields(class_item)
            for field_item in fields:
                self.__process_identifier(field_item)

        return self.__issues
