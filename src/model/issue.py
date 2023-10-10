from datetime import datetime
from src.common.enum import IdentifierType


class Issue:

    def __init__(self, rule, identifier) -> None:
        __fqn = identifier.get_fully_qualified_name()

        self.details = rule.ISSUE_DESCRIPTION
        self.additional_details = ''
        self.category = rule.ISSUE_CATEGORY
        self.identifier_type = IdentifierType.get_type(
            type(identifier).__name__)
        self.identifier = __fqn if __fqn != '' else identifier.name
        self.file_path = rule.entity.path
        self.analysis_datetime = datetime.now()
        self.id = rule.ID
        self.file_type = rule.entity.file_type
        self.line_number = identifier.line_number
        self.column_number = identifier.column_number
