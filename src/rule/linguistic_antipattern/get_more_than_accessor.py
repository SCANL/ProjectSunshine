from src.common.enum import IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.util_parsing import get_all_conditional_statements
from src.model.issue import Issue
from src.rule.linguistic_antipattern.linguistic_antipattern import LinguisticAntipattern


class GetMoreThanAccessor(LinguisticAntipattern):

    ID = 'A.1'
    ISSUE_CATEGORY = '\'Get\' more than accessor'
    ISSUE_DESCRIPTION = 'A getter that performs actions other than returning the corresponding attribute.'

    def __init__(self):
        self.__class_attributes = None

    # Override
    def __process_identifier(self, identifier):
        # AntiPattern: The method name starts with 'get' AND the method is a getter for an attribute AND the method body contains conditional statements (if, loops, switch)
        try:
            if identifier.name_terms[0].lower() == 'get' and (identifier.specifier == 'public' or identifier.specifier == 'protected'):
                for attribute in self.__class_attributes:
                    if identifier.name[3:].lower() == (attribute.name.lower()) and identifier.return_type == attribute.type:
                        _, conditional_statements_total = get_all_conditional_statements(
                            identifier.source)
                        if conditional_statements_total != 0:
                            issue = Issue(self, identifier)
                            issue.additional_details = 'Count of conditional statements: %s' % conditional_statements_total
                            self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(
                    type(identifier).__name__), self.__entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('A.1', error_message, ErrorSeverity.Error, False, e)

    # Override
    def analyze(self, project, entity):
        # Analyze all methods in a class
        self.project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            self.__class_attributes = class_item.attributes
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues
