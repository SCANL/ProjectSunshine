import pytest
import os
import shutil
from src.common.util import get_file_name, read_input, remove_list_nestings, get_config_setting


class TestUtil:

    PATH = "./test/temp/"

    def __create_test_dir(self):
        if not os.path.exists(self.PATH):
            os.mkdir(self.PATH)

        if not os.path.exists(f"{self.PATH}/code"):
            os.mkdir(f"{self.PATH}/code")

        if not os.path.exists(f"{self.PATH}/code/project"):
            os.mkdir(f"{self.PATH}/code/project")

    def __delete_files(self):
        shutil.rmtree(self.PATH)

    @pytest.fixture
    def create_correct_files(self):
        self.__create_test_dir()

        with open(f"{self.PATH}/code/project/Main.java", "a") as code:
            code.write("public class Main {\n")
            code.write("    public static void main(String[] args){\n")
            code.write("        system.out.println(\"hello world\");\n")
            code.write("    }\n}")

        with open(f"{self.PATH}/input_test.csv", "a") as input:
            input.write("file,type,junit\n")
            input.write(f"{self.PATH}/code/project")

        yield

        self.__delete_files()

    @pytest.fixture
    def create_empty_csv(self):
        self.__create_test_dir()

        with open(f"{self.PATH}/input_test.csv", "a") as csv:
            csv.write("file,type,junit")

        yield

        self.__delete_files()

    @pytest.fixture
    def create_wrong_files(self):
        self.__create_test_dir()

        js = open(f"{self.PATH}/code/project/Main.js", "a")
        js.close()

        with open(f"{self.PATH}/input_test.csv", "a") as input:
            input.write("file,type,junit\n")
            input.write(f"{self.PATH}/code/project")

        yield

        self.__delete_files()

    def test_get_file_name(self):
        name = get_file_name("file/myfile.java")
        assert name == "myfile.java", "file name different than expected, got " + \
            name + " expected myfile.java"

    def test_read_input(self, create_correct_files):
        files = read_input(f"{self.PATH}/input_test.csv")
        assert len(files) == 1, "expected 1, given " + str(len(files))

    def test_read_input_fail_1(self):
        with pytest.raises(FileNotFoundError):
            read_input("")

    def test_read_input_fail_2(self, create_empty_csv):
        with pytest.raises(SystemExit):
            read_input(f"{self.PATH}/input_test.csv")

    def test_read_input_fail_3(self, create_wrong_files):
        with pytest.raises(SystemExit):
            read_input(f"{self.PATH}/input_test.csv")

    def test_remove_list_nesting(self):
        """
            Forse questo metodo non fa esattamente quello che dice di fare
        """
        out = remove_list_nestings([1, [2, 3, 4], 5, 6])
        assert out == [1, 5, 6], "get not the expected list " + str(out)

    def test_get_config_settings(self):
        name = get_config_setting("general", "name")
        assert name == "ProjectSunshine"

    def test_get_config_settings_fail_1(self, caplog):
        name = get_config_setting("not existing section", "name")
        assert "not available" in caplog.text, "Not the error message expected"

    def test_get_config_settings_fail_2(self, caplog):
        name = get_config_setting("general", "not existing param")
        assert "not available" in caplog.text, "Not the error message expected"
