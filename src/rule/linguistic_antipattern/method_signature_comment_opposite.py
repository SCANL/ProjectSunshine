import itertools
from datetime import datetime

from typing_extensions import override
from src.common.enum import IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.util_parsing import is_test_method
from src.model.issue import Issue
from src.nlp.related_terms import are_antonyms, clean_text
from linguistic_antipattern import LinguisticAntipattern


class MethodSignatureCommentOpposite(LinguisticAntipattern):

    ID = 'C.2'
    ISSUE_CATEGORY = 'Method signature and comment are opposite'
    ISSUE_DESCRIPTION = 'The documentation of a method is in contradiction with its declaration.'

    def __init__(self):
        super.__init__()

    @override
    def __process_identifier(self, identifier):
        # AntiPattern: The method name or return type and comment contain antonyms
        try:
            if not is_test_method(self.__project, self.__entity, identifier):
                matched_terms = 'Return Type: %s%s;' % (identifier.return_type,'(array)' if identifier.is_array else '')
                comment = identifier.block_comment
                if comment is not None:
                    comment_cleansed_terms = clean_text(comment, True)
                    unique_combinations_type = list(itertools.product(comment_cleansed_terms, identifier.type_terms))
                    if identifier.name_terms[0] == 'get':
                        unique_combinations_name = list(itertools.product(comment_cleansed_terms, identifier.name_terms[1:]))
                    else:
                        unique_combinations_name = list(itertools.product(comment_cleansed_terms, identifier.name_terms))

                    result_antonyms = False
                    for combination in unique_combinations_type:
                        if combination[0].isalpha() and combination[1].isalpha():
                            if combination[0].lower() != combination[1].lower():
                                if are_antonyms(combination[0], combination[1]):
                                    result_antonyms = True
                                    matched_terms = matched_terms + 'Antonyms: \'%s\' and \'%s\'' %(combination[0], combination[1])
                                    break

                    for combination in unique_combinations_name:
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
            handle_error('C.2', error_message, ErrorSeverity.Error, False, e)

    @override
    def analyze(self, project, entity):
        # Analyze all methods in a class
        self.__project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
