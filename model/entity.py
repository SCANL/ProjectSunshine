from lxml import etree

from model.file_type import FileType
from model.identifier import Class, Attribute, Method, Parameter, Variable


class Entity:

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
        if file_type == 1:
            self.file_type = FileType.Test
        elif file_type == 2:
            self.file_type = FileType.NonTest
        else:
            self.file_type = FileType.Unknown

    def construct_hierarchy(self):
        tree = etree.fromstring(self.srcml)
        self.language = tree.xpath('//src:unit/@language',namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
    ##----------------------------------------------------------------------------------------------------------------##
        class_list = tree.xpath('//src:class', namespaces={'src': 'http://www.srcML.org/srcML/src'})
        for class_item in class_list:
            class_name = class_item.xpath('./src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
            model_class = Class(class_name.text, class_item)
            class_comment = tree.xpath('//src:class[src:name=\''+model_class.name+'\']/preceding-sibling::*[1][self::src:comment]',namespaces={'src': 'http://www.srcML.org/srcML/src'})
            if len(class_comment) > 0:
                model_class.set_block_comment(class_comment[0].text)
            else:
                model_class.set_block_comment(None)
    ##----------------------------------------------------------------------------------------------------------------##
            attribute_list = class_item.xpath('*/src:decl_stmt/src:decl', namespaces={'src': 'http://www.srcML.org/srcML/src'})
            for i, attribute_item in enumerate(attribute_list):
                attribute_name = attribute_item.xpath('./src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
                attribute_type = attribute_item.xpath('./src:type/src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})
                attribute_type_array = False
                attribute_type_generic = False

                if len(attribute_type) != 0:
                    attribute_type = attribute_type[0]
                    if attribute_type.text == None:
                        attribute_type = attribute_item.xpath('./src:type/src:name/src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
                        attribute_array = attribute_item.xpath('./src:type/src:name/src:index', namespaces={'src': 'http://www.srcML.org/srcML/src'})
                        attribute_type_generic = True
                        if len(attribute_array) != 0:
                            attribute_type_array = True
                    model_attribute = Attribute(attribute_type.text, attribute_name.text,model_class.name, attribute_type_array, attribute_type_generic, attribute_item)
                    attribute_comment = class_item.xpath('//src:decl_stmt[src:decl/src:type/src:name=\''+attribute_type.text+'\' and src:decl/src:name=\''+attribute_name.text+'\']/preceding-sibling::*[1][self::src:comment]', namespaces={'src': 'http://www.srcML.org/srcML/src'})
                    if len(attribute_comment) > 0:
                        model_attribute.set_block_comment(attribute_comment[0].text)
                    else:
                        model_attribute.set_block_comment(None)

                else:# capture the attribute's type when the attributes are declared in groups (e.g., String app, testFilePath;)
                    if attribute_item.xpath('./src:type/@ref', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0] == 'prev':
                        attribute_type = model_class.attributes[-1].type
                        attribute_type_array = model_class.attributes[-1].is_array
                        attribute_comment = model_class.attributes[-1].block_comment
                        attribute_type_generic = model_class.attributes[-1].type_is_generic
                        model_attribute = Attribute(attribute_type, attribute_name.text, model_class.name, attribute_type_array, attribute_type_generic, attribute_item)
                        model_attribute.set_block_comment(attribute_comment)

                model_class.attributes.append(model_attribute)
    ##----------------------------------------------------------------------------------------------------------------##
            method_list = class_item.xpath('*/src:function', namespaces={'src': 'http://www.srcML.org/srcML/src'})
            for method_item in method_list:
                method_name = method_item.xpath('./src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
                method_annotation = method_item.xpath('./src:annotation/src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})
                method_annotation = [''.join(x.text) for x in method_annotation]
                method_return_type = method_item.xpath('./src:type/src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
                method_type_array = False
                if method_return_type.text is None:
                    method_return_type = method_item.xpath('./src:type/src:name/src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
                    method_array = method_item.xpath('./src:type/src:name/src:index', namespaces={'src': 'http://www.srcML.org/srcML/src'})
                    if len(method_array) != 0:
                        method_type_array = True

                model_method = Method(method_name.text, method_annotation, model_class.name, method_return_type.text, method_type_array, method_item)
    ##----------------------------------------------------------------------------------------------------------------##
                parameter_list = method_item.xpath('*/src:parameter/src:decl', namespaces={'src': 'http://www.srcML.org/srcML/src'})
                for parameter_item in parameter_list:
                    parameter_name = parameter_item.xpath('./src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
                    parameter_type = parameter_item.xpath('./src:type/src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})
                    parameter_type_array = False
                    parameter_type_generic = False
                    if len(parameter_type) != 0:
                        parameter_type = parameter_type[0]
                        if parameter_type.text == None:
                            parameter_type = parameter_item.xpath('./src:type/src:name/src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
                            parameter_array = parameter_item.xpath('./src:type/src:name/src:index', namespaces={'src': 'http://www.srcML.org/srcML/src'})
                            parameter_type_generic = True
                            if len(parameter_array) != 0:
                                parameter_type_array = True

                        model_parameter = Parameter(parameter_type.text, parameter_name.text, parameter_type_array, parameter_type_generic, parameter_item)

                    model_method.parameters.append(model_parameter)

                for parameter_item in model_method.parameters:
                    parameter_item.set_parent_name(model_method.get_fully_qualified_name())

                ### get (header/block) comments for the method ###
                xpath_strings=[]
                for num, parameter in enumerate(model_method.parameters, start=1):
                    if parameter.type_is_generic:
                        xpath_strings.append("(src:parameter_list/src:parameter["+str(num)+"]/src:decl/src:name='"+parameter.name+"' and src:parameter_list/src:parameter["+str(num)+"]/src:decl/src:type/src:name/src:name='"+parameter.type+"')")
                    else:
                        xpath_strings.append("(src:parameter_list/src:parameter["+str(num)+"]/src:decl/src:name='"+parameter.name+"' and src:parameter_list/src:parameter["+str(num)+"]/src:decl/src:type/src:name='"+parameter.type+"')")
                xpath_string = "//src:function[src:name='"+model_method.name+"'"
                if len(xpath_strings) != 0:
                    xpath_string = xpath_string + ' and ' + ' and '.join(xpath_strings) + "]/preceding-sibling::*[1][self::src:comment]"
                else:
                    xpath_string = xpath_string + "]/preceding-sibling::*[1][self::src:comment]"
                method_comment = class_item.xpath(xpath_string,namespaces={'src': 'http://www.srcML.org/srcML/src'})
                if len(method_comment) > 0:
                    model_method.set_block_comment(method_comment[0].text)
                else:
                    model_method.set_block_comment(None)
    ##----------------------------------------------------------------------------------------------------------------##
                variable_list = method_item.xpath('*//src:decl_stmt/src:decl', namespaces={'src': 'http://www.srcML.org/srcML/src'})
                for variable_item in variable_list:
                    variable_name = variable_item.xpath('./src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
                    variable_type = variable_item.xpath('./src:type/src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})
                    variable_type_array = False
                    variable_type_generic = False

                    if len(variable_type) != 0:
                        variable_type = variable_type[0]
                        if variable_type.text == None:
                            variable_type = variable_item.xpath('./src:type/src:name/src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
                            variable_array = variable_item.xpath('./src:type/src:name/src:index', namespaces={'src': 'http://www.srcML.org/srcML/src'})
                            variable_type_generic = True
                            if len(variable_array) != 0:
                                variable_type_array = True
                        model_variable = Variable(variable_type.text, variable_name.text, variable_type_array, variable_type_generic, variable_item)
                        variable_comment = method_item.xpath('//src:decl_stmt[src:decl/src:type/src:name=\'' + variable_type.text + '\' and src:decl/src:name=\'' + variable_name.text + '\']/preceding-sibling::*[1][self::src:comment]', namespaces={'src': 'http://www.srcML.org/srcML/src'})
                        if len(variable_comment) > 0:
                            model_variable.set_block_comment(variable_comment[0].text)
                        else:
                            model_variable.set_block_comment(None)

                    else:  # capture the variable's type when the variables are declared in groups (e.g., String app, testFilePath;)
                        if variable_item.xpath('./src:type/@ref', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0] == 'prev':
                            variable_type = model_method.variables[-1].type
                            variable_type_array = model_method.variables[-1].is_array
                            variable_comment = model_method.variables[-1].block_comment
                            variable_type_generic = model_method.variables[-1].type_is_generic
                            model_variable = Variable(variable_type, variable_name.text, variable_type_array, variable_type_generic, variable_item)
                            model_variable.set_block_comment(variable_comment)

                    model_method.variables.append(model_variable)

                for variable_item in model_method.variables:
                    variable_item.set_parent_name(model_method.get_fully_qualified_name())

                model_class.methods.append((model_method))

            self.classes.append(model_class)

        return self.classes
