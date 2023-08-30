import pytest
from src.common.util import get_file_name, remove_list_nestings, get_config_setting


@pytest.mark.unit
class TestUtil:

    def test_get_file_name(self):
        """
            TC-CMM-2 (integration maybe, 1 line of code)
        """

        # Act
        name = get_file_name("file/myfile.java")

        # Assert
        assert name == "myfile.java", "file name different than expected, got " + \
            name + " expected myfile.java"

    def test_remove_list_nesting(self):
        """
            TC-CMM-3
            TODO: check if the original function is doing what it should really do 🤔
        """

        # Act
        out = remove_list_nestings([1, [2, 3, 4], 5, 6])

        # Assert
        assert out == [1, 5, 6], "get not the expected list " + str(out)
