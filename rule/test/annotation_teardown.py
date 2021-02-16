from model.identifier_type import IdentifierType
from model.issue import Issue


class AnnotationTeardown:

    def __init__(self):
        self.entity = None
        self.junit = 4#None
        self.issues = []
        self.issue_category = '\'After\' annotation not in use'
        self.issue_description = 'Utilize the \'After\' annotation for setup methods'

    def __get_junit_version(self):
        pass

    def __process_identifier(self, identifier):
        if self.junit >= 4:
            if len(identifier.name_terms) == 1 and \
                    identifier.name_terms[0].lower() == 'teardown' and \
                    'After' not in identifier.annotations:
                issue = Issue()
                issue.file_path = self.entity.path
                issue.identifier = identifier
                issue.identifier_type = IdentifierType.Method
                issue.category = self.issue_category
                issue.details = self.issue_description
                self.issues.append(issue)

    def analyze(self, entity):
        self.entity = entity
        for class_item in self.entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)
