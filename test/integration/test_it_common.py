import pytest, os, shutil
from src.model.project import Project
from src.common.testing_list import get_test_method_annotations, get_testing_packages, get_null_check_test_method
from src.common.enum import LanguageType
import src.common.util as util
from src.common.util import get_config_setting

__current_dir = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.realpath(__current_dir))

CONFIG_VALUE_NAME = "ProjectSunshine"
PATH = "./test/temp/"


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

class CommonTestUtils: 

    def __create_test_dir(self):
        """
            this function creates the folder where the temporary test files will be stored
        """
        if not os.path.exists(PATH):
            os.mkdir(PATH)

    def delete_files(self):
        """
            this function deletes the temporary folder created for testing with its contents
        """
        shutil.rmtree(PATH)

    def create_config_file(self,
                            java_testing_packages = "[]",
                            csharp_testing_packages = "[]",
                            java_null_check_methods = "[]",
                            csharp_null_check_methods = "[]", 
                            java_test_annotations = "[]", 
                            csharp_test_annotations = "[]"):
        """
            this function creates the configuration files needed to run the tests
            Args:
                java_testing_packages: The list of custom packages used for testing a project written in java code to be included in the configuration file
                csharp_testing_packages: The list of custom packages used for testing a project written in C# code to be included in the configuration file
                java_null_check_methods: The list of custom annotations used to describe whether or not a method returns a null value in a project written in Java code
                csharp_null_check_methods: The list of custom annotations used to describe whether or not a method returns a null value in a project written in C# code
                java_test_annotations: The list of custom annotations used to identify a test method in a project written in java code
                csharp_test_annotations: The list of custom annotations used to identify a test method in a project written in C# code
        """

        self.__create_test_dir()

        # creates the custom_code.txt file, inside which the custom packages and annotations used by the user in the project will be inserted
        with open(f"{PATH}custom_code.txt", "a", encoding='utf-8') as code_file:
            code_file.write("[DataTypes]\n")
            code_file.write("csharp_custom_collection_data_types = []\n")
            code_file.write("\n[Test]\n")
            code_file.write(f"java_custom_testing_packages = {java_testing_packages}\n")
            code_file.write(f"csharp_custom_testing_packages = {csharp_testing_packages}\n")
            code_file.write(f"java_custom_null_check_test_methods = {java_null_check_methods}\n")
            code_file.write(f"csharp_custom_null_check_test_methods = {csharp_null_check_methods}\n")
            code_file.write(f"java_custom_test_method_annotation = {java_test_annotations}\n")
            code_file.write(f"csharp_custom_test_method_annotation = {csharp_test_annotations}\n")

        # create the project1.config file, in which the path to our file with the custom code will be inserted
        with open(f"{PATH}project1.config", "a", encoding="utf-8") as config:
            config.write("[Files]\n")
            config.write("input_file=./src/apps/IDEAL/input.csv\n")
            config.write("output_directory=./src/apps/IDEAL\n")
            config.write("custom_code=" + PATH + "custom_code.txt\n")
            config.write("custom_terms=custom_terms.txt\n")

            config.write("[Properties]\n")
            config.write("junit_version=4\n")


