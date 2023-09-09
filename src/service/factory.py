from src.common import util
from src.common.error_handler import handle_error, ErrorSeverity
from src.model.entity import Entity
from src.service.parser import Parser


class EntityFactory:
    """
        A factory class for constructing Entity objects from source code files.
        Attributes:
            None
    """

    def __init__(self):
        self.entity: Entity = None  # type: ignore

    def construct_model(self, source_path: str, file_type, junit: bool) -> Entity:
        """
            Construct an Entity object from a source code file.
            Args:
                source_path (str): The path to the source code file.
                file_type (str): The type of the source code file.
                junit (bool): Whether the source code is related to JUnit testing.
            Returns:
                Entity: The constructed Entity object.
            Note:
                VSCode complains about types because of `Entity`'s constructor setting all attributes to None,
                and it is useless since that is standard Python behavior.
        """

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
            error_message = "Issue encountered in parsing file: \'%s\'" % str(
                source_path)
            handle_error('EntityFactory', error_message,
                         ErrorSeverity.Critical, False)

        return self.entity
