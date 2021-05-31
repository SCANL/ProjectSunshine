from os import path


class ResultWriter:

    def __init__(self, output_directory):
        results_file = 'IDEAL_Results.csv'
        if output_directory is not None:
            if path.exists(output_directory):
                results_file = path.join(output_directory, results_file)

        if path.exists(results_file):
            self.results_file = open(results_file, 'a', encoding="utf-8")
        else:
            self.results_file = open(results_file, 'w', encoding="utf-8")
            self.results_file.write(
                '"FilePath","FileType","Identifier","IdentifierType","LineNumber","ColumnNumber","IssueID","IssueAdditionalDetail","IssueCategory","IssueDetail","AnalysisDateTime"\n')
            self.results_file.flush()

    def save_issues(self, issues):
        for issue in issues:
            self.results_file.write('"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"\n' % (
                issue.file_path, issue.file_type.name, issue.identifier, issue.identifier_type.name, issue.line_number,
                issue.column_number, issue.id, issue.additional_details, issue.category, issue.details,
                issue.analysis_datetime.strftime("%Y-%m-%d %H:%M:%S")))
            self.results_file.flush()
        self.results_file.close()
