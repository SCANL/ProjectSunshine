from src.common.enum import GreetIssueType
from src.model.greet.greet_entity import AbstractGreetEntity
from typing import List


class GreetFunction(AbstractGreetEntity):
    """
      A class representing a greet function found in a source code file.
    """

    def __init__(self,
                 identifier: str,
                 start_line: int,
                 end_line: int,
                 start_column: int,
                 end_column: int,
                 code: str,
                 args: List[str] = None,
                 issue: GreetIssueType = GreetIssueType.CLEAR,
                 entities: List[AbstractGreetEntity] = None):
        """
        Constructor for the GreetFunction class.

        Args:
            startLine (int): The start line of the greet function.
            endLine (int): The end line of the greet function.
            startColumn (int): The start column of the greet function.
            endColumn (int): The end column of the greet function.
            string (str): The string representing the greet function.
        """
        super().__init__(identifier, start_line, end_line,
                         start_column, end_column, code=code, issue=issue)
        if args is None:
            args = []

        if entities is None:
            entities = []
        self.__entities = entities

    def getEntities(self) -> List[AbstractGreetEntity]:
        """
          Get the entities associated with the greet function.

          Returns:
            List[AbstractGreetEntity]: The entities associated with the greet function.
        """
        return self.__entities

    def __str__(self):
        return self.__code
