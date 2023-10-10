from os import path
from typing import cast

from src.common.enum import GreetIssueType
from src.model.greet.greet_function import GreetFunction
from src.model.greet.greet_issue import GreetIssue
from src.rule.linguistic_antipattern.method_signature_comment_opposite import MethodSignatureCommentOpposite
from src.rule.linguistic_antipattern.attribute_signature_comment_opposite import AttributeSignatureCommentOpposite
from src.rule.linguistic_antipattern.not_implemented_condition import NotImplementedCondition


class ResultWriter:

    def __init__(self, output_directory):
        results_file = 'IDEAL_Results.csv'
        if output_directory is not None and path.exists(output_directory):
            results_file = path.join(output_directory, results_file)

        if path.exists(results_file):
            self.results_file = open(results_file, 'a', encoding="utf-8")
        else:
            self.results_file = open(results_file, 'w', encoding="utf-8")
            self.results_file.write(
                '"FilePath","FileType","Identifier","IdentifierType","LineNumber","ColumnNumber","IssueID","IssueAdditionalDetail","IssueCategory","IssueDetail","AnalysisDateTime"\n')
            self.results_file.flush()

    def __get_issue_details(self, issue: GreetIssueType):
        if issue == GreetIssueType.ATTRIBUTE_OPPOSITE_COMMENT:
            return AttributeSignatureCommentOpposite()
        elif issue == GreetIssueType.METHOD_OPPOSITE_COMMENT:
            return MethodSignatureCommentOpposite()
        elif issue == GreetIssueType.NOT_IMPL_CONDITION:
            return NotImplementedCondition()

    def save_issues(self, issues):
        for issue in issues:
            if isinstance(issue, GreetIssue):

                if isinstance(issue.get_entity(), GreetFunction):
                    attribute_type = "Method"
                else:
                    attribute_type = "Attribute"

                __issue_details = cast(AttributeSignatureCommentOpposite, self.__get_issue_details(
                    issue.get_issue_type()))

                self.results_file.write('"%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s"\n' % (
                    issue.get_file_path(),
                    "NonTest",
                    issue.get_entity().get_identifier(),
                    attribute_type,
                    issue.get_entity().get_start_line(),
                    issue.get_entity().get_start_column(),
                    __issue_details.ID,
                    "",
                    __issue_details.ISSUE_CATEGORY,
                    __issue_details.ISSUE_DESCRIPTION,
                    issue.get_analysis_datetime().strftime("%Y-%m-%d %H:%M:%S")
                ))
            else:
                self.results_file.write('"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"\n' % (
                    issue.file_path, issue.file_type.name, issue.identifier, issue.identifier_type.name, issue.line_number,
                    issue.column_number, issue.id, issue.additional_details, issue.category, issue.details,
                    issue.analysis_datetime.strftime("%Y-%m-%d %H:%M:%S")))
                self.results_file.flush()
        self.results_file.close()
