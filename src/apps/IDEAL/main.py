# IDEAL (IDentifiEr AppraisaL)
from src.nlp.splitter import Splitter
from src.nlp.pos_tagger_stanford import POSTaggerStanford
from src.model.project import Project
from src.common.util import read_input
from src.common.testing_list import TestingPackage
from src.common.logger import setup_logger
from src.common.error_handler import handle_error, ErrorSeverity
from src.common import util
from result_writer import ResultWriter
from analyzer import Analyzer
from argparse import ArgumentParser
import time
import os

import collections

# The following is needed to run in the Docker
collections.Iterable = collections.abc.Iterable  # type: ignore


class Main:
    def __init__(self):
        self.files = []

        parser = ArgumentParser(util.get_config_setting('general', 'name'))
        parser.add_argument("-f", "--file", dest="arg_file", required=True,
                            help="Project Configuration file", metavar="FILE")
        args = parser.parse_args()

        if not os.path.exists(args.arg_file) or not os.path.isfile(args.arg_file):
            error_message = "Invalid Configuration File: \'%s\'\n" % str(
                args.arg_file)
            handle_error('Main', error_message, ErrorSeverity.Critical, True)

        self.project = Project(args.arg_file)
        self.files = read_input(self.project.input_file)

    def run_analysis(self):
        time_analysis_start = time.time()
        logger = setup_logger('ProjectSunshine-FileProcessed',
                              'ProjectSunshine-Processed.log')
        results = None
        tagger = POSTaggerStanford()
        splitter = Splitter()
        splitter.set_project(self.project)
        testing_package = TestingPackage()
        testing_package.set_project(self.project)
        for file in self.files:
            time_file_start = time.time()
            print("Analyzing: %s ..." % (file.path), end='', flush=True)
            a = Analyzer(self.project, file)
            results = ResultWriter(self.project.output_directory)
            results.save_issues(a.analyze())
            time_file_end = time.time()
            print('done! (%s seconds)' % str(time_file_end - time_file_start))
            logger.info('"%s"' % file.path)
        tagger.terminate()

        time_analysis_end = time.time()
        print("Analysis completed in " +
              str(time_analysis_end - time_analysis_start) + " seconds")


if __name__ == '__main__':
    main = Main()
    main.run_analysis()
