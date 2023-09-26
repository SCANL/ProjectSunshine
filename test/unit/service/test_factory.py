import pytest
from unittest.mock import patch
from src.service.factory import EntityFactory


@pytest.mark.unit
class TestFactory:
    """
        Test case specification for these test cases can be found here:
        https://t.ly/0CCGA
    """

    # util.get_file_name mock ?
    @pytest.fixture
    def temp_input_file(self, tmpdir):
        content = '''
        public class Main {
            public static void main(String[] args) {
                System.out.println("Hello World!");
            }
        }
        '''
        file_path = tmpdir.join("temp_input.java")
        file_path.write(content)
        yield file_path
        file_path.remove()

    @pytest.fixture
    def mock_parse_file(self, mocker):
        """
            Mock for src.service.parser.Parser.parse_file (used in src.service.factory.EntityFactory.construct_model)
        """
        return mocker.patch("src.service.parser.Parser.parse_file")

    @pytest.fixture
    def mock_construct_hierarchy(self, mocker):
        """
            src.model.entity.Entity.construct_hierarchy (used in src.service.factory.EntityFactory.construct_model)
        """
        return mocker.patch("src.model.entity.Entity.construct_hierarchy")

    def test_construct_model_with_invalid_input(self, mock_parse_file):
        """
            ID: TC-SRV-2.1
        """
        mock_parse_file.return_value = False
        factory = EntityFactory()
        invalid_file_path = "path/to/invalid/file.java"
        assert factory.construct_model(invalid_file_path, "", False) == None

    def test_construct_model_with_valid_input(self, temp_input_file, mock_parse_file, mock_construct_hierarchy):
        """
            ID: TC-SRV-2.2
        """
        mock_parse_file.return_value = True
        mock_construct_hierarchy.return_value = []

        factory = EntityFactory()

        valid_file_path = str(temp_input_file)
        factory.construct_model(valid_file_path, "", False)

        assert factory.entity is not None
