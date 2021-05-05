import os
import sys
from argparse import ArgumentParser
from pathlib import Path

import pandas

from analyzer import Analyzer
from common import util
from model.input import Input
from service.result_writer import ResultWriter


def run_analysis(files):
    results = None
    for file in files:
        print("Analyzing: %s ..." % (file.path), end='', flush=True)
        a = Analyzer(file.path, file.type)
        results = ResultWriter()
        results.save_issues(a.analyze())
        print('done!')


def read_input(path_string):
    input_data = pandas.read_csv(path_string)
    if len(input_data) == 0:
        sys.exit("Input CSV file cannot be empty")

    files = []
    file_extensions = util.get_supported_file_extensions()
    for i, item in input_data.iterrows():
        path = Path(item[0])
        path_string = str(path)

        if os.path.isdir(path_string):
            source_files = [p for p in path.rglob('*') if p.suffix in file_extensions]
            for file in source_files:
                input_item = Input(str(file), item[1], item[2])
                files.append(input_item)

        elif os.path.isfile(path_string):
            if path_string.lower().endswith(tuple(file_extensions)):
                input_item = Input(path_string, item[1], item[2])
                files.append(input_item)
        else:
            sys.exit("Invalid files provided in input CSV file: %s" %path_string)

    if len(files) == 0:
        sys.exit("Invalid files provided in input CSV file")

    run_analysis(files)


def process_arguments():
    parser = ArgumentParser(util.get_config_setting('general', 'name'))
    parser.add_argument("-f", "--file", dest="arg_file", required=True,
                        help="Input CSV file", metavar="FILE")
    args = parser.parse_args()

    if not os.path.exists(args.arg_file):
        sys.exit("Invalid file supplied")

    read_input(args.arg_file)


if __name__ == '__main__':
    process_arguments()
