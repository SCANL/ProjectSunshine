from src.model.greet.greet_entity import AbstractGreetEntity
from typing import List


class GreetClass(AbstractGreetEntity):
    """
        Class that represents a class found in a source code file.
    """

    def __init__(self, name: str, entities: List[AbstractGreetEntity] = []):
        """
            Constructor for a GreetClass.

            Parameters:
            - name (str): The name of the class.
            - entities (List[AbstractGreetEntity], optional): A list of entities contained in the class.
                Default is an empty list.

        """
        self.__name = name
        self.__entities: List[AbstractGreetEntity] = entities

    def get_name(self):
        return self.__name

    def get_entities(self):
        return self.__entities
