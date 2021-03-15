def get_class_attribute_names(entity_class):
    names = []
    for attribute_item in entity_class.attributes:
        names.append(attribute_item.name)
    return names


def get_all_class_fields(entity_class):
    items = []
    for attribute_item in entity_class.attributes:
        items.append(attribute_item)
    for method_item in entity_class.methods:
        for variable_item in method_item.variables:
            items.append(variable_item)
        for parameter_item in method_item.parameters:
            items.append(parameter_item)

    return items


def get_all_exception_throws(method):
    return method.xpath('.//src:throw', namespaces={'src': 'http://www.srcML.org/srcML/src'})


def get_all_return_statements(method):
    return method.xpath('.//src:return', namespaces={'src': 'http://www.srcML.org/srcML/src'})


def get_all_comments(method):
    return method.xpath('.//src:comment', namespaces={'src': 'http://www.srcML.org/srcML/src'})


def get_comment_with_text(method, text):
    return method.xpath('.//src:comment[contains(text(),\'' + text + '\')]',
                        namespaces={'src': 'http://www.srcML.org/srcML/src'})


def get_all_conditional_statements(method):
    statements = {}
    statements_total = 0

    statement_while = method.xpath('.//src:while', namespaces={'src': 'http://www.srcML.org/srcML/src'})
    statements['while'] = statement_while
    statements_total += len(statement_while)

    statement_do = method.xpath('.//src:do', namespaces={'src': 'http://www.srcML.org/srcML/src'})
    statements['do'] = statement_do
    statements_total += len(statement_do)

    statement_for = method.xpath('.//src:for', namespaces={'src': 'http://www.srcML.org/srcML/src'})
    statements['for'] = statement_for
    statements_total += len(statement_for)

    statement_if = method.xpath('.//src:if', namespaces={'src': 'http://www.srcML.org/srcML/src'})
    statements['if'] = statement_if
    statements_total += len(statement_if)

    statement_if2 = method.xpath('.//src:if_stmt', namespaces={'src': 'http://www.srcML.org/srcML/src'})
    statements['if_stmt'] = statement_if2
    statements_total += len(statement_if2)

    statement_switch = method.xpath('.//src:switch', namespaces={'src': 'http://www.srcML.org/srcML/src'})
    statements['switch'] = statement_switch
    statements_total += len(statement_switch)

    return statements, statements_total
