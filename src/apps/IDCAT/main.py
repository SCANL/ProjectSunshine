# IDCAT (IDentifier CATalog)

import os
import time
from argparse import ArgumentParser
from pathlib import Path

import pandas

from src.apps.IDCAT.analyzer import Analyzer
from src.apps.IDCAT.result_writer import ResultWriter
from src.common import util
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.logger import setup_logger
from src.common.testing_list import TestingPackage
from src.common.util import read_input
from src.model.input import Input
from src.model.project import Project
from src.nlp.pos_tagger_stanford import POSTaggerStanford
from src.nlp.splitter import Splitter
from src.service.factory import EntityFactory


class Main:
    def __init__(self):
        self.project = None

        parser = ArgumentParser(util.get_config_setting('general', 'name'))
        parser.add_argument("-f", "--file", dest="arg_file", required=True,
                            help="Project Configuration file", metavar="FILE")
        args = parser.parse_args()

        if not os.path.exists(args.arg_file) or not os.path.isfile(args.arg_file):
            error_message = "Invalid Configuration File: \'%s\'" % str(args.arg_file)
            handle_error('Main', error_message, ErrorSeverity.Critical, True)

        self.project = Project(args.arg_file)

        print("Identifying source files: ...", end='', flush=True)
        time_file_start = time.time()
        self.files = read_input(self.project.input_file)
        time_file_end = time.time()
        print('done! (%s seconds)' % str(time_file_end - time_file_start))
        print('Files identified: %s ' % str(len(self.files)))

    def run_analysis(self):
        time_analysis_start = time.time()
        logger = setup_logger('ProjectSunshine-FileProcessed', 'ProjectSunshine-Processed.log')

        results = None
        tagger = POSTaggerStanford()
        splitter = Splitter()
        splitter.set_project(self.project)
        testing_package = TestingPackage()
        testing_package.set_project(self.project)
        total_files = len(self.files)
        for i in range(total_files):
            file = self.files[i]
            time_file_start = time.time()
            print("[%s of %s (%% %s)]Analyzing: %s ..." % (str(i), str(total_files), str(i / total_files), file.path), end='', flush=True)
            a = Analyzer(self.project, file.path, file.type)
            methods, entity = a.analyze()
            if entity is not None:
                results = ResultWriter(self.project)
                results.save_issues(entity, methods)
                time_file_end = time.time()
                print('done! (%s seconds)' %str(time_file_end - time_file_start))
                logger.info('"%s"'%file.path)
        tagger.terminate()

        time_analysis_end = time.time()
        print("Analysis completed in " + str(time_analysis_end - time_analysis_start) + " seconds")


if __name__ == '__main__':
    main = Main()
    main.run_analysis()
