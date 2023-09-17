import pytest
import os
import shutil
from src.model.project import Project
from src.common.testing_list import get_test_method_annotations, get_testing_packages, get_null_check_test_method
from src.common.types_list import get_bool_types, get_collection_types, get_numeric_types, get_primitive_types
from src.common.enum import LanguageType
import src.common.util as util
from src.common.util import get_config_setting, read_input

__current_dir = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.realpath(__current_dir))

CONFIG_VALUE_NAME = "ProjectSunshine"
PATH = f"{root}/integration/temp/"

class TestingListUtils:

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
        os.remove("./src/apps/IDEAL/input.csv")
        shutil.rmtree(PATH)

    def create_config_file(self,
                           java_testing_packages="[]",
                           csharp_testing_packages="[]",
                           java_null_check_methods="[]",
                           csharp_null_check_methods="[]",
                           java_test_annotations="[]",
                           csharp_test_annotations="[]"):
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

        with open("./src/apps/IDEAL/input.csv", "w") as input:
            input.write("file,type,junit")

        # creates the custom_code.txt file, inside which the custom packages and annotations used by the user in the project will be inserted
        with open(f"{PATH}custom_code.txt", "w", encoding='utf-8') as code_file:
            code_file.write("[DataTypes]\n")
            code_file.write("csharp_custom_collection_data_types = []\n")
            code_file.write("\n[Test]\n")
            code_file.write(
                f"java_custom_testing_packages = {java_testing_packages}\n")
            code_file.write(
                f"csharp_custom_testing_packages = {csharp_testing_packages}\n")
            code_file.write(
                f"java_custom_null_check_test_methods = {java_null_check_methods}\n")
            code_file.write(
                f"csharp_custom_null_check_test_methods = {csharp_null_check_methods}\n")
            code_file.write(
                f"java_custom_test_method_annotation = {java_test_annotations}\n")
            code_file.write(
                f"csharp_custom_test_method_annotation = {csharp_test_annotations}\n")

        # create the project1.config file, in which the path to our file with the custom code will be inserted
        if not os.path.exists(f'{PATH}project1.config'):
            with open(f"{PATH}project1.config", "w", encoding="utf-8") as config:
                config.write("[Files]\n")
                config.write("input_file=./src/apps/IDEAL/input.csv\n")
                config.write("output_directory=./src/apps/IDEAL\n")
                config.write("custom_code=" + PATH + "custom_code.txt\n")
                config.write("custom_terms=custom_terms.txt\n")

                config.write("[Properties]\n")
                config.write("junit_version=4\n")


testing_list_utils = TestingListUtils()


