import enum


class LanguageType(enum.Enum):
    """
        Enumeration of programming languages.
        Values:
            Java | CSharp | CPP
            Unknown (int): Represents an unknown programming language.
    """

    Java = 1
    CSharp = 2
    CPP = 3
    Unknown = 4

    @staticmethod
    def get_type(language: str) -> 'LanguageType':
        """
            Get the LanguageType enumeration value for a given language name.
            Args:
                language (str): The name of the programming language.
            Returns:
                LanguageType: The corresponding LanguageType enumeration value.
        """
        if language == 'Java':
            return LanguageType.Java
        elif language == 'C++':
            return LanguageType.CPP
        elif language == 'C#':
            return LanguageType.CSharp
        else:
            return LanguageType.Unknown


class FileType(enum.Enum):
    """
    Enumeration of file types.
    Values:
        Test (int): Represents a test file.
        NonTest (int): Represents a non-test file.
        Unknown (int): Represents an unknown file type.
    """

    Test = 1
    NonTest = 2
    Unknown = 3


class IdentifierType(enum.Enum):
    """
        Enumeration of identifier types.
        Values:
            Class (int): Represents a class identifier.
            Attribute (int): Represents an attribute identifier.
            Method (int): Represents a method identifier.
            Parameter (int): Represents a parameter identifier.
            Variable (int): Represents a variable identifier.
            Unknown (int): Represents an unknown identifier type.
    """

    Class = 1
    Attribute = 2
    Method = 3
    Parameter = 4
    Variable = 5
    Unknown = 6

    @staticmethod
    def get_type(identifier: str) -> 'IdentifierType':
        """
            Get the IdentifierType enumeration value for a given identifier name.
            Args:
                identifier (str): The name of the identifier.
            Returns:
                IdentifierType: The corresponding IdentifierType enumeration value.
        """

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
