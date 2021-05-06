import itertools
from datetime import datetime

from common.enum import IdentifierType
from common.util_parsing import get_all_class_fields
from model.issue import Issue
from nlp.related_terms import clean_text, are_antonyms


class AttributeSignatureCommentOpposite:

    def __init__(self):
        self.__entity = None
        self.__id = 'F.2'
        self.__issues = []
        self.__issue_category = 'Attribute signature and comment are opposite'
        self.__issue_description = 'The declaration of an attribute is in contradiction with its documentation.'

    def __process_identifier(self, identifier):
        # AntiPattern: The identifier name or retrun type and comment contain antonyms
        matched_terms = ''
        comment = identifier.block_comment
        if comment is not None:
            comment_cleansed_terms = clean_text(comment, True)
            unique_combinations_type = list(itertools.product(comment_cleansed_terms, identifier.type_terms))
            unique_combinations_name = list(itertools.product(comment_cleansed_terms, identifier.name_terms))

            result_antonyms = False
            for combination in unique_combinations_type:
                if are_antonyms(combination[0], combination[1]):
                    result_antonyms = True
                    matched_terms = 'Antonyms: \'%s\' and \'%s\'' % (combination[0], combination[1])
                    break

            for combination in unique_combinations_name:
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

    def analyze(self, entity):
        # Analyze all attributes, variables and parameters in a class
        self.__entity = entity
        for class_item in self.__entity.classes:
            fields = get_all_class_fields(class_item)
            for field_item in fields:
                self.__process_identifier(field_item)

        return self.__issues
