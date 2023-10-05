from src.common.enum import FileType, IdentifierType, LanguageType
from src.common.error_handler import ErrorSeverity, handle_error
from src.model.issue import Issue
from src.common.util_parsing import get_all_class_fields

# Impacted File: Test
# Impacted identifier: Method


class TestAnnotationSetup():

    ID = 'X.1'
    ISSUE_CATEGORY = '\'Before\' annotation not in use'
    ISSUE_DESCRIPTION = 'Utilize the \'Before\' annotation for setup methods'

    def __init__(self):
        super.__init__()
        self.__junit = None

    # Override
    def __process_identifier(self, identifier):
        if self.__entity.language == LanguageType.Java and self.__junit is not None:
            if self.__junit >= 4:
                try:
                    if len(identifier.name_terms) == 1 and \
                            identifier.name_terms[0].lower() == 'setup' and \
                            'Before' not in identifier.annotations:
                        issue = Issue(self, identifier)
                        self.__issues.append(issue)
                except Exception as e:
                    error_message = "Error encountered processing %s in file %s [%s:%s]" % (
                        IdentifierType.get_type(
                            type(identifier).__name__), self.__entity.path, identifier.line_number,
                        identifier.column_number)
                    handle_error('X.1', error_message,
                                 ErrorSeverity.Error, False, e)

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
