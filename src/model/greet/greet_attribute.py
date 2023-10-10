from src.common.enum import GreetIssueType
from src.model.greet.greet_entity import AbstractGreetEntity


class GreetAttribute(AbstractGreetEntity):
    """
        A class representing a greet attribute.
    """

    def __init__(self,
                 identifier: str,
                 start_line: int,
                 end_line: int,
                 start_column: int,
                 end_column: int,
                 code: str,
                 issue: GreetIssueType = GreetIssueType.CLEAR,
                 value: str = '',
                 comment: str = ''):
        """
            Constructor for the GreetAttribute class.

            Args:
                identifier (str): The identifier of the attribute.
                startLine (int): The start line of the attribute.
                endLine (int): The end line of the attribute.
                startColumn (int): The start column of the attribute.
                endColumn (int): The end column of the attribute.
                string (str): The string representing the attribute.
                value (str): The value assigned to the attribute.
                comment (str, optional): Optional comment associated with the attribute. Defaults to ''.
        """
        super().__init__(identifier, start_line, end_line,
                         start_column, end_column, code=code, issue=issue)
        self.__value = value
        self.__comment = comment

    def get_code(self) -> str:
        """
            Get the string representing the greet attribute.

            Returns:
                str: The string representing the greet attribute.
        """
        return f"""\"\"\"
{self.__comment.strip()}
\"\"\"
{self._AbstractGreetEntity__identifier} = {self.__value}
"""
