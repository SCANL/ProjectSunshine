from abc import ABC
from src.common.enum import GreetIssueType


class AbstractGreetEntity(ABC):
    """
        An abstract base class representing a greet entity.
    """

    def __init__(self,
                 identifier: str,
                 start_line: int,
                 end_line: int,
                 start_column: int,
                 end_column: int,
                 code: str,
                 issue: GreetIssueType = GreetIssueType.CLEAR):
        """
            Constructor for the abstract greet entity.

            Args:
                startLine (int): The start line of the entity.
                endLine (int): The end line of the entity.
                startColumn (int): The start column of the entity.
                endColumn (int): The end column of the entity.
                string (str): The string extracted from the source code representing the greet entity.
        """
        self.__identifier = identifier
        self.__start_line = start_line
        self.__end_line = end_line
        self.__start_column = start_column
        self.__end_column = end_column
        self.__code = code
        self.__issue = issue

    def get_identifier(self) -> str:
        return self.__identifier

    def get_start_line(self) -> int:
        return self.__start_line

    def get_end_line(self) -> int:
        return self.__end_line

    def get_start_column(self) -> int:
        return self.__start_column

    def get_end_column(self) -> int:
        return self.__end_column

    def get_issue(self) -> GreetIssueType:
        return self.__issue

    # Function to set the issue type
    def set_issue(self, issue: GreetIssueType):
        self.__issue = issue

    def get_code(self) -> str:
        return self.__code
