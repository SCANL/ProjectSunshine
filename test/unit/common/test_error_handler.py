import pytest
from src.common.error_handler import handle_error, ErrorSeverity

@pytest.mark.unit
class TestErrorHandler:

    @pytest.fixture
    def mock_logger(self, mocker):
        return mocker.patch('src.common.error_handler.logger')
    
    @pytest.fixture
    def mock_sys(self, mocker):
        return mocker.patch('src.common.error_handler.sys') 

    def test_handle_error_critical(self, mock_sys, mock_logger):
        """
            TC-CMM-5.1
        """

        # Arrange
        module = 'test_module'
        message = 'test_message'
        severity = ErrorSeverity.Critical
        exception = Exception('test_exception')

        # Act
        handle_error(module, message, severity, True, exception)

        # Assert
        mock_logger.critical.assert_called_once_with(
            f"[{module}] {severity.name}: {message}. Exception: {str(exception)}. Stacktrace: NoneType: None\n"
        )
        mock_sys.exit.assert_called_once()


    def test_handle_error_warning(self, mock_sys, mock_logger):
        """
            TC-CMM-5.2
        """

        # Arrange
        module = 'test_module'
        message = 'test_message'
        severity = ErrorSeverity.Warning
        exception = Exception('test_exception')

        # Act
        handle_error(module, message, severity, False, exception)

        # Assert
        mock_logger.warning.assert_called_once_with(
            f"[{module}] {severity.name}: {message}. Exception: {str(exception)}. Stacktrace: NoneType: None\n"
        )
        mock_sys.exit.assert_not_called()

    def test_handle_error_no_exception(self, mock_sys, mock_logger):
        """
            TC-CMM-5.3
        """

        # Arrange
        module = 'test_module'
        message = 'test_message'
        severity = ErrorSeverity.Error

        # Act
        handle_error(module, message, severity)

        # Assert
        mock_logger.warning.assert_called_once_with(
            f"[{module}] {severity.name}: {message}. Exception: None. Stacktrace: NoneType: None\n"
        )
        mock_sys.exit.assert_not_called()
