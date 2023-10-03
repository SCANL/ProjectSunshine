import ctypes
import logging
import sys
import ast
from src.model.greet import greet_attribute, greet_function
from typing import List, Optional
from enum import Enum
from subprocess import Popen, PIPE
from typing import Tuple
from src.common import util


class Parser:
    """
        A utility class for parsing source code files using srcML.
        Attributes:
            parsed_string (str): The parsed source code as a string.
    """

    log = logging.getLogger(__name__)

    def __init__(self):
        self.parsed_string = None

    @staticmethod
    def __run_srcml(file_path: str) -> Tuple[bytes, bytes]:
        """
            Run srcML on a source code file.
            Args:
                file_path (str): The path to the source code file.
            Returns:
                tuple: A tuple containing the parsed result (stdout) and any error messages (stderr).
        """
        directory = util.get_config_setting('srcml', 'directory')
        executable = util.get_config_setting('srcml', 'executable')
        position = '--position'

        args = [executable, position, file_path]

        if sys.platform.startswith("win"):
            file_path = '"'+file_path+'"'
            # Don't display the Windows GPF dialog if the invoked program dies.
            SEM_NOGPFAULTERRORBOX = 0x0002
            ctypes.windll.kernel32.SetErrorMode(  # type: ignore
                SEM_NOGPFAULTERRORBOX
            )
            subprocess_flags = 0x8000000
            process = Popen(" ".join(args), stdout=PIPE, stderr=PIPE,
                            creationflags=subprocess_flags, cwd=directory)
        else:
            subprocess_flags = 0
            process = Popen(args, stdout=PIPE, stderr=PIPE,
                            creationflags=subprocess_flags, cwd=directory)

        return process.communicate()

    def parse_file(self, file_path: str) -> bool:
        """
            Parse a source code file using srcML.
            Args:
                file_path (str): The path to the source code file.
            Returns:
                bool: True if parsing was successful, False otherwise.
        """
        result, error = self.__run_srcml(file_path)
        if len(error) == 0:
            result.decode("utf-8")
            self.parsed_string = result
            return True
        else:
            return False


class Structures(Enum):
    LIST = 0
    TUPLE = 1
    SET = 2
    DICTIONARY = 3


