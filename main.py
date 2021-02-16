from analyzer import Analyzer
from model.file_type import FileType


def run_analysis():
    file_path = 'C:/Users/sheha/Downloads/GreetingTest.java'
    file_type = FileType.Test
    a = Analyzer(file_path, file_type)
    a.analyze()


if __name__ == '__main__':
    run_analysis()
