import pytest
from src.common.types_list import get_primitive_types, get_bool_types, get_numeric_types
from src.common.enum import LanguageType

class TestTypesList:

    def test_get_primitive_types_java(self):
        """
            TC-CMM-15.1
        """
        
        # Act
        primitive_types = get_primitive_types(LanguageType.Java)
        
        # Assert
        assert primitive_types == ['byte', 'short', 'int', 'long', 'float', 'double', 'boolean', 'char']

    def test_get_primitive_types_csharp(self):
        """
            TC-CMM-15.2
        """
        
        # Act
        primitive_types = get_primitive_types(LanguageType.CSharp)
        
        # Assert
        assert primitive_types == ['bool', 'byte', 'sbyte', 'char', 'decimal', 'double', 'float', 'int', 'uint', 'long', 'ulong', 'short', 'ushort', 'object', 'string', 'dynamic']

    def test_get_primitive_types_cpp(self):
        """
            TC-CMM-15.3
        """
        
        # Act
        primitive_types = get_primitive_types(LanguageType.CPP)
        
        # Assert
        assert primitive_types == [
            'int', 
            'unsigned int', 
            'signed int', 
            'short', 
            'short int', 
            'unsigned short', 
            'long', 
            'long double', 
            'unsigned long', 
            'float', 
            'double', 
            'char', 
            'unsigned char',
            'signed char',
            'bool'
        ]

    def test_get_primitive_types_unknown(self):
        """
            TC-CMM-15.4
        """
        
        # Act
        primitive_types = get_primitive_types(LanguageType.Unknown)
        
        # Assert
        assert primitive_types == None
    
    def test_get_numeric_types_java(self):
        """
            TC-CMM-16.1
        """
        
        # Act
        numeric_types = get_numeric_types(LanguageType.Java)
        
        # Assert
        assert numeric_types == ['byte', 'short', 'int', 'long', 'float', 'double', 'Byte', 'Float', 'Integer', 'Long', 'Number', 'Short']

    def test_get_numeric_types_csharp(self):
        """
            TC-CMM-16.2
        """
        
        # Act
        numeric_types = get_numeric_types(LanguageType.CSharp)
        
        # Assert
        assert numeric_types == ['byte', 'sbyte',  'decimal', 'double', 'float', 'int', 'uint', 'long', 'ulong', 'short', 'ushort']

    def test_get_numeric_types_unknown(self):
        """
            TC-CMM-16.3
        """
        
        # Act
        numeric_types = get_numeric_types(LanguageType.Unknown)
        
        # Assert
        assert numeric_types == None

    def test_get_bool_types_java(self):
        """
            TC-CMM-17.1
        """
        
        # Act
        bool_types = get_bool_types(LanguageType.Java)
        
        # Assert
        assert bool_types == ['boolean', 'Boolean', 'Predicate']

    def test_get_bool_types_csharp(self):
        """
            TC-CMM-17.2
        """
        
        # Act
        bool_types = get_bool_types(LanguageType.CSharp)
        
        # Assert
        assert bool_types == ['bool', 'Boolean', 'Predicate']
    
    def test_get_bool_types_unknown(self):
        """
            TC-CMM-17.3
        """
        
        # Act
        bool_types = get_bool_types(LanguageType.Unknown)
        
        # Assert
        assert bool_types == None