class PythonParser:

    def __init__(self, parsed_file):
        self.DATA_STRUCTURES_COLSURES = {
            "list_start": "[",
            "list_end": "]",
            "graph_start": "{",
            "graph_end": "}",
            "tuple_start": "(",
            "tuple_end": ")"
        }
        self.code = None
        self.functions = []
        self.attributes = []
        if len(parsed_file) > 0:
            code = ast.parse(parsed_file)
            self.code = code
            self.opened_file = parsed_file

    def get_functions(self) -> Optional[List[greet_function.GreetFunction]]:
        """
            Returns a list of GreetFunction objects if there are functions in the parsed file, otherwise None.

            Returns:
                Optional[List[greet_function.GreetFunction]]: A list of GreetFunction objects or None.
        """
        if len(self.functions) > 0:
            return self.functions

    def get_attributes(self) -> Optional[List[greet_attribute.GreetAttribute]]:
        """
            Returns a list of GreetAttribute objects if there are attributes in the parsed file, otherwise None.

            Returns:
                Optional[List[greet_attribute.GreetAttribute]]: A list of GreetAttribute objects or None.
        """
        if len(self.attributes) > 0:
            return self.attributes

    def parse_file(self):
        """
            Parses the file by extracting attributes and functions.
        """
        self.extract_attribute()
        self.extract_function()

    def extract_attribute(self):
        """
            Extracts variables and their comments from the target file by calling the private method `__extract()`.
        """
        if self.code:
            self.__extract(self.code)

    def __extract(self, code):
        """
            Recursively extracts variables and their comments from the target file using the AST (Abstract Syntax Tree).

            Args:
                code (ast.AST): The parent node of the subtree to be analyzed.

            Notes:
                - The analysis is performed recursively. When the function encounters a node that can have children (e.g., a function or a class), it iterates over the children to extract variables and comments.
                - For variables, it checks if the immediately preceding node in the file is a multiline comment. If so, it creates a GreetAttribute instance and adds it to the list of attributes.
                - If the function encounters a node of type Function or Class, it calls itself recursively to continue the analysis.

    """
        childs = code.body
        for index, node in enumerate(childs):
            name = ""
            if isinstance(node, ast.Assign) or (isinstance(node, ast.Expr) and isinstance(node.value, ast.Attribute)):
                if index - 1 >= 0 and isinstance(code.body[index - 1], ast.Expr) and isinstance(code.body[index - 1].value, ast.Str):
                    name, colls = self.__extract_name(node)
                    start_line = code.body[index - 1].lineno

                    attribute = greet_attribute.GreetAttribute(
                        identifier=name,
                        start_line=start_line,
                        end_line=node.lineno,
                        start_column=self.__get_comment_first_col(start_line),
                        end_column=node.col_offset + len(name) + colls,
                        code="",
                        value=self.__extract_assign_value(node),
                        comment=ast.literal_eval(code.body[index - 1].value)
                    )
                    self.attributes.append(attribute)
            elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
                self.__extract(node)

    def __extract_assign_value(self, node):
        """
            Extracts the value of an assignment node.

            Args:
                node (ast.Assign): The assignment node to extract the value from.

            Returns:
                str: The extracted value as a string.

            Notes:
                - If the assignment value is a string, it is enclosed in double quotes.
                - If the assignment value is a number, it is extracted as is.
                - If the assignment value is a variable name, the variable name is returned.
                - If the assignment value is a function call, it is extracted using the __extract_call method.
                - If the assignment value is a list, set, tuple, or dictionary, it is extracted accordingly.
        """

        value = ""
        if isinstance(node, ast.Assign):
            if isinstance(node.value, ast.Str):
                expr = ast.Expr(node.value)
                ast.fix_missing_locations(expr)
                value = '"' + str(ast.literal_eval(expr.value)) + '"'
            elif isinstance(node.value, ast.Num):
                expr = ast.Expr(node.value)
                ast.fix_missing_locations(expr)
                value = ast.literal_eval(expr.value)
            elif isinstance(node.value, ast.Name):
                value = node.value.id
            elif isinstance(node.value, ast.Call):
                value = self.__extract_call(node.value)
            elif isinstance(node.value, ast.List):
                value = self.__extract_data_structures(
                    node.value.elts, Structures.LIST)
            elif isinstance(node.value, ast.Set):
                value = self.__extract_data_structures(
                    node.value.elts, Structures.SET)
            elif isinstance(node.value, ast.Tuple):
                value = self.__extract_data_structures(
                    node.value.elts, Structures.TUPLE)
            elif isinstance(node.value, ast.Dict):
                value = self.__extract_dictionary(node.value)
            return value

    def __process_keyword(self, keyword):
        value = ""
        if isinstance(keyword.value, ast.Str):
            expr = ast.Expr(keyword.value)
            ast.fix_missing_locations(expr)
            value += '"' + str(ast.literal_eval(expr.value)) + '"'
        elif isinstance(keyword.value, ast.Num):
            expr = ast.Expr(keyword.value)
            ast.fix_missing_locations(expr)
            value += str(ast.literal_eval(expr.value))
        if isinstance(keyword.value, ast.Name):
            value += keyword.value.id
        elif isinstance(keyword.value, ast.Call):
            value += self.__extract_call(keyword.value)
        elif isinstance(keyword.value, ast.List):
            value += self.__extract_data_structures(
                keyword.value.elts, Structures.LIST)
        elif isinstance(keyword.value, ast.Set):
            value += self.__extract_data_structures(
                keyword.value.elts, Structures.SET)
        elif isinstance(keyword.value, ast.Tuple):
            value += self.__extract_data_structures(
                keyword.value.elts, Structures.TUPLE)
        elif isinstance(keyword.value, ast.Dict):
            value += self.__extract_dictionary(keyword.value)

        return value

    def __process_arg(self, arg):
        args = ""
        if isinstance(arg, ast.Str):
            expr = ast.Expr(arg)
            ast.fix_missing_locations(expr)
            args += '"' + str(ast.literal_eval(expr.value)) + '"'
        elif isinstance(arg, ast.Num):
            expr = ast.Expr(arg)
            ast.fix_missing_locations(expr)
            args += str(ast.literal_eval(expr.value))
        if isinstance(arg, ast.Name):
            args += arg.id
        elif isinstance(arg, ast.Call):
            args += self.__extract_call(arg)
        elif isinstance(arg, ast.List):
            args += self.__extract_data_structures(
                arg.elts, Structures.LIST)
        elif isinstance(arg, ast.Set):
            args += self.__extract_data_structures(
                arg.elts, Structures.SET)
        elif isinstance(arg, ast.Tuple):
            args += self.__extract_data_structures(
                arg.elts, Structures.TUPLE)
        return args

    def __extract_call(self, node: ast.Call):
        """
            Extracts information about a function call node.

            Args:
                node (ast.Call): The function call node to extract information from.

            Returns:
                str: A string representation of the function call.

            Notes:
                - Extracts the function name and its arguments, including both positional arguments and keyword arguments.
                - Handles different types of arguments, such as strings, numbers, variables, function calls, lists, sets, tuples, and dictionaries.
        """

        func_name = ""
        if isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
        elif isinstance(node.func, ast.Call):
            func_name = self.__extract_call(node.func)
        else:
            func_name = node.func.id
        args = ""
        args_with_key = ""

        for i, arg in enumerate(node.args):
            args += self.__process_arg(arg)

            if isinstance(arg, ast.Dict):
                value = self.__extract_dictionary(arg)

            if i != len(node.args) - 1:
                args += ", "

        for i, keyword in enumerate(node.keywords):
            value = self.__process_keyword(keyword)

            args_with_key += str(keyword.arg) + "=" + str(value)

            if i != len(node.keywords) - 1:
                args_with_key += ", "

        call = func_name + "("
        if args != "":
            call += args

        if args_with_key != "":
            call += ", " + args_with_key

        call += ")"

        return call

    def __process_structure(self, item):
        res = ""
        if isinstance(item, ast.Str):
            expr = ast.Expr(item)
            ast.fix_missing_locations(expr)
            res += '"' + str(ast.literal_eval(expr.value)) + '"'
        elif isinstance(item, ast.Num):
            expr = ast.Expr(item)
            ast.fix_missing_locations(expr)
            res += str(ast.literal_eval(expr.value))
        elif isinstance(item, ast.Name):
            res += item.id
        elif isinstance(item, ast.Call):
            res += self.__extract_call(item)
        elif isinstance(item, ast.List):
            res += self.__extract_data_structures(
                item.elts, Structures.LIST)
        elif isinstance(item, ast.Set):
            res += self.__extract_data_structures(
                item.elts, Structures.SET)
        elif isinstance(item, ast.Tuple):
            res += self.__extract_data_structures(
                item.elts, Structures.TUPLE)

        return res

    def __extract_data_structures(self, structure, type):
        """
            Extracts data structures such as lists, sets, or tuples into a string representation.

            Args:
                structure (Union[ast.List, ast.Set, ast.Tuple]): The data structure node to extract.
                structure_type (str): The type of data structure (e.g., "list", "set", "tuple").

            Returns:
                str: A string representation of the extracted data structure.

            Notes:
                - Supports extracting elements from data structures, including strings, numbers, variables, function calls, nested data structures, and dictionaries.

        """
        res = ""
        if type == Structures.LIST:
            res += self.DATA_STRUCTURES_COLSURES["list_start"]
        elif type == Structures.SET:
            res += self.DATA_STRUCTURES_COLSURES["graph_start"]
        elif type == Structures.TUPLE:
            res += self.DATA_STRUCTURES_COLSURES["tuple_start"]

        for i, item in enumerate(structure):
            res += self.__process_structure(item)
            if isinstance(item, ast.Dict):
                value = self.__extract_dictionary(item)

            if i != len(structure) - 1:
                res += ", "

        if type == Structures.LIST:
            res += self.DATA_STRUCTURES_COLSURES["list_end"]
        elif type == Structures.SET:
            res += self.DATA_STRUCTURES_COLSURES["graph_end"]
        elif type == Structures.TUPLE:
            res += self.DATA_STRUCTURES_COLSURES["tuple_end"]

        return res

    def __extract_dictionary(self, dict):
        """
            Extracts a dictionary into a string representation.

            Args:
                dictionary_node (ast.Dict): The dictionary node to extract.

            Returns:
                str: A string representation of the extracted dictionary.

            Notes:
                - Supports extracting key-value pairs from the dictionary, handling different types of values, including strings, numbers, variables, function calls, nested data structures, and dictionaries.
        """

        dictionary = self.DATA_STRUCTURES_COLSURES["graph_start"]
        for i, item in enumerate(dict.values):
            value = ""
            if isinstance(item, ast.Str):
                expr = ast.Expr(item)
                ast.fix_missing_locations(expr)
                value = '"' + str(ast.literal_eval(expr.value)) + '"'
            elif isinstance(item, ast.Num):
                expr = ast.Expr(item)
                ast.fix_missing_locations(expr)
                value = str(ast.literal_eval(expr.value))
            elif isinstance(item, ast.Name):
                value = item.id
            elif isinstance(item, ast.Call):
                value = self.__extract_call(item)
            elif isinstance(item, ast.List):
                value = self.__extract_data_structures(
                    item.elts, Structures.LIST)
            elif isinstance(item, ast.Set):
                value = self.__extract_data_structures(
                    item.elts, Structures.SET)
            elif isinstance(item, ast.Tuple):
                value = self.__extract_data_structures(
                    item.elts, Structures.TUPLE)
            elif isinstance(item, ast.Dict):
                value = self.__extract_dictionary(item)

            dictionary += str(ast.literal_eval(
                dict.keys[i])) + ": " + str(value)

            if i != len(dict.values) - 1:
                dictionary += ", "

        dictionary += self.DATA_STRUCTURES_COLSURES["graph_end"]

        return dictionary

    def __extract_name(self, node):
        """
            Extracts the name of a variable from an assignment or attribute node.

            Args:
                node (Union[ast.Assign, ast.Expr]): The node from which to extract the variable name.

            Returns:
                Tuple[str, int]: A tuple containing the extracted variable name and column offset.
        """

        name = ""
        colls = 0
        if isinstance(node, ast.Assign):
            if isinstance(node.targets[0], ast.Attribute):
                name = node.targets[0].attr
                colls = 5
            elif isinstance(node.targets[0], ast.Tuple):
                name = self.__extract_data_structures(
                    node.targets[0].elts, Structures.TUPLE)
            elif isinstance(node.targets[0], ast.List):
                name = self.__extract_data_structures(
                    node.targets[0].elts, Structures.LIST)
            else:
                name = node.targets[0].id
        elif (isinstance(node, ast.Expr) and isinstance(node.value, ast.Attribute)):
            name = str(node.value.attr)
            colls = 5

        return name, colls

    def extract_function(self):
        """
            Extracts information about functions from the parsed code and adds them to the list of functions.
        """
        if self.code:
            for index, node in enumerate(ast.walk(self.code)):
                if isinstance(node, ast.FunctionDef):
                    args = []
                    for arg in node.args.args:
                        args.append(arg.arg)
                    if isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str):
                        p_function = greet_function.GreetFunction(
                            identifier=node.name,
                            start_line=node.lineno,
                            end_line=node.body[0].end_lineno,
                            start_column=node.col_offset + 4,
                            end_column=self.__get_comment_last_col(
                                node.body[0].lineno - 1),
                            code=self.__get_func_code(node),
                            args=args,
                            entities=[]
                        )
                        self.functions.append(p_function)

    def __get_func_code(self, function):
        """
            Retrieves the source code of a function from the opened file.

            Args:
                function (ast.FunctionDef): The FunctionDef node representing the function.

            Returns:
                str: The source code of the function as a string.

            Notes:
                - Determines the start and end lines of the function in the file based on the provided FunctionDef node.
                - Extracts the corresponding lines from the opened file to retrieve the function's source code.
        """

        start = function.lineno-1
        end = function.body[-1].lineno+1
        temp = ""
        splitted = self.opened_file.split('\n')
        for i, line in enumerate(splitted):
            if i in range(start, end):
                temp += line + '\n'
            elif i > end:
                break
        return temp

    def __get_comment_last_col(self, line_number):
        splitted = self.opened_file.split('\n')
        return len(splitted[line_number]) - 1

    def __get_comment_first_col(self, start_line):
        splitted = self.opened_file.split('\n')
        return splitted[start_line - 1].find('"')
