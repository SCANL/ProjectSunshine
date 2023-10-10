from src.common.enum import LanguageType


class Input:

    def __init__(self, path, type, junit, language: LanguageType):
        self.path = path
        self.junit = junit
        self.entity = None
        self.type = type
        self.language = language

    def set_entity(self, entity):
        self.entity = entity
