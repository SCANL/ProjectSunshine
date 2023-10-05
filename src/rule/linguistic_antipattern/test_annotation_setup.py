from src.common.enum import FileType, IdentifierType, LanguageType
from src.common.error_handler import ErrorSeverity, handle_error
from src.model.issue import Issue

# Impacted File: Test
# Impacted identifier: Method


class TestAnnotationSetup(LinguisticAntipattern):

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
            self.__junit = project.junit_version
            LinguisticAntipattern.analyze(self, project, entity)

        return self.__issues
