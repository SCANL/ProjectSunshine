from src.common.enum import FileType, IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.model.issue import Issue
from src.common.util_parsing import get_all_class_fields

# Impacted File: Test
# Impacted identifier: Method


class TestAnnotationTest():

    ID = 'G.2'
    ISSUE_CATEGORY = 'Redundant use of \'test\' in method name'
    ISSUE_DESCRIPTION = 'Replace the term \'test\' in the method name with the \'Test\' annotation'

    def __init__(self):
        super.__init__()
        self.__junit = None

    # Override
    def __process_identifier(self, identifier):
        try:
            if self.__junit is not None and self.__junit < 4:
                return

            if identifier.name_terms[0].lower() == 'test':
                issue = Issue(self, identifier)
                self.__issues.append(issue)
        except Exception as e:
            error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                IdentifierType.get_type(
                    type(identifier).__name__), self.__entity.path, identifier.line_number,
                identifier.column_number)
            handle_error('G.2', error_message, ErrorSeverity.Error, False, e)

    # Override
    def analyze(self, project, entity):
        if entity.file_type == FileType.Test:
            # Analyze all attributes, variables and parameters in a class
            self.project = project
            self.entity = entity
            for class_item in self.entity.classes:
                fields = get_all_class_fields(class_item)
                for field_item in fields:
                    self.__process_identifier(field_item)

            return self.__issues

        return self.__issues
