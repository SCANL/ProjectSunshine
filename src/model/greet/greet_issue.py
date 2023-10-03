from src.common.enum import GreetIssueType
from src.model.greet.greet_entity import AbstractGreetEntity
from src.model.input import Input


class GreetIssue:

    def __init__(self, entity: AbstractGreetEntity, issue_type: GreetIssueType, file_path: str):
        self.__entity = entity
        self.__issue_type = issue_type
        self.__file_path = file_path

    def get_entity(self):
        return self.__entity

    def get_issue_type(self):
        return self.__issue_type

    def get_file_path(self):
        return self.__file_path
