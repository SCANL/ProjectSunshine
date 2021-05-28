from src.service.factory import EntityFactory


class Analyzer:

    def __init__(self, project, file_path, file_type):
        self.project = project
        self.file_path = file_path
        self.file_type = file_type
        self.junit = None

    def analyze(self):
        entity = EntityFactory().construct_model(self.file_path, self.file_type, self.junit)
        if entity is None:
            return [], None

        # Get all methods in a class
        methods = []
        for class_item in entity.classes:
            for method_item in class_item.methods:
                methods.append(method_item)

        return methods, entity