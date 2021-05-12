import enum
import sys

from colorama import init, Fore, Style


class ErrorSeverity(enum.Enum):
    Warning = 1
    Critical = 2


def handle_error(module, message, severity=ErrorSeverity.Warning, exit_system=False):
    error_message = "[%s] %s: %s" % (module, severity.name, message)
    if exit_system:
        print(Fore.RED + Style.BRIGHT + error_message)
        sys.exit()
    else:
        print(Fore.YELLOW + Style.BRIGHT + error_message)

    print(Style.RESET_ALL)


init()