@pytest.mark.integration
class TestItUtils:

    def __create_test_dir(self):
        """
            The function deals with the creation of folders
            that will contain the files created specifically for function testing
        """
        if not os.path.exists(PATH):
            os.mkdir(PATH)

        if not os.path.exists(f"{PATH}/code"):
            os.mkdir(f"{PATH}/code")

        if not os.path.exists(f"{PATH}/code/project"):
            os.mkdir(f"{PATH}/code/project")

    def __setup(self):
        """
            This fixture is used to create a temp directory where the config file will be stored
            and to remove it after the tests are done.
        """
        # create a temp directory where the config files will be stored
        os.mkdir(PATH)

        # write the config file in the directory
        with open(f'{PATH}config.txt', 'w') as f:
            f.write(f"[general]\nname = {CONFIG_VALUE_NAME}\n")

    def __delete_files(self):
        """
            The function completely deletes all files and folders created for testing
        """
        shutil.rmtree(PATH)

    @pytest.fixture
    def create_correct_files(self):
        """
            the function takes care of the creation of a project file and an input.csv file
            containing the path to the previous file, in order to simulate
            the existence of an input to the system that is correct
        """
        self.__create_test_dir()

        with open(f"{PATH}/code/project/Main.java", "a") as code:
            code.write("public class Main {\n")
            code.write("    public static void main(String[] args){\n")
            code.write("        system.out.println(\"hello world\");\n")
            code.write("    }\n}")

        with open(f"{PATH}/input_test.csv", "a") as input:
            input.write("file,type,junit\n")
            input.write(f"{PATH}/code/project")

        yield

        self.__delete_files()

    @pytest.fixture
    def create_empty_csv(self):
        """
            The function takes care of creating an empty dummy input.csv file,
            in order to simulate an incorrect input to the system
        """
        self.__create_test_dir()

        with open(f"{PATH}/input_test.csv", "a") as csv:
            csv.write("file,type,junit")

        yield

        self.__delete_files()

    @pytest.fixture
    def create_wrong_files(self):
        """
            The function takes care of the creation of a project file with an extension that cannot be analyzed by the system,
            and of an input.csv file containing the path to it,
            in order to simulate an incorrect input to the system
        """
        self.__create_test_dir()

        js = open(f"{PATH}/code/project/Main.js", "a")
        js.close()

        with open(f"{PATH}/input_test.csv", "a") as input:
            input.write("file,type,junit\n")
            input.write(f"{PATH}/code/project")

        yield

        self.__delete_files()

    def test_read_input(self, create_correct_files):
        """
            TC-CMM-4.1
        """

        # Act
        files = read_input(f"{PATH}/input_test.csv")

        # Assert
        assert len(files) == 1, "expected 1, given " + str(len(files))

    def test_read_input_fail_2(self, create_empty_csv, capfd):
        """
            TC-CMM-4.2
        """

        # Act
        with pytest.raises(SystemExit):
            read_input(f"{PATH}/input_test.csv")
        out, _ = capfd.readouterr()

        # Assert
        assert "[Main] Critical: Input CSV file cannot be empty: " in out

    def test_read_input_fail_3(self, create_wrong_files, capfd):
        """
            TC-CMM-4.3
        """

        # Act
        with pytest.raises(SystemExit):
            read_input(f"{PATH}/input_test.csv")
        out, _ = capfd.readouterr()

        # Assert
        assert "[Main] Critical: Invalid files provided in input CSV file: " in out

    def test_read_input_fail_1(self):
        """
            TC-CMM-4.4
        """

        # Assert
        with pytest.raises(FileNotFoundError):
            read_input("")

    @pytest.fixture
    def mock_os_path_join(self, monkeypatch):
        """
            This fixture is used to mock the os.path.join function so that it returns the path of the config created for this test case. 
        """

        self.__setup()

        def mock_join(*args):
            # Replace with the desired mocked path
            return f"{PATH}config.txt"

        # Apply the monkeypatch to os.path.join
        monkeypatch.setattr(os.path, 'join', mock_join)

        yield

        self.__delete_files()

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


