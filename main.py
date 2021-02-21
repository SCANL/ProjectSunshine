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


def read_input(path):
    input_data = pandas.read_csv(path)
    if len(input_data) == 0:
        sys.exit("Input CSV file cannot be empty")

    files = []
    for i, item in input_data.iterrows():
        path = str(Path(item[0]))
        if os.path.isfile(path):
            if path.lower().endswith('.java'):
                input_item = Input(path, item[1], item[2])
                files.append(input_item)

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
