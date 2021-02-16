import antlr4
from antlr4 import *
from ANTLR_JAVA import JavaParser, JavaLexer

code = open('C:\\Projects\\MSR2021_Challenge\\Java\\src\\org\\scanl\\Main.java', 'r').read()
lexer = JavaLexer.JavaLexer(antlr4.InputStream(code))
stream = antlr4.CommonTokenStream(lexer)
parser = JavaParser.JavaParser(stream)
tree = parser.compilationUnit()
print(tree.toStringTree(recog=parser))
print('----')