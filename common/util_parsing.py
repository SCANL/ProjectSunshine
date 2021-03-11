def get_all_return_statements(code):
    return code.xpath('.//src:return', namespaces={'src': 'http://www.srcML.org/srcML/src'})


def get_all_conditional_statements(code):
    statements = {}
    statements_total = 0

    statement_while = code.xpath('.//src:while', namespaces={'src': 'http://www.srcML.org/srcML/src'})
    statements['while'] = statement_while
    statements_total += len(statement_while)

    statement_do = code.xpath('.//src:do', namespaces={'src': 'http://www.srcML.org/srcML/src'})
    statements['do'] = statement_do
    statements_total += len(statement_do)

    statement_for = code.xpath('.//src:for', namespaces={'src': 'http://www.srcML.org/srcML/src'})
    statements['for'] = statement_for
    statements_total += len(statement_for)

    statement_if = code.xpath('.//src:if', namespaces={'src': 'http://www.srcML.org/srcML/src'})
    statements['if'] = statement_if
    statements_total += len(statement_if)

    statement_if2 = code.xpath('.//src:if_stmt', namespaces={'src': 'http://www.srcML.org/srcML/src'})
    statements['if_stmt'] = statement_if2
    statements_total += len(statement_if2)

    statement_switch = code.xpath('.//src:switch', namespaces={'src': 'http://www.srcML.org/srcML/src'})
    statements['switch'] = statement_switch
    statements_total += len(statement_switch)

    return statements, statements_total
