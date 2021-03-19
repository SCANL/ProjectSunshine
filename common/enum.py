import enum


class LanguageType(enum.Enum):
    Java = 1
    CSharp = 2
    CPP = 3
    Unknown = 4

    @staticmethod
    def get_type(language):
        if language == 'Java':
            return LanguageType.Java
        elif language == 'C++':
            return LanguageType.CPP
        elif language == 'C#':
            return LanguageType.CSharp
        else:
            return LanguageType.Unknown


class FileType(enum.Enum):
    Test = 1
    NonTest = 2
    Unknown = 3


class IdentifierType(enum.Enum):
    Class = 1
    Attribute = 2
    Method = 3
    Parameter = 4
    Variable = 5
    Unknown = 6

    @staticmethod
    def get_type(identifier):
        if identifier == 'Class':
            return IdentifierType.Class
        elif identifier == 'Attribute':
            return IdentifierType.Attribute
        elif identifier == 'Method':
            return IdentifierType.Method
        elif identifier == 'Parameter':
            return IdentifierType.Parameter
        elif identifier == 'Variable':
            return IdentifierType.Variable
        else:
            return IdentifierType.Unknown