class TestItTestingList:

    @pytest.fixture
    def mock_project(self):
        """
            The fixture creates a project instance using a configuration file without any kind of custom term
        """

        testing_list_utils.create_config_file()

        yield Project(f"{PATH}project1.config")
  
        testing_list_utils.delete_files()

    def test_get_test_method_annotations_java(self, mock_project):
        """
            TC-CMM-11.1
        """

        # Act
        annotations = get_test_method_annotations(
            mock_project, LanguageType.Java)

        # Assert
        assert annotations == ['Test']

    @pytest.fixture
    def mock_project_with_custom_java(self):
        """
            The fixture creates a project instance using a configuration file containing custom annotations for projects written in Java code
        """

        testing_list_utils.create_config_file(
            java_test_annotations="[\"UnitTest\", \"IntegrationTest\", \"SystemTest\"]")

        yield Project(f"{PATH}project1.config")

        testing_list_utils.delete_files()

    def test_get_test_method_annotations_with_custom_java(self, mock_project_with_custom_java):
        """
            TC-CMM-11.2
        """

        # Act
        annotations = get_test_method_annotations(
            mock_project_with_custom_java, LanguageType.Java)

        # Assert
        assert annotations == ['Test', 'UnitTest',
                               'IntegrationTest', 'SystemTest']

    def test_get_test_method_annotations_csharp(self, mock_project):
        """
            TC-CMM-11.3
        """

        # Act
        annotations = get_test_method_annotations(
            mock_project, LanguageType.CSharp)

        # Assert
        assert annotations == ['TestMethod',
                               'Test', 'TestCase' 'Fact', 'Theory']

    @pytest.fixture
    def mock_project_with_custom_csharp(self):
        """
            The fixture creates a project instance using a configuration file containing custom annotations for projects written in C# code
        """

        testing_list_utils.create_config_file(
            csharp_test_annotations="[\"UnitTest\", \"IntegrationTest\", \"SystemTest\"]")

        yield Project(f"{PATH}project1.config")

        testing_list_utils.delete_files()

    def test_get_test_method_annotations_with_custom_csharp(self, mock_project_with_custom_csharp):
        """
            TC-CMM-11.4
        """

        # Act
        annotations = get_test_method_annotations(
            mock_project_with_custom_csharp, LanguageType.CSharp)

        # Assert
        assert annotations == ['TestMethod', 'Test', 'TestCase' 'Fact',
                               'Theory', 'UnitTest', 'IntegrationTest', 'SystemTest']

    def test_get_test_method_annotations_unknown(self, mock_project):
        """
            TC-CMM-11.5
        """

        # Act
        annotations = get_test_method_annotations(
            mock_project, LanguageType.Unknown)

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

        testing_list_utils.create_config_file(
            java_testing_packages="[\"Serenity\", \"TestNG\", \"JBehave\"]")

        yield Project(f"{PATH}project1.config")

        testing_list_utils.delete_files()

    def test_get_testing_packages_java_with_custom(self, mock_project_packages_java_with_custom):
        """
            TC-CMM-12.2
        """

        # Act
        packages = get_testing_packages(
            mock_project_packages_java_with_custom, LanguageType.Java)

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

        testing_list_utils.create_config_file(
            csharp_testing_packages="[\"MSTest\", \"MbUnit\"]")

        yield Project(f"{PATH}project1.config")

        testing_list_utils.delete_files()

    def test_get_testing_packages_csharp_with_custom(self, mock_project_packages_csharp_with_custom):
        """
            TC-CMM-12.4
        """

        # Act
        packages = get_testing_packages(
            mock_project_packages_csharp_with_custom, LanguageType.CSharp)

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
        null_check_methods = get_null_check_test_method(
            mock_project, LanguageType.Java)

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
        testing_list_utils.create_config_file(
            java_null_check_methods="[\"assertEmpty\", \"isNull\"]")

        yield Project(f"{PATH}project1.config")

        testing_list_utils.delete_files()

    def test_get_null_check_test_method_java_with_custom(self, mock_project_null_check_test_methods_java_with_custom):
        """
            TC-CMM-13.2
        """

        # Act
        null_check_methods = get_null_check_test_method(
            mock_project_null_check_test_methods_java_with_custom, LanguageType.Java)

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
        null_check_methods = get_null_check_test_method(
            mock_project, LanguageType.CSharp)

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
        testing_list_utils.create_config_file(
            csharp_null_check_methods="[\"isEmpty\", \"assertNull\"]")

        yield Project(f"{PATH}project1.config")

        testing_list_utils.delete_files()

    def test_get_null_check_test_method_csharp_with_custom(self, mock_project_null_check_test_methods_csharp_with_custom):
        """
            TC-CMM-13.4
        """

        # Act
        null_check_methods = get_null_check_test_method(
            mock_project_null_check_test_methods_csharp_with_custom, LanguageType.CSharp)

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
        null_check_methods = get_null_check_test_method(
            mock_project, LanguageType.Unknown)

        # Assert
        assert null_check_methods == None


