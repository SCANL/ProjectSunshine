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
