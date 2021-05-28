from os import path

from src.common.util_parsing import is_test_method


class ResultWriter:

    def __init__(self, project):
        self.project = project
        output_directory = project.output_directory
        results_file = 'IDCAT_Results.csv'

        if output_directory is not None:
            if path.exists(output_directory):
                results_file = path.join(output_directory, results_file)

        if path.exists(results_file):
            self.results_file = open(results_file, 'a', encoding="utf-8")
        else:
            self.results_file = open(results_file, 'w', encoding="utf-8")
            self.results_file.write(
                '"FilePath","FileType","MethodName","MethodName_FirstTerm","ReturnType","IsTestMethod","ParameterCount","LineNumber","ColumnNumber"\n')
            self.results_file.flush()

    def save_issues(self, entity, methods):
        for method in methods:
            is_test = is_test_method(self.project, entity, method)
            self.results_file.write('"%s","%s","%s","%s","%s","%s","%s","%s","%s"\n' % (
                entity.path, entity.file_type, method.name, method.name_terms[0], method.return_type,
                is_test, str(len(method.parameters)), method.line_number, method.column_number))
            self.results_file.flush()
        self.results_file.close()
