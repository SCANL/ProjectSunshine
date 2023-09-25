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

    @abstractclassmethod
    def analyze(self, project, entity):
        pass