import itertools

from src.common.enum import IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.util_parsing import get_all_class_fields
from src.model.issue import Issue
from src.nlp.related_terms import clean_text, are_antonyms
from src.rule.linguistic_antipattern.linguistic_antipattern import LinguisticAntipattern


class AttributeSignatureCommentOpposite(LinguisticAntipattern):

    ID = 'F.2'
    ISSUE_CATEGORY = 'Attribute signature and comment are opposite'
    ISSUE_DESCRIPTION = 'The declaration of an attribute is in contradiction with its documentation.'

    def __init__(self):
        super.__init__()

    #Override
    def __process_identifier(self, identifier):
        # AntiPattern: The identifier name or retrun type and comment contain antonyms
        try:
            matched_terms = 'Date Type: %s%s;' % (identifier.type, '(array)' if identifier.is_array else '')
            comment = identifier.block_comment
            if comment is not None:
                comment_cleansed_terms = clean_text(comment, True)
                unique_combinations_type = list(itertools.product(comment_cleansed_terms, identifier.type_terms))
                unique_combinations_name = list(itertools.product(comment_cleansed_terms, identifier.name_terms))

                result_antonyms = False
                for combination in unique_combinations_type:
                    if combination[0].isalpha() and combination[1].isalpha():
                        if combination[0].lower() != combination[1].lower():
                            if are_antonyms(combination[0], combination[1]):
                                result_antonyms = True
                                matched_terms = matched_terms + 'Antonyms: \'%s\' and \'%s\'' % (combination[0], combination[1])
                                break

                for combination in unique_combinations_name:
                    if combination[0].isalpha() and combination[1].isalpha():
                        if combination[0].lower() != combination[1].lower():
                            if are_antonyms(combination[0], combination[1]):
                                result_antonyms = True
                                matched_terms = matched_terms + 'Antonyms: \'%s\' and \'%s\'' % (combination[0], combination[1])
                                break

                if result_antonyms:
                        issue = Issue(self, identifier)
                        issue.additional_details = matched_terms
                        self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(type(identifier).__name__), self.__entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('F.2', error_message, ErrorSeverity.Error, False, e)

    #Override
    def analyze(self, project, entity):
        # Analyze all attributes, variables and parameters in a class
        self.project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            fields = get_all_class_fields(class_item)
            for field_item in fields:
                self.__process_identifier(field_item)

        return self.__issues
