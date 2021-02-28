from rule.linguistic_antipattern.get_no_return import GetNoReturn
from rule.test.annotation_setup import AnnotationSetup
from rule.test.annotation_teardown import AnnotationTeardown
from rule.test.annotation_test import AnnotationTest
from rule.test.nonverb_starting import NonVerbStarting
from service.factory import EntityFactory


class Analyzer:

    def __init__(self, file_path, file_type):
        self.file_path = file_path
        self.file_type = file_type
        self.junit = None
        self.rules = [
            GetNoReturn(),
            AnnotationTest(),
            AnnotationSetup(),
            AnnotationTeardown(),
            NonVerbStarting()
        ]
        self.issues = []

    def analyze(self):
        entity = EntityFactory().construct_model(self.file_path)
        entity.set_file_type(self.file_type)
        entity.junit = self.junit

        for rule in self.rules:
            issue_list = rule.analyze(entity)
            if issue_list is not None:
                self.issues.append(issue_list)

        concat_issues = [j for i in self.issues for j in i]
        return concat_issues
