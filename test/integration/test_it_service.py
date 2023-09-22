import os
import shutil
import pytest
from src.service.parser import Parser
from src.service import parser as p
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
