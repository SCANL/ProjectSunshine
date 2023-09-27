from src.common.enum import IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.model.issue import Issue
from src.rule.linguistic_antipattern.linguistic_antipattern import LinguisticAntipattern

# Impacted identifier: All
# Impacted identifier: Method
from src.nlp import term_list


class SetReturns(LinguisticAntipattern):

    ID = 'A.3'
    ISSUE_CATEGORY = '\'Set\' method returns'
    ISSUE_DESCRIPTION = 'A set method having a return type different than \'void\'.'

    def __init__(self):
        super.__init__()

    #Override
    def __process_identifier(self, identifier):
        # AntiPattern: The name starts with a set, but the method return type is not void
        try:
            if identifier.name_terms[0].lower() in term_list.get_set_terms(self.__project):
                if identifier.return_type != 'void':
                    issue = Issue(self, identifier)
                    issue.additional_details = 'Return type: %s%s' % (identifier.return_type,'(array)' if identifier.is_array else '')
                    self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(type(identifier).__name__), self.__entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('A.3', error_message, ErrorSeverity.Error, False, e)
