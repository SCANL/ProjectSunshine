import pytest
from src.common.util import get_file_name, remove_list_nestings, get_config_setting

@pytest.mark.unit
class TestUtil:

    def test_get_config_settings(self):
        """
            TC-CMM-1.1
        """

        # Act
        name = get_config_setting("general", "name")
        
        # Assert
        assert name == "ProjectSunshine"

    def test_get_config_settings_fail_1(self, caplog):
        """
            TC-CMM-1.2
        """

        # Act
        name = get_config_setting("not existing section", "name")
        
        # Assert
        assert "not available" in caplog.text, "Not the error message expected"

    def test_get_config_settings_fail_2(self, caplog):
        """
            TC-CMM-1.3
        """

        # Act
        name = get_config_setting("general", "not existing param")
        
        # Assert
        assert "not available" in caplog.text, "Not the error message expected"

    def test_get_file_name(self):
        """
            TC-CMM-2
        """

        # Act
        name = get_file_name("file/myfile.java")
        
        # Assert
        assert name == "myfile.java", "file name different than expected, got " + \
            name + " expected myfile.java"

    def test_remove_list_nesting(self):
        """
            TC-CMM-3
            Forse questo metodo non fa esattamente quello che dice di fare
        """

        # Act
        out = remove_list_nestings([1, [2, 3, 4], 5, 6])
        
        # Assert
        assert out == [1, 5, 6], "get not the expected list " + str(out)
