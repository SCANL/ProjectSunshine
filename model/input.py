from model.file_type import FileType


class Input:

    def __init__(self, path, type, junit):
        self.path = path
        self.junit = junit
        self.entity = None

        if type == 1:
            self.type = FileType.Test
        elif type == 2:
            self.type = FileType.NonTest
        else:
            self.type = FileType.Unknown

    def set_entity(self, entity):
        self.entity = entity
