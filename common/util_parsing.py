def get_all_return_statements(code):
    return code.xpath('.//src:return', namespaces={'src': 'http://www.srcML.org/srcML/src'})
