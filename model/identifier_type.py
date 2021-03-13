import enum


class IdentifierType(enum.Enum):
    Class = 1
    Attribute = 2
    Method = 3
    Parameter = 4
    Variable = 5


def get_type(text):
    if text == 'Class':
        return IdentifierType.Class
    elif text == 'Attribute':
        return IdentifierType.Attribute
    elif text == 'Method':
        return IdentifierType.Method
    elif text == 'Parameter':
        return IdentifierType.Parameter
    elif text == 'Variable':
        return IdentifierType.Variable
