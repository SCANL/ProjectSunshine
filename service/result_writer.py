from os import path


class ResultWriter:

    def __init__(self):
        results_file = 'results.csv'
        if path.exists(results_file):
            self.results_file = open(results_file, 'a', encoding="utf-8")
        else:
            self.results_file = open(results_file, 'w', encoding="utf-8")
            self.results_file.write('FilePath,Identifier,IdentifierType,IssueCategory,IssueDetail,AnalysisDateTime\n')
            self.results_file.flush()

    def save_issue(self, issue):
        self.results_file.write('%s,%s,%s,%s,%s,%s\n' % (
            issue.file_path, issue.identifier, issue.identifier_type.name, issue.category, issue.details,
            issue.analysis_datetime.strftime("%Y-%m-%d %H:%M:%S")))
        self.results_file.flush()
        self.results_file.close()

    def save_issues(self, issues):
        for issue in issues:
            self.results_file.write('%s,%s,%s,%s,%s,%s\n' % (
                issue.file_path, issue.identifier, issue.identifier_type.name, issue.category, issue.details,
                issue.analysis_datetime.strftime("%Y-%m-%d %H:%M:%S")))
            self.results_file.flush()
        self.results_file.close()
