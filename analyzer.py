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
                self.issues.append(rule.analyze(entity))

        results = ResultWriter()
        for issue in self.issues:
            if type(issue) is not type(None):
                for sub_issue in issue:
                    results.save_issue(sub_issue)
