import enum
import sys
import traceback

from colorama import init, Fore, Style


from src.common.logger import setup_logger

logger = setup_logger('ProjectSunshine-Problem', 'ProjectSunshine-Problem.log')


class ErrorSeverity(enum.Enum):
    """
        Enumeration representing error severity levels.
        Values:
            Warning (int): Represents a warning severity.
            Error (int): Represents an error severity.
            Critical (int): Represents a critical severity.
    """
    Warning = 1
    Error = 2
    Critical = 3


def handle_error(module: str, message: str, severity: ErrorSeverity = ErrorSeverity.Warning, exit_system: bool = False, exception=None) -> None:
    """
        Handle and log error messages with specified severity.

        Args:
            module (str): The name of the module where the error occurred.
            message (str): The error message to be logged.
            severity (ErrorSeverity): The severity level of the error (default is ErrorSeverity.Warning).
            exit_system (bool): Whether to exit the system after logging the error (default is False).
            exception (Exception or None): Optional exception associated with the error (default is None).
    """
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