class TypesListUtils:

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
        os.remove("./src/apps/IDEAL/input.csv")
        shutil.rmtree(PATH)

    def create_config_file(self,
                           csharp_custom_collection_data_types="[]",
                           java_custom_collection_data_types="[]"):
        """
            this function creates the configuration files needed to run the tests
            Args:
                csharp_custom_collection_data_types: The list of custom collection data types used for testing a project written in C# code to be included in the configuration file
                java_custom_collection_data_types: The list of custom collection data types used for testing a project written in Java code to be included in the configuration file
        """

        self.__create_test_dir()

        with open("./src/apps/IDEAL/input.csv", "w") as input:
            input.write("file,type,junit")

        # creates the custom_code.txt file, inside which the custom packages and annotations used by the user in the project will be inserted
        with open(f"{PATH}custom_code.txt", "w") as code_file:
            code_file.write("[DataTypes]\n")
            code_file.write(
                f"csharp_custom_collection_data_types = {csharp_custom_collection_data_types}\n")
            code_file.write(
                f"java_custom_collection_data_types = {java_custom_collection_data_types}\n")
            code_file.write("\n[Test]\n")
            code_file.write("java_custom_testing_packages = []\n")
            code_file.write("csharp_custom_testing_packages = []\n")
            code_file.write("java_custom_null_check_test_methods = []\n")
            code_file.write("csharp_custom_null_check_test_methods = []\n")
            code_file.write("java_custom_test_method_annotation = []\n")
            code_file.write("csharp_custom_test_method_annotation = []\n")

        # create the project1.config file, in which the path to our file with the custom code will be inserted
        if not os.path.exists(f"{PATH}project1.config"):
            with open(f"{PATH}project1.config", "w") as config:
                config.write("[Files]\n")
                config.write("input_file=./src/apps/IDEAL/input.csv\n")
                config.write("output_directory=./src/apps/IDEAL\n")
                config.write("custom_code=" + PATH + "custom_code.txt\n")
                config.write("custom_terms=custom_terms.txt\n")

                config.write("[Properties]\n")
                config.write("junit_version=4\n")


types_list_utils = TypesListUtils()


