import os
import shutil
import pytest
from src.service.parser import Parser
from src.service import parser as p
from src.service.parser import PythonParser
from definitions import ROOT_DIR

PATH = ROOT_DIR + "/test/integration/temp"


@pytest.mark.integration
class TestItService:

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

    def __create_code_dir(self):
        if not os.path.exists(PATH):
            os.mkdir(PATH)

    def __delete_files(self):
        """
            The function completely deletes all files and folders created for testing
        """
        shutil.rmtree(PATH)

    @pytest.fixture(scope="module")
    def create_correct_files(self):
        """
            the function takes care of the creation of a project file and an input.csv file
            containing the path to the previous file, in order to simulate
            the existence of an input to the system that is correct
        """
        self.__create_test_dir()

        test_file_content = """public class Main {
    public static void main(String[] args){
        System.out.println("hello world");
    }
}
"""

        with open(f"{PATH}/code/project/Main.java", "a") as code:
            code.write(test_file_content)

        yield

        self.__delete_files()

    @pytest.fixture
    def parser(self):
        return Parser()

    def test_run_srcml(self, create_correct_files, parser: Parser):
        """
            ID: TC-SRV-4.1

            Not really sure what is going on in this method.
            The static method __run_srcml must be called with that syntax
            even though some type issues show up in vscode.

            This test is also failing because the command to spawn
            srcml is broken.
        """
        _, error = parser._Parser__run_srcml(               # type: ignore
            f"{PATH}/code/project/Main.java"
        )
        assert len(error) == 0

    def test_parse_file(self, parser: Parser):
        """
            ID: TC-SRV-3.2        """
        result = parser.parse_file(
            f"{PATH}/code/project/Main.java"
        )
        assert result == True

    @pytest.fixture
    def create_code_file(self):
        self.__create_code_dir()

        with open(f"{PATH}/Main.py", "a") as file:
            file.write("\"\"\"\n")
            file.write("    this variable contains the dog name\n")
            file.write("\"\"\"\n")
            file.write("dog_name = \"Jack\"\n")
            file.write("def get_dog_name(project):\n")
            file.write("    \"\"\"\n")
            file.write("        this function returns the dog name")
            file.write("    \"\"\"\n")
            file.write("    return dog_name")

        yield 

        os.remove(f"{PATH}/Main.py")

    @pytest.fixture
    def create_multiple_attr_in_func_code_file(self):
        self.__create_code_dir()

        with open(f"{PATH}/Main.py", "a") as file:
            file.write("\"\"\"\n")
            file.write("    this variable contains the dog name\n")
            file.write("\"\"\"\n")
            file.write("dog_name = \"Jack\"\n")
            file.write("def get_dog_name(project):\n")
            file.write("    \"\"\"\n")
            file.write("        this function returns the dog name\n")
            file.write("    \"\"\"\n")
            file.write("    new_dog_name = \"Mike\"\n")
            file.write("    return dog_name")

        yield 

        os.remove(f"{PATH}/Main.py")

    @pytest.fixture
    def create_multiple_attr_code_file(self):
        self.__create_code_dir()

        with open(f"{PATH}/Main.py", "a") as file:
            file.write("\"\"\"\n")
            file.write("    this variable contains the dog name\n")
            file.write("\"\"\"\n")
            file.write("dog_name = \"Jack\"\n")
            file.write("\"\"\"\n")
            file.write("    this variable contains the cat name\n")
            file.write("\"\"\"\n")
            file.write("cat_name = \"Kitty\"\n")
            file.write("def get_dog_name(project):\n")
            file.write("    \"\"\"\n")
            file.write("        this function returns the dog name\n")
            file.write("    \"\"\"\n")
            file.write("    return dog_name")

        yield 

        os.remove(f"{PATH}/Main.py")

    @pytest.fixture
    def mock_ast_tree(self):
        with open(f"{PATH}/Main.py", 'r') as file:
            data = file.read()
            parser = PythonParser(data)

            return parser
    
    def test_parse_single_attribute(self, create_code_file, mock_ast_tree):
        p: PythonParser = mock_ast_tree

        p.extract_attribute()

        assert len(p.attributes) == 1
        assert p.attributes[0].get_identifier() == 'dog_name'

    def test_parse_multiple_attributes(self, create_multiple_attr_code_file, mock_ast_tree):
        p: PythonParser = mock_ast_tree

        p.extract_attribute()

        assert len(p.attributes) == 2
        assert p.attributes[0].get_identifier() == 'dog_name'

    @pytest.fixture
    def create_no_attribute_code_file(self):
        self.__create_code_dir()

        with open(f"{PATH}/Main.py", "a") as file:
            file.write("def get_dog_name(project):\n")
            file.write("    \"\"\"\n")
            file.write("        this function returns the dog name")
            file.write("    \"\"\"\n")
            file.write("    return dog_name")

        yield 

        os.remove(f"{PATH}/Main.py")

    def test_parse_no_attribute(self, create_no_attribute_code_file, mock_ast_tree):
        p: PythonParser = mock_ast_tree

        p.extract_attribute()

        assert len(p.attributes) == 0

    def test_parse_attribute_in_function(self, create_multiple_attr_in_func_code_file, mock_ast_tree):
        p: PythonParser = mock_ast_tree

        p.extract_attribute()

        assert len(p.attributes) == 2
        assert p.attributes[0].get_identifier() == 'dog_name'

    def test_parse_single_function(self, create_code_file, mock_ast_tree):
        p: PythonParser = mock_ast_tree

        p.extract_function()

        assert len(p.functions)== 1
        assert p.functions[0].get_identifier() == 'get_dog_name'

    @pytest.fixture
    def create_single_func_in_a_class_code_file(self):
        self.__create_code_dir()

        with open(f"{PATH}/Main.py", "a") as file:
            file.write("class MyClass:\n")
            file.write("    dog_name = \"Jhon\"\n")
            file.write("    def get_dog_name(project):\n")
            file.write("        \"\"\"\n")
            file.write("            this function returns the dog name")
            file.write("        \"\"\"\n")
            file.write("        return dog_name")

        yield 

        os.remove(f"{PATH}/Main.py")

    def test_parse_single_function(self, create_single_func_in_a_class_code_file, mock_ast_tree):
        p: PythonParser = mock_ast_tree

        p.extract_function()

        assert len(p.functions)== 1
        assert p.functions[0].get_identifier() == 'get_dog_name'

    @pytest.fixture
    def create_multiple_func_in_a_class_code_file(self):
        self.__create_code_dir()

        with open(f"{PATH}/Main.py", "a") as file:
            file.write("class MyClass:\n")
            file.write("    dog_name = \"Jhon\"\n")
            file.write("    cat_name = \"Kitty\"\n")
            file.write("    def get_dog_name(project):\n")
            file.write("        \"\"\"\n")
            file.write("            this function returns the dog name")
            file.write("        \"\"\"\n")
            file.write("        return dog_name\n\n")
            file.write("    def get_cat_name(project):\n")
            file.write("        \"\"\"\n")
            file.write("            this function returns the dog name\n")
            file.write("        \"\"\"\n")
            file.write("        return cat_name\n")

        yield 

        os.remove(f"{PATH}/Main.py")

    def test_parse_multiple_function_in_a_class(self, create_multiple_func_in_a_class_code_file, mock_ast_tree):
        p: PythonParser = mock_ast_tree

        p.extract_function()

        assert len(p.functions)== 2
        assert p.functions[0].get_identifier() == 'get_dog_name'
        assert p.functions[1].get_identifier() == 'get_cat_name'

    @pytest.fixture
    def create_multiple_func_code_file(self):
        self.__create_code_dir()

        with open(f"{PATH}/Main.py", "a") as file:
            file.write("\"\"\"\n")
            file.write("    this variable contains the dog name\n")
            file.write("\"\"\"\n")
            file.write("dog_name = \"Jack\"\n")
            file.write("cat_name = \"Kitty\"\n")
            file.write("def get_dog_name(project):\n")
            file.write("    \"\"\"\n")
            file.write("        this function returns the dog name\n")
            file.write("    \"\"\"\n")
            file.write("    return dog_name\n\n")
            file.write("def get_cat_name(project):\n")
            file.write("    \"\"\"\n")
            file.write("        this function returns the dog name\n")
            file.write("    \"\"\"\n")
            file.write("    return cat_name")

        yield 

        os.remove(f"{PATH}/Main.py")

    def test_parse_multiple_function(self, create_multiple_func_code_file, mock_ast_tree):
        p: PythonParser = mock_ast_tree

        p.extract_function()

        assert len(p.functions)== 2
        assert p.functions[0].get_identifier() == 'get_dog_name'
        assert p.functions[1].get_identifier() == 'get_cat_name'

    @pytest.fixture
    def create_no_func_code_file(self):
        self.__create_code_dir()

        with open(f"{PATH}/Main.py", "a") as file:
            file.write("\"\"\"\n")
            file.write("    this variable contains the dog name\n")
            file.write("\"\"\"\n")
            file.write("dog_name = \"Jack\"\n")
            file.write("cat_name = \"Kitty\"\n")

        yield 

        os.remove(f"{PATH}/Main.py")

    def test_parse_no_function(self, create_no_func_code_file, mock_ast_tree):
        p: PythonParser = mock_ast_tree

        p.extract_function()

        assert len(p.functions)== 0

    def create_file_with_assign(self, assign_type, var_name="variable_name"):
        self.__create_code_dir()

        with open(f"{PATH}/Main.py", "a") as file:
            file.write("\"\"\"\n")
            file.write("    this is the variable content\n")
            file.write("\"\"\"\n")
            file.write(f"{var_name} = {assign_type}")

    @pytest.fixture
    def mock_ast_tree_array_assign(self):
        self.create_file_with_assign(assign_type="[\"first_value\", \"second_value\"]")

        parser = None

        with open(f"{PATH}/Main.py", 'r') as file:
            data = file.read()
            print(data)
            parser = PythonParser(data)

        yield parser

        os.remove(f"{PATH}/Main.py")

    def test_attribute_with_array_value(self, mock_ast_tree_array_assign):
        p: PythonParser = mock_ast_tree_array_assign

        p.extract_attribute()
        print(p.attributes[0].get_code())

        assert "[\"first_value\", \"second_value\"]" in p.get_attributes()[0].get_code()

    @pytest.fixture
    def mock_ast_tree_tuple_assign(self):
        self.create_file_with_assign(assign_type="(\"first_value\", \"second_value\", \"third_value\")")

        parser = None

        with open(f"{PATH}/Main.py", 'r') as file:
            data = file.read()
            print(data)
            parser = PythonParser(data)

        yield parser

        os.remove(f"{PATH}/Main.py")

    def test_attribute_with_tuple_value(self, mock_ast_tree_tuple_assign):
        p: PythonParser = mock_ast_tree_tuple_assign

        p.extract_attribute()
        print(p.attributes[0].get_code())

        assert "(\"first_value\", \"second_value\", \"third_value\")" in p.get_attributes()[0].get_code()

    @pytest.fixture
    def mock_ast_tree_set_assign(self):
        self.create_file_with_assign(assign_type="{\"first_value\", \"second_value\", \"third_value\"}")

        parser = None

        with open(f"{PATH}/Main.py", 'r') as file:
            data = file.read()
            print(data)
            parser = PythonParser(data)

        yield parser

        os.remove(f"{PATH}/Main.py")

    def test_attribute_with_set_value(self, mock_ast_tree_set_assign):
        p: PythonParser = mock_ast_tree_set_assign

        p.extract_attribute()
        print(p.attributes[0].get_code())

        assert "{\"first_value\", \"second_value\", \"third_value\"}" in p.get_attributes()[0].get_code()

    @pytest.fixture
    def mock_ast_tree_dictionary_assign(self):
        self.create_file_with_assign(assign_type="{\"first_value\": \"one\", \"second_value\": \"two\", \"third_value\": \"three\"}")

        parser = None

        with open(f"{PATH}/Main.py", 'r') as file:
            data = file.read()
            print(data)
            parser = PythonParser(data)

        yield parser

        os.remove(f"{PATH}/Main.py")

    def test_attribute_with_dictionary_value(self, mock_ast_tree_dictionary_assign):
        p: PythonParser = mock_ast_tree_dictionary_assign

        p.extract_attribute()
        print(p.attributes[0].get_code())

        assert "{first_value: \"one\", second_value: \"two\", third_value: \"three\"}" in p.get_attributes()[0].get_code()

    @pytest.fixture
    def mock_ast_tree_tuple_name_assign(self):
        self.create_file_with_assign(var_name="val1, val2" ,assign_type="100, 200")

        parser = None

        with open(f"{PATH}/Main.py", 'r') as file:
            data = file.read()
            print(data)
            parser = PythonParser(data)

        yield parser

        os.remove(f"{PATH}/Main.py")

    def test_attribute_with_tuple_name_assign(self,  mock_ast_tree_tuple_name_assign):
        p: PythonParser =  mock_ast_tree_tuple_name_assign

        p.extract_attribute()
        print(p.attributes[0].get_code())

        assert "val1, val2" in p.get_attributes()[0].get_identifier()

    @pytest.fixture
    def mock_ast_tree_list_name_assign(self):
        self.create_file_with_assign(var_name="val1, val2, val3" ,assign_type="100, 200, 300")

        parser = None

        with open(f"{PATH}/Main.py", 'r') as file:
            data = file.read()
            print(data)
            parser = PythonParser(data)

        yield parser

        os.remove(f"{PATH}/Main.py")

    def test_attribute_with_list_name_assign(self,  mock_ast_tree_list_name_assign):
        p: PythonParser =  mock_ast_tree_list_name_assign

        p.extract_attribute()
        print(p.attributes[0].get_code())

        assert "val1, val2, val3" in p.get_attributes()[0].get_identifier()

    @pytest.fixture
    def mock_ast_tree_func_call_assign(self):
        self.create_file_with_assign(assign_type="func_call()")

        parser = None

        with open(f"{PATH}/Main.py", 'r') as file:
            data = file.read()
            print(data)
            parser = PythonParser(data)

        yield parser

        os.remove(f"{PATH}/Main.py")

    def test_attribute_with_func_call_value(self, mock_ast_tree_func_call_assign):
        p: PythonParser = mock_ast_tree_func_call_assign

        p.extract_attribute()
        print(p.attributes[0].get_code())

        assert "func_call()" in p.get_attributes()[0].get_code() 