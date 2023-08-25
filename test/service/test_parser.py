import pytest
from unittest.mock import patch
from src.service.parser import Parser


def new_run_srcml_for_valid_input(*args, **kwargs):
    return b'', ""


def new_run_srcml_for_invalid_input(*args, **kwargs):
    return b'', "error"


def parser_init(*args, **kwargs):
    pass


class TestParser:
    """
        Test case specification for these test cases can be found here:
        https://t.ly/0CCGA
    """

    @pytest.fixture
    def temp_input_file(self, tmpdir):
        content = '''
        public class Main {
            public static void main(String[] args) {
                System.out.println("Ciao, mondo!");
            }
        }
        '''
        file_path = tmpdir.join("temp_input.java")
        file_path.write(content)
        yield file_path
        file_path.remove()

    def test_parse_file_with_invalid_input(self):
        """
            ID: TC-SRV-3.1
        """
        with patch.object(Parser, '_Parser__run_srcml', new=new_run_srcml_for_invalid_input):
            with patch.object(Parser, '__init__', new=parser_init):
                parser = Parser()
                result = parser.parse_file("path/to/invalid/file.java")

        assert result == False

    def test_parse_file_with_valid_input(self, temp_input_file):
        """
            ID: TC-SRV-3.2
        """
        with patch.object(Parser, '_Parser__run_srcml', new=new_run_srcml_for_valid_input):
            with patch.object(Parser, '__init__', new=parser_init):
                parser = Parser()
                valid_file_path = str(temp_input_file)
                result = parser.parse_file(valid_file_path)

        assert result == True

    def test_run_srcml_invalid(self):
        """
            ID: TC-SRV-4.1
        """
        invalid_file_path = "path/to/invalid/file.java"
        parser = Parser()
        result = parser._Parser__run_srcml(invalid_file_path)

        expected_stdout = b''
        expected_stderr = b'srcml: Unable to open file path/to/invalid/file.java\r\n'

        assert result == (expected_stdout, expected_stderr)

    def test_run_srcml_valid(self, temp_input_file):
        """
            ID: TC-SRV-4.2
        """
        valid_file_path = str(temp_input_file)
        parser = Parser()
        result = parser._Parser__run_srcml(valid_file_path)
        if isinstance(result, bytes):
            result_string = result.decode("utf-8")
        else:
            result_string = str(result)
        assert result_string.startswith(
            '(b\'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
