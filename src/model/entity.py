from typing import List, cast
from lxml import etree

from src.common import enum
from src.common.enum import FileType, LanguageType, IdentifierType
from src.common.error_handler import handle_error, ErrorSeverity
from src.common.testing_list import get_testing_packages
from src.model.identifier import Class, Attribute, Method, Parameter, Variable, Property


class Entity:

    SRCML_NS_URL = "http://www.srcML.org/srcML/src"
    SRCML_SRCNAME_XPATH = "src:name"
    SRCML_SRCTYPE_XPATH = "src:type"
    SRCML_PRECEDINGSIBLING_XPATH = '\']/preceding-sibling::*[1][self::src:comment]'

    def __init__(self):
        self.srcml = None
        self.name = None
        self.path = None
        self.classes = []
        self.type = None
        self.file_type = None
        self.junit = None
        self.language = None

    def set_file_type(self, file_type):
        """
            Set the file type.

            Args:
                file_type (Union[int, FileType]): The file type to set
                    - If `file_type` is 1, the file type will be set to FileType.Test.
                    - If `file_type` is 2, the file type will be set to FileType.NonTest.
                    - Otherwise, the file type will be set to FileType.Unknown.
        """

        if file_type == 1:
            self.file_type = FileType.Test
        elif file_type == 2:
            self.file_type = FileType.NonTest
        else:
            self.file_type = FileType.Unknown

    def is_using_testing_package(self, source: etree._ElementTree) -> None:
        """
            Determine if the source is using testing packages and set the file type accordingly.

            Args:
                source (etree._ElementTree): The source code represented as an ElementTree.

            Returns:
                None: This function modifies the `self.file_type` attribute based on the analysis.
        """
        if self.file_type is not enum.FileType.Unknown:
            return

        self.file_type = enum.FileType.NonTest
        testing_packages = get_testing_packages(None, self.language)

        if self.language == enum.LanguageType.Java:
            all_imports = source.xpath(
                f'//src:import/{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})
            for i in range(len(all_imports)+1):
                partial_name = source.xpath(
                    '//src:import['+str(i)+f']/{self.SRCML_SRCNAME_XPATH}//text()', namespaces={'src': self.SRCML_NS_URL})
                if ''.join(partial_name) in cast(List[str], testing_packages):
                    self.file_type = enum.FileType.Test
                    break

        if self.language == enum.LanguageType.CSharp:
            all_imports = source.xpath(
                f'//src:using/{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})
            for i in range(len(all_imports)+1):
                partial_name = source.xpath(
                    '//src:using['+str(i)+f']/{self.SRCML_SRCNAME_XPATH}//text()', namespaces={'src': self.SRCML_NS_URL})
                if ''.join(partial_name) in cast(List[str], testing_packages):
                    self.file_type = enum.FileType.Test
                    break

    def construct_hierarchy(self):
        tree = etree.fromstring(self.srcml, None)
        self.language = LanguageType.get_type(tree.xpath(
            '//src:unit/@language', namespaces={'src': self.SRCML_NS_URL})[0])
    ## ----------------------------------------------------------------------------------------------------------------##
        self.is_using_testing_package(tree)
    ## ----------------------------------------------------------------------------------------------------------------##
        class_list = tree.xpath(
            '//src:class', namespaces={'src': self.SRCML_NS_URL})
        for class_item in class_list:
            if len(class_item.xpath(f'./{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})) == 0:
                continue
            class_name = class_item.xpath(
                f'./{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})[0]
            if class_name.text is None:
                class_name = class_item.xpath(
                    f'./{self.SRCML_SRCNAME_XPATH}/{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})[0]
            model_class = Class(class_name.text, class_item)
            class_comment = tree.xpath(
                f'//src:class[{self.SRCML_SRCNAME_XPATH}=\''+model_class.name + self.SRCML_PRECEDINGSIBLING_XPATH, namespaces={'src': self.SRCML_NS_URL})
            if len(class_comment) > 0:
                model_class.set_block_comment(class_comment[0].text)
            else:
                model_class.set_block_comment(None)
    ## ----------------------------------------------------------------------------------------------------------------##
            attribute_list = class_item.xpath(
                '*/src:decl_stmt/src:decl', namespaces={'src': self.SRCML_NS_URL})
            for i, attribute_item in enumerate(attribute_list):
                try:
                    attribute_specifier = attribute_item.xpath(
                        f'./{self.SRCML_SRCTYPE_XPATH}/src:specifier', namespaces={'src': self.SRCML_NS_URL})
                    if len(attribute_specifier) == 0:
                        attribute_specifier = None
                    else:
                        attribute_specifier = attribute_specifier[0].text
                    attribute_name = attribute_item.xpath(
                        f'./{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})[0]
                    if attribute_name.text is None:
                        attribute_name = attribute_item.xpath(
                            f'./{self.SRCML_SRCNAME_XPATH}/{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})[0]
                    attribute_type = attribute_item.xpath(
                        f'./{self.SRCML_SRCTYPE_XPATH}/{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})
                    attribute_type_array = False
                    attribute_type_generic = False
                    model_attribute = None
                    if len(attribute_type) != 0:
                        attribute_type = attribute_type[0]
                        if attribute_type.text == None:
                            attribute_type = attribute_item.xpath(
                                f'./{self.SRCML_SRCTYPE_XPATH}/{self.SRCML_SRCNAME_XPATH}/{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})[0]
                            if attribute_type.text == None:
                                attribute_type = attribute_item.xpath(
                                    f'./{self.SRCML_SRCTYPE_XPATH}/{self.SRCML_SRCNAME_XPATH}/{self.SRCML_SRCNAME_XPATH}/{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})[0]
                            attribute_array = attribute_item.xpath(
                                f'./{self.SRCML_SRCTYPE_XPATH}/{self.SRCML_SRCNAME_XPATH}/src:index', namespaces={'src': self.SRCML_NS_URL})
                            attribute_type_generic = True
                            if len(attribute_array) != 0:
                                attribute_type_array = True
                        model_attribute = Attribute(attribute_specifier, attribute_type.text, attribute_name.text,
                                                    model_class.name, attribute_type_array, attribute_type_generic, attribute_item)

                        attribute_comment = class_item.xpath(f'//src:decl_stmt[src:decl/{self.SRCML_SRCTYPE_XPATH}/{self.SRCML_SRCNAME_XPATH}=\''+attribute_type.text+f'\' and src:decl/{self.SRCML_SRCNAME_XPATH}=\'' +
                                                             attribute_name.text + self.SRCML_PRECEDINGSIBLING_XPATH, namespaces={'src': self.SRCML_NS_URL})
                        if len(attribute_comment) > 0:
                            model_attribute.set_block_comment(
                                attribute_comment[0].text)
                        else:
                            model_attribute.set_block_comment(None)

                    # capture the attribute's type when the attributes are declared in groups (e.g., String app, testFilePath;)
                    else:
                        if attribute_item.xpath(f'./{self.SRCML_SRCTYPE_XPATH}/@ref', namespaces={'src': self.SRCML_NS_URL})[0] == 'prev':
                            attribute_specifier = model_class.attributes[-1].specifier
                            attribute_type = model_class.attributes[-1].type
                            attribute_type_array = model_class.attributes[-1].is_array
                            attribute_comment = model_class.attributes[-1].block_comment
                            attribute_type_generic = model_class.attributes[-1].type_is_generic
                            model_attribute = Attribute(attribute_specifier, attribute_type, attribute_name.text,
                                                        model_class.name, attribute_type_array, attribute_type_generic, attribute_item)
                            model_attribute.set_block_comment(
                                attribute_comment)

                    model_class.attributes.append(
                        cast(Attribute, model_attribute)
                    )
                except Exception as e:
                    error_message = "Error encountered parsing attribute in class %s in file %s" % (
                        model_class.name, self.path)
                    handle_error('Hierarchy', error_message,
                                 ErrorSeverity.Error, False, e)
                    continue

            method_list = class_item.xpath(
                '*/src:function', namespaces={'src': self.SRCML_NS_URL})
            for method_item in method_list:
                try:
                    method_specifier = method_item.xpath(
                        f'./{self.SRCML_SRCTYPE_XPATH}/src:specifier', namespaces={'src': self.SRCML_NS_URL})
                    if len(method_specifier) == 0:
                        method_specifier = None
                    else:
                        method_specifier = method_specifier[0].text
                    method_name = method_item.xpath(
                        f'./{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})[0]
                    if method_name.text is None:
                        method_name = method_item.xpath(
                            f'./{self.SRCML_SRCNAME_XPATH}/{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})[0]
                    method_annotation = method_item.xpath(
                        f'./src:annotation/{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})
                    method_annotation = [''.join(x.text)
                                         for x in method_annotation]
                    method_return_type = method_item.xpath(
                        f'./{self.SRCML_SRCTYPE_XPATH}/{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})[0]
                    method_type_array = False
                    if method_return_type.text is None:
                        method_return_type = method_item.xpath(
                            f'./{self.SRCML_SRCTYPE_XPATH}/{self.SRCML_SRCNAME_XPATH}/{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})[0]
                        method_array = method_item.xpath(
                            f'./{self.SRCML_SRCTYPE_XPATH}/{self.SRCML_SRCNAME_XPATH}/src:index', namespaces={'src': self.SRCML_NS_URL})
                        if len(method_array) != 0:
                            method_type_array = True

                    model_method = Method(method_specifier, method_name.text, method_annotation,
                                          model_class.name, method_return_type.text, method_type_array, method_item)
        ## ----------------------------------------------------------------------------------------------------------------##
                    parameter_list = method_item.xpath(
                        '*/src:parameter/src:decl', namespaces={'src': self.SRCML_NS_URL})
                    for parameter_item in parameter_list:
                        if len(parameter_item.xpath(f'./{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})) != 0:
                            parameter_name = parameter_item.xpath(
                                f'./{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})[0]
                        else:
                            if len(parameter_item.xpath(f'./{self.SRCML_SRCNAME_XPATH}/{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})) != 0:
                                parameter_name = parameter_item.xpath(
                                    f'./{self.SRCML_SRCNAME_XPATH}/{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})[0]
                            else:
                                continue

                        if parameter_name.text is None:
                            parameter_name = parameter_item.xpath(
                                f'./{self.SRCML_SRCNAME_XPATH}/{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})[0]

                        parameter_type = parameter_item.xpath(
                            f'./{self.SRCML_SRCTYPE_XPATH}/{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})
                        parameter_type_array = False
                        parameter_type_generic = False
                        model_parameter = None
                        if len(parameter_type) != 0:
                            parameter_type = parameter_type[0]
                            if parameter_type.text == None:
                                parameter_type = parameter_item.xpath(
                                    f'./{self.SRCML_SRCTYPE_XPATH}/{self.SRCML_SRCNAME_XPATH}/{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})[0]
                                parameter_array = parameter_item.xpath(
                                    f'./{self.SRCML_SRCTYPE_XPATH}/{self.SRCML_SRCNAME_XPATH}/src:index', namespaces={'src': self.SRCML_NS_URL})
                                parameter_type_generic = True
                                if len(parameter_array) != 0:
                                    parameter_type_array = True

                            model_parameter = Parameter(
                                parameter_type.text,
                                parameter_name.text,
                                parameter_type_array,
                                parameter_type_generic,
                                parameter_item
                            )

                        model_method.parameters.append(
                            cast(Parameter, model_parameter)
                        )

                    for parameter_item in model_method.parameters:
                        parameter_item.set_parent_name(
                            model_method.get_fully_qualified_name())

                    ### get (header/block) comments for the method ###
                    xpath_strings = []
                    for num, parameter in enumerate(model_method.parameters, start=1):
                        if parameter.type_is_generic:
                            xpath_strings.append("(src:parameter_list/src:parameter["+str(num)+f"]/src:decl/{self.SRCML_SRCNAME_XPATH}='"+parameter.name+"' and src:parameter_list/src:parameter["+str(
                                num)+f"]/src:decl/{self.SRCML_SRCTYPE_XPATH}/{self.SRCML_SRCNAME_XPATH}/{self.SRCML_SRCNAME_XPATH}='"+parameter.type+"')")
                        else:
                            xpath_strings.append("(src:parameter_list/src:parameter["+str(num)+f"]/src:decl/{self.SRCML_SRCNAME_XPATH}='"+parameter.name +
                                                 "' and src:parameter_list/src:parameter["+str(num)+f"]/src:decl/{self.SRCML_SRCTYPE_XPATH}/{self.SRCML_SRCNAME_XPATH}='"+parameter.type+"')")
                    xpath_string = f"//src:function[{self.SRCML_SRCNAME_XPATH}='" + \
                        model_method.name+"'"
                    if len(xpath_strings) != 0:
                        xpath_string = xpath_string + ' and ' + \
                            ' and '.join(
                                xpath_strings) + "]/preceding-sibling::*[1][self::src:comment]"
                    else:
                        xpath_string = xpath_string + \
                            "]/preceding-sibling::*[1][self::src:comment]"
                    method_comment = class_item.xpath(xpath_string, namespaces={
                                                      'src': self.SRCML_NS_URL})
                    if len(method_comment) > 0:
                        model_method.set_block_comment(method_comment[0].text)
                    else:
                        model_method.set_block_comment(None)
        ## ----------------------------------------------------------------------------------------------------------------##
                    variable_list = method_item.xpath(
                        '*//src:decl_stmt/src:decl', namespaces={'src': self.SRCML_NS_URL})
                    for variable_item in variable_list:
                        variable_specifier = variable_item.xpath(
                            f'./{self.SRCML_SRCTYPE_XPATH}/src:specifier', namespaces={'src': self.SRCML_NS_URL})
                        if len(variable_specifier) == 0:
                            variable_specifier = None
                        else:
                            variable_specifier = variable_specifier[0].text

                        if len(variable_item.xpath(f'./{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})) != 0:
                            variable_name = variable_item.xpath(
                                f'./{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})[0]
                        else:
                            if len(variable_item.xpath(f'./{self.SRCML_SRCNAME_XPATH}/{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})) != 0:
                                variable_name = variable_item.xpath(
                                    f'./{self.SRCML_SRCNAME_XPATH}/{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})[0]
                            else:
                                continue

                        if variable_name.text is None:
                            variable_name = variable_item.xpath(
                                f'./{self.SRCML_SRCNAME_XPATH}/{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})[0]

                        variable_type = variable_item.xpath(
                            f'./{self.SRCML_SRCTYPE_XPATH}/{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})
                        variable_type_array = False
                        variable_type_generic = False
                        model_variable = None
                        if len(variable_type) != 0:
                            variable_type = variable_type[0]
                            if variable_type.text == None:
                                variable_type = variable_item.xpath(
                                    f'./{self.SRCML_SRCTYPE_XPATH}/{self.SRCML_SRCNAME_XPATH}/{self.SRCML_SRCNAME_XPATH}', namespaces={'src': self.SRCML_NS_URL})[0]
                                variable_array = variable_item.xpath(
                                    f'./{self.SRCML_SRCTYPE_XPATH}/{self.SRCML_SRCNAME_XPATH}/src:index', namespaces={'src': self.SRCML_NS_URL})
                                variable_type_generic = True
                                if len(variable_array) != 0:
                                    variable_type_array = True
                            model_variable = Variable(
                                variable_specifier, variable_type.text, variable_name.text, variable_type_array, variable_type_generic, variable_item)
                            variable_comment = method_item.xpath(f'//src:decl_stmt[src:decl/{self.SRCML_SRCTYPE_XPATH}/{self.SRCML_SRCNAME_XPATH}=\'' + variable_type.text + f'\' and src:decl/{self.SRCML_SRCNAME_XPATH}=\'' +
                                                                 variable_name.text + self.SRCML_PRECEDINGSIBLING_XPATH, namespaces={'src': self.SRCML_NS_URL})
                            if len(variable_comment) > 0:
                                model_variable.set_block_comment(
                                    variable_comment[0].text)
                            else:
                                model_variable.set_block_comment(None)

                        # capture the variable's type when the variables are declared in groups (e.g., String app, testFilePath;)
                        else:
                            if variable_item.xpath('./{self.SRCML_SRCTYPE_XPATH}/@ref', namespaces={'src': self.SRCML_NS_URL})[0] == 'prev':
                                variable_specifier = model_method.variables[-1].specifier
                                variable_type = model_method.variables[-1].type
                                variable_type_array = model_method.variables[-1].is_array
                                variable_comment = model_method.variables[-1].block_comment
                                variable_type_generic = model_method.variables[-1].type_is_generic
                                model_variable = Variable(
                                    variable_specifier, variable_type, variable_name.text, variable_type_array, variable_type_generic, variable_item)
                                model_variable.set_block_comment(
                                    variable_comment)

                        model_method.variables.append(
                            cast(Variable, model_variable))

                    for variable_item in model_method.variables:
                        variable_item.set_parent_name(
                            model_method.get_fully_qualified_name())

                    model_class.methods.append((model_method))
                except Exception as e:
                    error_message = "Error encountered parsing method in class %s in file %s" % (
                        model_class.name, self.path)
                    handle_error('Hierarchy', error_message,
                                 ErrorSeverity.Error, False, e)
                    continue

            self.classes.append(model_class)

        return self.classes
