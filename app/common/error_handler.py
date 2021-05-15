import enum
import logging
import sys
import traceback

from colorama import init, Fore, Style

logging.basicConfig(
    filename='ProjectSunshine.log',
    filemode='a',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger()


class ErrorSeverity(enum.Enum):
    Warning = 1
    Error = 2
    Critical = 3


def handle_error(module, message, severity=ErrorSeverity.Warning, exit_system=False, exception=None):
    error_message = "[%s] %s: %s. Exception: %s. Stacktrace: %s" % (
        module, severity.name, message, str(exception), traceback.format_exc())
    if exit_system:
        print(Fore.RED + Style.BRIGHT + error_message)
        logger.critical(error_message)
        sys.exit()
    else:
        print(Fore.YELLOW + Style.BRIGHT + error_message)
        logger.warning(error_message)

    print(Style.RESET_ALL)


# Required for the colored command line font
init()
