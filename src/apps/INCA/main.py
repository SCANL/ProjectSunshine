# INCA (IdeNtifier CAtalog)

import os
import time
from argparse import ArgumentParser

from src.common import util
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.logger import setup_logger
from src.model.project import Project


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

    def run_analysis(self):
        time_analysis_start = time.time()
        logger = setup_logger('ProjectSunshine-FileProcessed', 'ProjectSunshine-Processed.log')

        time_analysis_end = time.time()
        print("Analysis completed in " + str(time_analysis_end - time_analysis_start) + " seconds")


if __name__ == '__main__':
    main = Main()
    main.run_analysis()
