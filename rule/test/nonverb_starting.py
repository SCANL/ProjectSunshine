from datetime import datetime

from model.file_type import FileType
from model.identifier_type import IdentifierType
from model.issue import Issue
from nlp import pos_tag
from nlp.pos_tag import POSType


class NonVerbStarting:

    def __init__(self):
        self.__entity = None
        self.__junit = 4  # None
        self.__issues = []
        self.__issue_category = 'Starting term must be a verb'
        self.__issue_description = 'The starting term (excluding \'test\') must be a verb'

    def __get_junit_version(self):
        pass

    def __process_identifier(self, identifier):
        starting_term = identifier.name_terms[0] if identifier.name_terms[0].lower() != 'test' else ''

        if len(identifier.name_terms) > 1:
            if identifier.name_terms[0].lower() == 'test':
                starting_term = identifier.name_terms[1]

        if starting_term != '':
            tag = pos_tag.generate_tag(starting_term)
            if pos_tag.get_tag_text(tag) != POSType.Verb:
                issue = Issue()
                issue.file_path = self.__entity.path
                issue.identifier = identifier.get_fully_qualified_name()
                issue.identifier_type = IdentifierType.Method
                issue.category = self.__issue_category
                issue.details = self.__issue_description
                issue.analysis_datetime = datetime.now()
                self.__issues.append(issue)

    def analyze(self, entity):
        if entity.file_type == FileType.Test:
            self.__entity = entity
            for class_item in self.__entity.classes:
                for method_item in class_item.methods:
                    self.__process_identifier(method_item)

        return self.__issues
