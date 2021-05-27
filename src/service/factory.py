from src.common import util
from src.common.error_handler import handle_error, ErrorSeverity
from src.model.entity import Entity
from src.service.parser import Parser


class EntityFactory:

    def __init__(self):
        self.entity = None

    def construct_model(self, source_path, file_type, junit):
        parser = Parser()
        success = parser.parse_file(source_path)
        if success:
            self.entity = Entity()
            self.entity.srcml = parser.parsed_string
            self.entity.path = source_path
            self.entity.name = util.get_file_name(source_path)
            self.entity.set_file_type(file_type)
            self.entity.junit = junit
            c = self.entity.construct_hierarchy()
        else:
            error_message = "Issue encountered in parsing file: \'%s\'" % str(source_path)
            handle_error('EntityFactory', error_message, ErrorSeverity.Critical, False)

        return self.entity
