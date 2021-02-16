from lxml import etree

from model.identifier import Class, Attribute, Method, Parameter, Variable


class Entity:

    def __init__(self):
        self.srcml = None
        self.name = None
        self.path = None
        self.classes = []
        self.type = None

    def construct_hierarchy(self):
        tree = etree.fromstring(self.srcml)
        class_list = tree.xpath('//src:class', namespaces={'src': 'http://www.srcML.org/srcML/src'})
        for class_item in class_list:
            class_name = class_item.xpath('./src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
            model_class = Class(class_name.text, class_item)

            attribute_list = class_item.xpath('*/src:decl_stmt/src:decl', namespaces={'src': 'http://www.srcML.org/srcML/src'})
            for attribute_item in attribute_list:
                attribute_name = attribute_item.xpath('./src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
                attribute_type = attribute_item.xpath('./src:type/src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
                model_attribute = Attribute(attribute_type.text, attribute_name.text, model_class.name+"."+attribute_name.text,  attribute_item)
                model_class.attribute.append((model_attribute))

            method_list = class_item.xpath('*/src:function', namespaces={'src': 'http://www.srcML.org/srcML/src'})
            for method_item in method_list:
                method_name = method_item.xpath('./src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
                method_annotation = method_item.xpath('./src:annotation/src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})
                method_annotation = [''.join(x.text) for x in method_annotation]

                model_method = Method(method_name.text, method_annotation, model_class.name, method_item)

                parameter_list = method_item.xpath('*/src:parameter/src:decl', namespaces={'src': 'http://www.srcML.org/srcML/src'})
                for parameter_item in parameter_list:
                    parameter_name = parameter_item.xpath('./src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
                    parameter_type = parameter_item.xpath('./src:type/src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
                    model_parameter = Parameter(parameter_type.text, parameter_name.text, parameter_item)
                    model_method.parameters.append(model_parameter)

                for parameter_item in model_method.parameters:
                    parameter_item.set_parent_name(model_method.get_fully_qualified_name())

                variable_list = method_item.xpath('*//src:decl_stmt/src:decl', namespaces={'src': 'http://www.srcML.org/srcML/src'})
                for variable_item in variable_list:
                    variable_name = variable_item.xpath('./src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
                    variable_type = variable_item.xpath('./src:type/src:name', namespaces={'src': 'http://www.srcML.org/srcML/src'})[0]
                    model_variable = Variable(variable_type.text, variable_name.text, variable_item)
                    model_method.variables.append(model_variable)

                for variable_item in model_method.variables:
                    variable_item.set_parent_name(model_method.get_fully_qualified_name())

                model_class.methods.append((model_method))

            self.classes.append(model_class)

        return self.classes
