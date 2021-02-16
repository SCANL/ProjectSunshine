import enum


class IdentifierType(enum.Enum):
    Class = 1
    Attribute = 2
    Method = 3
    Parameter = 4
    Variable = 5