utils = CommonTestUtils()

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

    """
    ------------------------ testing_list.py ------------------------------------
    """

    # get_test_method_annotations

    @pytest.fixture
    def mock_project(self):
        """
            The fixture creates a project instance using a configuration file without any kind of custom term
        """

        utils.create_config_file()

        if os.path.exists(f"{PATH}project1.config"):
            yield Project(f"{PATH}project1.config")
        else:
            yield     

        utils.delete_files()   

    def test_get_test_method_annotations_java(self, mock_project):
        """
            TC-CMM-11.1
        """
        
        # Act
        annotations = get_test_method_annotations(mock_project, LanguageType.Java)
        
        # Assert
        assert annotations == ['Test']

    @pytest.fixture
    def mock_project_with_custom_java(self):
        """
            The fixture creates a project instance using a configuration file containing custom annotations for projects written in Java code
        """

        utils.create_config_file(java_test_annotations="[\"UnitTest\", \"IntegrationTest\", \"SystemTest\"]")

        if os.path.exists(f"{PATH}project1.config"):
            yield Project(f"{PATH}project1.config")
        else:
            yield

        utils.delete_files()

    def test_get_test_method_annotations_with_custom_java(self, mock_project_with_custom_java):
        """
            TC-CMM-11.2
        """
        
        # Act
        annotations = get_test_method_annotations(mock_project_with_custom_java, LanguageType.Java)
        
        # Assert
        assert annotations == ['Test', 'UnitTest', 'IntegrationTest', 'SystemTest']

    def test_get_test_method_annotations_csharp(self, mock_project):
        """
            TC-CMM-11.3
        """
        
        # Act
        annotations = get_test_method_annotations(mock_project, LanguageType.CSharp)
        
        # Assert
        assert annotations == ['TestMethod', 'Test', 'TestCase' 'Fact', 'Theory']

    @pytest.fixture
    def mock_project_with_custom_csharp(self):
        """
            The fixture creates a project instance using a configuration file containing custom annotations for projects written in C# code
        """
        
        utils.create_config_file(csharp_test_annotations="[\"UnitTest\", \"IntegrationTest\", \"SystemTest\"]")

        if os.path.exists(f"{PATH}project1.config"):
            yield Project(f"{PATH}project1.config")
        else:
            yield

        utils.delete_files()

    def test_get_test_method_annotations_with_custom_csharp(self, mock_project_with_custom_csharp):
        """
            TC-CMM-11.4
        """
        
        # Act
        annotations = get_test_method_annotations(mock_project_with_custom_csharp, LanguageType.CSharp)
        
        # Assert
        assert annotations == ['TestMethod', 'Test', 'TestCase' 'Fact', 'Theory', 'UnitTest', 'IntegrationTest', 'SystemTest']
    
    def test_get_test_method_annotations_unknown(self, mock_project):
        """
            TC-CMM-11.5
        """
        
        # Act
        annotations = get_test_method_annotations(mock_project, LanguageType.Unknown)
        
        # Assert
        assert annotations == None

    # get_test_testing_packages

    def test_get_testing_packages_java(self, mock_project):
        """
            TC-CMM-12.1
        """
        
        # Act
        packages = get_testing_packages(mock_project, LanguageType.Java)
        
        # Assert
        assert packages == [
            'junit.framework.Test',
            'junit.framework.TestCase',
            'org.junit.Test',
            'android.test.AndroidTestCase',
            'android.test.InstrumentationTestCase',
            'android.test.ActivityInstrumentationTestCase2',
            'org.junit.Assert',
            'org.junit.jupiter.api.Test',
            'org.junit.rules.TestRule',
            'org.junit.runner.Description',
            'org.junit.runners.model.Statement',
            'org.junit.jupiter.api.BeforeEach',
            'org.mockito.Mockito',
            'org.assertj.core.api.Assertions.assertThat'
        ]

    @pytest.fixture
    def mock_project_packages_java_with_custom(self):
        """
            The fixture creates a project instance using a configuration file containing 
            custom packages for testing projects written in Java code
        """

        utils.create_config_file(java_testing_packages="[\"Serenity\", \"TestNG\", \"JBehave\"]")

        if os.path.exists(f"{PATH}project1.config"):
            yield Project(f"{PATH}project1.config")
        else:
            yield

        utils.delete_files()

    def test_get_testing_packages_java_with_custom(self, mock_project_packages_java_with_custom):
        """
            TC-CMM-12.2
        """
        
        # Act
        packages = get_testing_packages(mock_project_packages_java_with_custom, LanguageType.Java)
        
        # Assert
        assert packages == [
            'junit.framework.Test',
            'junit.framework.TestCase',
            'org.junit.Test',
            'android.test.AndroidTestCase',
            'android.test.InstrumentationTestCase',
            'android.test.ActivityInstrumentationTestCase2',
            'org.junit.Assert',
            'org.junit.jupiter.api.Test',
            'org.junit.rules.TestRule',
            'org.junit.runner.Description',
            'org.junit.runners.model.Statement',
            'org.junit.jupiter.api.BeforeEach',
            'org.mockito.Mockito',
            'org.assertj.core.api.Assertions.assertThat',
            'Serenity',
            'TestNG',
            'JBehave'
        ]

    def test_get_testing_packages_csharp(self, mock_project):
        """
            TC-CMM-12.3
        """

        # Act
        packages = get_testing_packages(mock_project, LanguageType.CSharp)
        
        # Assert
        assert packages == [
            'Microsoft.VisualStudio.TestTools.UnitTesting',
            'Microsoft.VisualStudio.QualityTools.UnitTesting.Framework',
            'NUnit.Tests',
            'NUnit.Framework',
            'Xunit',
            'Xunit.Abstractions'
        ]

    @pytest.fixture
    def mock_project_packages_csharp_with_custom(self):
        """
            The fixture creates a project instance using a configuration file containing 
            custom packages for testing projects written in C# code
        """

        utils.create_config_file(csharp_testing_packages="[\"MSTest\", \"MbUnit\"]")

        if os.path.exists(f"{PATH}project1.config"):
            yield Project(f"{PATH}project1.config")
        else:
            yield

        utils.delete_files()

    def test_get_testing_packages_csharp_with_custom(self, mock_project_packages_csharp_with_custom):
        """
            TC-CMM-12.4
        """

        # Act
        packages = get_testing_packages(mock_project_packages_csharp_with_custom, LanguageType.CSharp)
        
        # Assert
        assert packages == [
            'Microsoft.VisualStudio.TestTools.UnitTesting',
            'Microsoft.VisualStudio.QualityTools.UnitTesting.Framework',
            'NUnit.Tests',
            'NUnit.Framework',
            'Xunit',
            'Xunit.Abstractions',
            'MSTest',
            'MbUnit'
        ]

    def test_get_test_method_packages_unknown(self, mock_project):
        """
            TC-CMM-12.5
        """
        
        # Act
        packages = get_testing_packages(mock_project, LanguageType.Unknown)
        
        # Assert
        assert packages == None

    def test_get_null_check_test_method_java(self, mock_project):
        """
            TC-CMM-13.1
        """
        
        # Act
        null_check_methods = get_null_check_test_method(mock_project, LanguageType.Java)
        
        # Assert
        assert null_check_methods == [
            'assertNotNull',
            'assertNull'
        ]

    @pytest.fixture
    def mock_project_null_check_test_methods_java_with_custom(self):
        """
            The fixture creates a project instance using a configuration file 
            in which annotations are inserted for checking whether or not null values 
            are returned by methods of a project written in Java code
        """
        utils.create_config_file(java_null_check_methods="[\"assertEmpty\", \"isNull\"]")

        if os.path.exists(f"{PATH}project1.config"):
            yield Project(f"{PATH}project1.config")
        else:
            yield

        utils.delete_files()

    def test_get_null_check_test_method_java_with_custom(self, mock_project_null_check_test_methods_java_with_custom):
        """
            TC-CMM-13.2
        """

        # Act
        null_check_methods = get_null_check_test_method(mock_project_null_check_test_methods_java_with_custom, LanguageType.Java)
        
        # Assert
        assert null_check_methods == [
            'assertNotNull',
            'assertNull',
            'assertEmpty',
            'isNull'
        ]

    def test_get_null_check_test_method_csharp(self, mock_project):
        """
            TC-CMM-13.3
        """
        
        # Act
        null_check_methods = get_null_check_test_method(mock_project, LanguageType.CSharp)
        
        # Assert
        assert null_check_methods == [
            'IsNull',
            'IsNotNull'
        ]

    @pytest.fixture
    def mock_project_null_check_test_methods_csharp_with_custom(self):
        """
            The fixture creates a project instance using a configuration file 
            in which annotations are inserted for checking whether or not null values 
            are returned by methods of a project written in C# code
        """
        utils.create_config_file(csharp_null_check_methods="[\"isEmpty\", \"assertNull\"]")

        if os.path.exists(f"{PATH}project1.config"):
            yield Project(f"{PATH}project1.config")
        else:
            yield

        utils.delete_files()

    def test_get_null_check_test_method_csharp_with_custom(self, mock_project_null_check_test_methods_csharp_with_custom):
        """
            TC-CMM-13.4
        """
        
        # Act
        null_check_methods = get_null_check_test_method(mock_project_null_check_test_methods_csharp_with_custom, LanguageType.CSharp)
        
        # Assert
        assert null_check_methods == [
            'IsNull',
            'IsNotNull',
            'isEmpty',
            'assertNull'
        ]

    def test_get_null_check_test_method_unknown(self, mock_project):
        """
            TC-CMM-13.5
        """
        
        # Act
        null_check_methods = get_null_check_test_method(mock_project, LanguageType.Unknown)
        
        # Assert
        assert null_check_methods == None
    