import itertools
from typing import cast

from src.common.enum import IdentifierType, LanguageType
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.util_parsing import is_test_method
from src.model.entity import Entity
from src.model.issue import Issue
from src.model.project import Project
from src.nlp.related_terms import are_antonyms
from src.rule.linguistic_antipattern.linguistic_antipattern import LinguisticAntipattern


class MethodNameReturnOpposite(LinguisticAntipattern):

    ID = 'C.1'
    ISSUE_CATEGORY = 'Method name and return type are opposite'
    ISSUE_DESCRIPTION = 'The intent of the method suggested by its name is in contradiction with what it returns.'

    def __init__(self):
        super.__init__()  # type: ignore

    # Override
    def __process_identifier(self, identifier):
        project = cast(Project, self.project)
        entity = cast(Entity, self.__entity)
        path = cast(str, cast(Entity, self.__entity).path)

        # AntiPattern: The method name and return type name contain antonyms
        try:
            if not is_test_method(project, entity, identifier):
                matched_terms = 'Return Type: %s%s;' % (
                    identifier.return_type, '(array)' if identifier.is_array else '')
                if identifier.name_terms[0] == 'get':
                    unique_combinations = list(itertools.product(
                        identifier.name_terms[1:], identifier.type_terms))
                else:
                    unique_combinations = list(itertools.product(
                        identifier.name_terms, identifier.type_terms))

                result_antonyms = False
                for combination in unique_combinations:
                    if combination[0].isalpha() and combination[1].isalpha() and combination[0].lower() != combination[1].lower() and are_antonyms(combination[0], combination[1]):
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
                    type(identifier).__name__), path, identifier.line_number,
                identifier.column_number)
            handle_error('C.1', error_message, ErrorSeverity.Error, False, e)
