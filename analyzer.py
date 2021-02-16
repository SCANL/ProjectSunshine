from model.file_type import FileType
from rule.test.annotation_setup import AnnotationSetup
from rule.test.annotation_teardown import AnnotationTeardown
from rule.test.annotation_test import AnnotationTest
from service.factory import EntityFactory
from service.result_writer import ResultWriter


class Analyzer:

    def __init__(self, file_path, file_type):
        self.file_path = file_path
        self.file_type = file_type
        self.junit = None
        self.rules = [AnnotationTest(), AnnotationSetup(), AnnotationTeardown()]
        self.issues = []

    def analyze(self):
        if self.file_type == FileType.Test:
            entity = EntityFactory().construct_model(self.file_path)
            for rule in self.rules:
                issue_list = rule.analyze(entity)
                if issue_list is not None:
                    self.issues.append(issue_list)

        results = ResultWriter()
        concat_issues = [j for i in self.issues for j in i]
        results.save_issues(concat_issues)
