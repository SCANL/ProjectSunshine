import pytest
import os
import src.common.util as util
from src.common.util import get_config_setting

__current_dir = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.realpath(__current_dir))

CONFIG_VALUE_NAME = "ProjectSunshine"


@pytest.fixture(scope="module", autouse=True)
def setup():
    """
        This fixture is used to create a temp directory where the config file will be stored
        and to remove it after the tests are done.
    """
    # create a temp directory where the config files will be stored
    os.mkdir(f'{root}/integration/temp/')

    # write the config file in the directory
    with open(f'{root}/integration/temp/config.txt', 'w') as f:
        f.write(f"[general]\nname = {CONFIG_VALUE_NAME}\n")

    yield

    # remove the temp directory
    os.remove(f'{root}/integration/temp/config.txt')
    os.rmdir(f'{root}/integration/temp/')


@pytest.mark.integration
class TestItCommon:

    @pytest.fixture
    def mock_os_path_join(self, monkeypatch):
        """
            This fixture is used to mock the os.path.join function so that it returns the path of the config created for this test case. 
        """

        def mock_join(*args):
            # Replace with the desired mocked path
            return f"{root}/integration/temp/config.txt"

        # Apply the monkeypatch to os.path.join
        monkeypatch.setattr(os.path, 'join', mock_join)

    def test_get_config_setting(self, mock_os_path_join):
        """
            TC-CMM-1.1
        """
        name = get_config_setting("general", "name")
        assert name == CONFIG_VALUE_NAME

    def test_get_config_setting_fail_1(self, mock_os_path_join, caplog):
        """
            TC-CMM-1.2
        """
        get_config_setting("not existing section", "name")
        assert "not available" in caplog.text, "Not the error message expected"

    def test_get_config_setting_fail_2(self, mock_os_path_join, caplog):
        """
            TC-CMM-1.3
        """
        get_config_setting("general", "not existing param")
        assert "not available" in caplog.text, "Not the error message expected"

    