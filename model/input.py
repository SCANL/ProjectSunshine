from common.enum import FileType


class Input:

    def __init__(self, path, type, junit):
        self.path = path
        self.junit = junit
        self.entity = None
        self.type = type

    def set_entity(self, entity):
        self.entity = entity
