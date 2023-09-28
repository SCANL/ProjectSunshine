from datetime import datetime
from src.common.enum import IdentifierType
# from src.rule.linguistic_antipattern.attribute_name_type_opposite import AttributeNameTypeOpposite


class Issue:

    def __init__(self, rule, identifier) -> None:
        self.details = rule.ISSUE_DESCRIPTION
        self.additional_details = ''
        self.category = rule.ISSUE_CATEGORY
        self.identifier_type = IdentifierType.get_type(
            type(identifier).__name__)
        self.identifier = identifier.get_fully_qualified_name()
        self.file_path = rule.entity.path
        self.analysis_datetime = datetime.now()
        self.id = rule.ID
        self.file_type = rule.entity.file_type
        self.line_number = identifier.line_number
        self.column_number = identifier.column_number
