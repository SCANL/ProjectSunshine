from common import util
from model.entity import Entity
from service.parser import Parser


class EntityFactory:

    def __init__(self):
        self.entity = None

    def construct_model(self, source_path):
        parser = Parser()
        success = parser.parse_file(source_path)
        if success:
            self.entity = Entity()
            self.entity.srcml = parser.parsed_string
            self.entity.path = source_path
            self.entity.name = util.get_file_name(source_path)
            c = self.entity.construct_hierarchy()
        else:
            print('todo: fail')

        return self.entity
