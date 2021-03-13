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

    def set_file_type(self, file_type):
        if file_type == 1:
            self.file_type = FileType.Test
        elif file_type == 2:
            self.file_type = FileType.NonTest
        else:
            self.file_type = FileType.Unknown

    def construct_hierarchy(self):
        tree = etree.fromstring(self.srcml)
        class_list = tree.xpath('//src:class', namespaces={'src': 'http://www.srcML.org/srcML/src'})
        for class_item in class_list:
            class_name = class_item.xpath('./src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
            model_class = Class(class_name.text, class_item)

            attribute_list = class_item.xpath('*/src:decl_stmt/src:decl', namespaces={'src': 'http://www.srcML.org/srcML/src'})
            for i, attribute_item in enumerate(attribute_list):
                attribute_name = attribute_item.xpath('./src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
                attribute_type = attribute_item.xpath('./src:type/src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})

                if len(attribute_type) != 0:
                    attribute_type = attribute_type[0]
                    if attribute_type.text == None:
                        attribute_type = attribute_item.xpath('./src:type/src:name/src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
                    model_attribute = Attribute(attribute_type.text, attribute_name.text,model_class.name + "." + attribute_name.text, attribute_item)
                else:# capture the attribute's type when the attributes are declared in groups (e.g., String app, testFilePath;)
                    if attribute_item.xpath('./src:type/@ref', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0] == 'prev':
                        attribute_type = model_class.attributes[-1].type
                        model_attribute = Attribute(attribute_type, attribute_name.text, model_class.name + "." + attribute_name.text, attribute_item)

                model_class.attributes.append(model_attribute)

            method_list = class_item.xpath('*/src:function', namespaces={'src': 'http://www.srcML.org/srcML/src'})
            for method_item in method_list:
                method_name = method_item.xpath('./src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
                method_annotation = method_item.xpath('./src:annotation/src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})
                method_annotation = [''.join(x.text) for x in method_annotation]
                method_return_type = method_item.xpath('./src:type/src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
                if method_return_type.text is None:
                    method_return_type = method_item.xpath('./src:type/src:name/src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]

                model_method = Method(method_name.text, method_annotation, model_class.name, method_return_type.text, method_item)

                parameter_list = method_item.xpath('*/src:parameter/src:decl', namespaces={'src': 'http://www.srcML.org/srcML/src'})
                for parameter_item in parameter_list:
                    parameter_name = parameter_item.xpath('./src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
                    parameter_type = parameter_item.xpath('./src:type/src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})

                    if len(parameter_type) != 0:
                        parameter_type = parameter_type[0]
                        if parameter_type.text == None:
                            parameter_type = parameter_item.xpath('./src:type/src:name/src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
                        model_parameter = Parameter(parameter_type.text, parameter_name.text, parameter_item)

                    model_method.parameters.append(model_parameter)

                for parameter_item in model_method.parameters:
                    parameter_item.set_parent_name(model_method.get_fully_qualified_name())

                variable_list = method_item.xpath('*//src:decl_stmt/src:decl', namespaces={'src': 'http://www.srcML.org/srcML/src'})
                for variable_item in variable_list:
                    variable_name = variable_item.xpath('./src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
                    variable_type = variable_item.xpath('./src:type/src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})

                    if len(variable_type) != 0:
                        variable_type = variable_type[0]
                        if variable_type.text == None:
                            variable_type = variable_item.xpath('./src:type/src:name/src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
                        model_variable = Variable(variable_type.text, variable_name.text, variable_item)
                    else:  # capture the variable's type when the variables are declared in groups (e.g., String app, testFilePath;)
                        if variable_item.xpath('./src:type/@ref', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0] == 'prev':
                            variable_type = model_method.variables[-1].type
                            model_variable = Variable(variable_type, variable_name.text, variable_item)

                    model_method.variables.append(model_variable)

                for variable_item in model_method.variables:
                    variable_item.set_parent_name(model_method.get_fully_qualified_name())

                model_class.methods.append((model_method))

            self.classes.append(model_class)

        return self.classes
