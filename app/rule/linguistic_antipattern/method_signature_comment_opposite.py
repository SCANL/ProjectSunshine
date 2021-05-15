import itertools
from datetime import datetime

from app.common.enum import IdentifierType
from app.common.error_handler import handle_error, ErrorSeverity
from app.model.issue import Issue
from app.nlp.related_terms import are_antonyms, clean_text


class MethodSignatureCommentOpposite:

    def __init__(self):
        self.__entity = None
        self.__project = None
        self.__id = 'C.2'
        self.__issues = []
        self.__issue_category = 'Method signature and comment are opposite'
        self.__issue_description = 'The documentation of a method is in contradiction with its declaration.'

    def __process_identifier(self, identifier):
        # AntiPattern: The method name or retrun type and comment contain antonyms
        try:
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
                        matched_terms = 'Antonyms: \'%s\' and \'%s\'' %(combination[0], combination[1])
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
                    issue.file_type = self.__entity.file_type
                    issue.line_number = identifier.line_number
                    issue.column_number = identifier.column_number
                    self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(type(identifier).__name__), self.__entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('C.2', error_message, ErrorSeverity.Error, False, e)

    def analyze(self, project, entity):
        # Analyze all methods in a class
        self.__project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