class TestItTypesList:

    @pytest.fixture
    def mock_project(self):
        """
            The fixture creates a project instance using a configuration file without any kind of custom type
        """

        types_list_utils.create_config_file()

        yield Project(f"{PATH}project1.config")

        types_list_utils.delete_files()

    def test_get_collection_types_java(self, mock_project):
        """
            TC-CMM-14.1
        """

        # Act
        collection_types = get_collection_types(
            mock_project, LanguageType.Java)

        # Assert
        assert collection_types == [
            'ArrayBlockingQueue',
            'ArrayDeque',
            'ArrayList',
            'BlockingDeque',
            'BlockingQueue',
            'Collection',
            'ConcurrentHashMap',
            'ConcurrentMap',
            'ConcurrentNavigableMap',
            'ConcurrentSkipListMap',
            'ConcurrentSkipListSet',
            'CopyOnWriteArrayList',
            'CopyOnWriteArraySet',
            'DelayQueue',
            'Deque',
            'HashMap',
            'HashSet',
            'Hashtable',
            'Iterator ',
            'LinkedBlockingDeque',
            'LinkedBlockingQueue',
            'LinkedHashMap',
            'LinkedHashSet',
            'LinkedList',
            'LinkedTransferQueue',
            'List',
            'ListIterator',
            'Map',
            'NavigableMap',
            'NavigableSet',
            'PriorityBlockingQueue',
            'PriorityQueue',
            'Queue',
            'Set',
            'SortedMap',
            'SortedSet',
            'SynchronousQueue',
            'TransferQueue',
            'TreeMap',
            'TreeSet',
            'Vector',
            'BitSet'
        ]

    @pytest.fixture
    def mock_project_with_custom_java(self):
        """
            The fixture creates a project instance using a configuration file containing custom collection types for projects written in Java code
        """

        types_list_utils.create_config_file(
            java_custom_collection_data_types="[\"BigCollection\", \"Matrix\"]")

        yield Project(f"{PATH}project1.config")

        types_list_utils.delete_files()

    def test_get_collection_types_with_custom_java(self, mock_project_with_custom_java):
        """
            TC-CMM-14.2
        """

        # Act
        collection_types = get_collection_types(
            mock_project_with_custom_java, LanguageType.Java)

        # Assert
        assert collection_types == [
            'ArrayBlockingQueue',
            'ArrayDeque',
            'ArrayList',
            'BlockingDeque',
            'BlockingQueue',
            'Collection',
            'ConcurrentHashMap',
            'ConcurrentMap',
            'ConcurrentNavigableMap',
            'ConcurrentSkipListMap',
            'ConcurrentSkipListSet',
            'CopyOnWriteArrayList',
            'CopyOnWriteArraySet',
            'DelayQueue',
            'Deque',
            'HashMap',
            'HashSet',
            'Hashtable',
            'Iterator ',
            'LinkedBlockingDeque',
            'LinkedBlockingQueue',
            'LinkedHashMap',
            'LinkedHashSet',
            'LinkedList',
            'LinkedTransferQueue',
            'List',
            'ListIterator',
            'Map',
            'NavigableMap',
            'NavigableSet',
            'PriorityBlockingQueue',
            'PriorityQueue',
            'Queue',
            'Set',
            'SortedMap',
            'SortedSet',
            'SynchronousQueue',
            'TransferQueue',
            'TreeMap',
            'TreeSet',
            'Vector',
            'BitSet',
            'BigCollection',
            'Matrix'
        ]

    def test_collection_types_csharp(self, mock_project):
        """
            TC-CMM-14.3
        """

        # Act
        collection_types = get_collection_types(
            mock_project, LanguageType.CSharp)

        # Assert
        assert collection_types == [
            'Dictionary',
            'List',
            'Queue',
            'Stack',
            'LinkedList',
            'ObservableCollection',
            'SortedList',
            'HashSet',
            'SortedSet',
            'Hashtable',
            'Array',
            'ArrayList',
            'ConcurrentDictionary',
            'BitArray',
            'BlockingCollection',
            'ConcurrentQueue',
            'ConcurrentStack',
            'ConcurrentBag',
            'ICollection',
            'IComparer',
            'IDictionary',
            'IDictionaryEnumerator',
            'IEnumerable',
            'IEnumerator',
            'IEqualityComparer',
            'IHashCodeProvider',
            'IList',
            'IStructuralComparable',
            'IStructuralEquatable',
            'Collection',
            'ReadOnlyObservableCollection',
            'KeyedCollection',
            'ReadOnlyCollection',
            'ReadOnlyDictionary'
        ]

    @pytest.fixture
    def mock_project_with_custom_csharp(self):
        """
            The fixture creates a project instance using a configuration file containing custom collection types for projects written in C# code
        """

        types_list_utils.create_config_file(
            csharp_custom_collection_data_types="[\"PriorityQueue\", \"Matrix\"]")

        yield Project(f"{PATH}project1.config")

        types_list_utils.delete_files()

    def test_get_collection_types_with_custom_csharp(self, mock_project_with_custom_csharp):
        """
            TC-CMM-14.4
        """

        # Act
        collection_types = get_collection_types(
            mock_project_with_custom_csharp, LanguageType.CSharp)

        # Assert
        assert collection_types == [
            'Dictionary',
            'List',
            'Queue',
            'Stack',
            'LinkedList',
            'ObservableCollection',
            'SortedList',
            'HashSet',
            'SortedSet',
            'Hashtable',
            'Array',
            'ArrayList',
            'ConcurrentDictionary',
            'BitArray',
            'BlockingCollection',
            'ConcurrentQueue',
            'ConcurrentStack',
            'ConcurrentBag',
            'ICollection',
            'IComparer',
            'IDictionary',
            'IDictionaryEnumerator',
            'IEnumerable',
            'IEnumerator',
            'IEqualityComparer',
            'IHashCodeProvider',
            'IList',
            'IStructuralComparable',
            'IStructuralEquatable',
            'Collection',
            'ReadOnlyObservableCollection',
            'KeyedCollection',
            'ReadOnlyCollection',
            'ReadOnlyDictionary',
            'PriorityQueue',
            'Matrix'
        ]

    def test_get_collection_types_unknown(self, mock_project):
        """
            TC-CMM-14.5
        """

        # Act
        collection_types = get_collection_types(
            mock_project, LanguageType.Unknown)

        # Assert
        assert collection_types == None

    def test_collection_types_cpp(self, mock_project):
        """
            TC-CMM-14.6
        """

        # Act
        collection_types = get_collection_types(mock_project, LanguageType.CPP)

        # Assert
        assert collection_types == [
            'array',
            'vector',
            'deque',
            'forward_list',
            'list',
            'stack',
            'queue',
            'priority_queue',
            'set',
            'multiset',
            'map',
            'multimap',
            'unordered_set',
            'unordered_multiset',
            'unordered_map',
            'unordered_multimap'
        ]
