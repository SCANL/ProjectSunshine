import os
import sys
from argparse import ArgumentParser
from pathlib import Path

from analyzer import Analyzer
from common import util
from model.file_type import FileType


def run_analysis(files):
    # file_path = 'C:/Users/sheha/Downloads/GreetingTest.java'
    for file in files:
        print("Analyzing: %s ..." % (str(file)), end='', flush=True)
        file_type = FileType.Test
        a = Analyzer(str(file), file_type)
        a.analyze()
        print('done!')


def process_arguments():
    parser = ArgumentParser(util.get_config_setting('general', 'name'))
    parser.add_argument("-f", "--file", dest="arg_file", required=True,
                        help="Source file or directory to be analyzed", metavar="FILE")
    args = parser.parse_args()

    if not os.path.exists(args.arg_file):
        sys.exit("Invalid file/directory supplied")

    if os.path.isdir(args.arg_file):
        path = Path(args.arg_file)
        files = list(path.rglob('*.java'))
        if len(files) == 0:
            sys.exit("Java files not present in specified directory")
        else:
            run_analysis(files)

    if os.path.isfile(args.arg_file):
        if not args.arg_file.lower().endswith('.java'):
            sys.exit("Specified file must be a Java source file")
        else:
            run_analysis([args.arg_file])


if __name__ == '__main__':
    process_arguments()
