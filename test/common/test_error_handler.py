import pytest
from src.common.error_handler import handle_error, ErrorSeverity

class TestErrorHandler:

    def test_error_handler(self, capfd):
        handle_error("util.py", "error in main process", ErrorSeverity.Warning)
        out, err = capfd.readouterr()
        assert "[util.py] Warning: error in main process. Exception: None. Stacktrace: NoneType: None" in out, "not the error we expecteed"

    def test_error_handler_with_system_exit(self, capfd):
        with pytest.raises(SystemExit):
            handle_error("util.py", "error in main process", ErrorSeverity.Warning, True)
        out, err = capfd.readouterr()
        assert "[util.py] Warning: error in main process. Exception: None. Stacktrace: NoneType: None" in out, "not the error we expecteed"

    def test_error_handler_with_exception(self, capfd):
        handle_error("util.py", "error in main process", ErrorSeverity.Critical, False, Exception)
        out, err = capfd.readouterr()
        assert "[util.py] Critical: error in main process. Exception: <class 'Exception'>. Stacktrace: NoneType: None" in out, "not the error we expecteed "     