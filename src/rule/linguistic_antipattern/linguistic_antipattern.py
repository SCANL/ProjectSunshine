from abc import ABC, abstractclassmethod

class LinguisticAntipattern(ABC):

    ID = ''
    ISSUE_CATEGORY = ''
    ISSUE_DESCRIPTION = ''

    def __init__(self) -> None:
        super().__init__()
        self.__entity = None
        self.__project = None
        self.__issues = []

    @property
    def entity(self):
        return self.__entity
    
    @entity.setter
    def entity(self, value):
        self.__entity = value

    @property
    def project(self):
        return self.__project
    
    @project.setter
    def project(self, value):
        self.__project = value

    @property
    def issues(self):
        return self.__issues
    
    @issues.setter
    def project(self, value):
        self.__issues= value

    @abstractclassmethod
    def __process_identifier(self, identifier):
        pass

    def analyze(self, project, entity):
        # Analyze all methods in a class
        self.__project = project
        self.__entity = entity
        for class_item in self.__entity.classes:
            for method_item in class_item.methods:
                self.__process_identifier(method_item)

        return self.__issues