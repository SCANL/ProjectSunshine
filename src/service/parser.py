import ctypes
import logging
import sys
from subprocess import *
from typing import Tuple
from src.common import util


class Parser:
    """
        A utility class for parsing source code files using srcML.
        Attributes:
            parsed_string (str): The parsed source code as a string.
    """

    log = logging.getLogger(__name__)

    def __init__(self):
        self.parsed_string = None

    @staticmethod
    def __run_srcml(file_path: str) -> Tuple[bytes, bytes]:
        """
            Run srcML on a source code file.
            Args:
                file_path (str): The path to the source code file.
            Returns:
                tuple: A tuple containing the parsed result (stdout) and any error messages (stderr).
        """
        directory = util.get_config_setting('srcml', 'directory')
        executable = util.get_config_setting('srcml', 'executable')
        position = '--position'

        file_path = '"'+file_path+'"'
        args = [executable, position, file_path]

        if sys.platform.startswith("win"):
            # Don't display the Windows GPF dialog if the invoked program dies.
            SEM_NOGPFAULTERRORBOX = 0x0002
            ctypes.windll.kernel32.SetErrorMode(SEM_NOGPFAULTERRORBOX)
            subprocess_flags = 0x8000000
        else:
            subprocess_flags = 0

        process = Popen(" ".join(args), stdout=PIPE, stderr=PIPE,
                        creationflags=subprocess_flags, cwd=directory)
        return process.communicate()

    def parse_file(self, file_path: str) -> bool:
        """
            Parse a source code file using srcML.
            Args:
                file_path (str): The path to the source code file.
            Returns:
                bool: True if parsing was successful, False otherwise.
        """
        result, error = self.__run_srcml(file_path)
        if len(error) == 0:
            temp = result.decode("utf-8")
            self.parsed_string = result
            return True
        else:
            return False
