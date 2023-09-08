import pytest
from src.common.util_parsing import get_class_attribute_names, get_all_items_in_class, get_all_class_fields, is_test_method, is_boolean_type
from src.common.enum import IdentifierType, FileType, LanguageType


@pytest.mark.unit
class TestUtilParsing:

    def __mock_attribute(self, mocker, type, name, parent_name, is_array, is_generic, source=""):
        """
            Creates mock instances of the class src.model.identifier.Attribute.

            Args:
                mocker: Mocking framework instance for creating the mock.
                name: Name of the attribute.
                identifier_type: Type of the construct being created, assigned a value from the enumeration src.common.enum.IdentifierType specifier.
                parent_name: Name of the parent class.
                is_array: Indicates if the attribute is an array (default is False).
                is_generic: Indicates if the attribute can take generic values (default is False).
                source: The source code from which it's obtained (default is "").

            Returns:
                Mock of src.model.identifier.Attribute.
        """
        mock = mocker.patch('src.model.identifier.Attribute')
        mock.name = name
        mock.type = type
        mock.specifier = "default"
        mock.parent_name = parent_name
        mock.is_array = is_array
        mock.is_generic = is_generic
        mock.source = source

        return mock

    def __mock_method(self, mocker, name, annotations, parent_name, return_type, is_array, variables, parameters, source=""):
        """
            Creates mock instances of the class src.model.identifier.Method.

            Args:
                mocker: Mocking framework instance for creating the mock.
                name: Name of the method.
                annotations: Array of method annotations.
                parent_name: Name of the parent class.
                return_type: The return type of the method.
                is_array: Indicates if the return type is an array (default is False).
                variables: Variables present within the method (default is None).
                parameters: Parameters that the method takes as input (default is None).
                source: The source code from which it's obtained (default is "").

            Returns:
                Mock of src.model.identifier.Method.
        """
        mock = mocker.patch('src.model.identifier.Method')
        mock.name = name
        mock.specifier = "default"
        mock.annotations = annotations
        mock.parent_name = parent_name
        mock.is_array = is_array
        mock.return_type = return_type
        mock.source = source
        mock.variables = variables
        mock.parameters = parameters

        return mock

    def __mock_variable(self, mocker, type, name, is_array, is_generic, source=""):
        """
            Creates mock instances of the class src.model.identifier.Variable.

            Args:
                mocker: Mocking framework instance for creating the mock.
                identifier_type: Type of the construct being created, assigned a value from the enumeration src.common.enum.IdentifierType.
                name: Name of the variable.
                is_array: Indicates if the variable is an array (default is False).
                is_generic: Indicates if the variable can take generic values (default is False).
                source: The source code from which it's obtained (default is "").

            Returns:
                Mock of src.model.identifier.Variable.
        """
        mock = mocker.patch('src.model.identifier.Variable')
        mock.name = name
        mock.type = type
        mock.specifier = "default"
        mock.is_array = is_array
        mock.is_generic = is_generic
        mock.source = source

        return mock

    def __mock_parameter(self, mocker, type, name, is_array, is_generic, source=""):
        """
            Creates mock instances of the class src.model.identifier.Parameter.

            Args:
                mocker: Mocking framework instance for creating the mock.
                identifier_type: Type of the construct being created, assigned a value from the enumeration src.common.enum.IdentifierType.
                name: Name of the parameter.
                is_array: Indicates if the parameter is an array (default is False).
                is_generic: Indicates if the parameter can take generic values (default is False).
                source: The source code from which it's obtained (default is "").

            Return:
                Mock of src.model.identifier.Parameter.
        """
        mock = mocker.patch('src.model.identifier.Parameter')
        mock.name = name
        mock.type = type
        mock.specifier = "default"
        mock.is_array = is_array
        mock.is_generic = is_generic
        mock.source = source

        return mock

    @pytest.fixture
    def mock_entity_attributes(self, mocker):
        """
            Mocks a class containing two attributes.
        """

        mock = mocker.patch('src.model.identifier.Class')
        mock.attributes = [
            self.__mock_attribute(mocker, type=IdentifierType.Attribute, name="attr1",
                                  parent_name="Class", is_array=False, is_generic=False),
            self.__mock_attribute(mocker, type=IdentifierType.Attribute, name="attr2",
                                  parent_name="Class2", is_array=False, is_generic=False)
        ]
        return mock

    @pytest.fixture
    def mock_class_items(self, mocker, mock_entity_attributes):
        """
            Mocks a class containing a method.
        """
        parsed_parameters = [
            self.__mock_parameter(mocker, type=IdentifierType.Parameter,
                                  name='param1', is_array=False, is_generic=False),
            self.__mock_parameter(mocker, type=IdentifierType.Parameter,
                                  name='param2', is_array=True, is_generic=False)
        ]

        parsed_vars = [
            self.__mock_variable(mocker, type=IdentifierType.Variable,
                                 name='var1', is_array=False, is_generic=False),
            self.__mock_variable(mocker, type=IdentifierType.Variable,
                                 name='var2', is_array=True, is_generic=False)
        ]

        method = self.__mock_method(
            mocker, 'method1', '', 'Class', 'string', False, parsed_vars, parsed_parameters)

        mock = mock_entity_attributes
        mock.methods = [method]

        return mock

    def test_get_class_attribute_names(self, mock_entity_attributes):
        """
            TC-CMM-6.1
        """
        # Act
        names = get_class_attribute_names(mock_entity_attributes)

        # Assert
        assert names == ['attr1', 'attr2']

    def test_get_all_items_in_class(self, mock_class_items):
        """
            TC-CMM-7.1
        """

        # Act
        items = get_all_items_in_class(mock_class_items)

        # Assert
        assert len(items) == 8

    def test_get_all_class_fields(self, mock_class_items):
        """
            TC-CMM-8.1
        """

        # Act
        fields = get_all_class_fields(mock_class_items)

        # Assert
        assert len(fields) == 6

    @pytest.fixture
    def mock_project(self, mocker):
        return mocker.patch('src.model.project.Project')

    @pytest.fixture
    def mock_entity(self, mocker):
        return mocker.patch('src.model.entity.Entity')

    @pytest.fixture
    def mock_test_method(self, mocker):
        """
            Mocks a method having a Test annotation.
        """
        return self.__mock_method(mocker, name='MyTest', annotations=['Test'], parent_name='MyClass', return_type='', is_array=False, parameters=[], variables=[])

    @pytest.fixture
    def mock_method(self, mocker):
        """
            Mocks a regular method.
        """
        return self.__mock_method(mocker, name='MyTest', annotations=[''], parent_name='MyClass', return_type='', is_array=False, parameters=[], variables=[])

    @pytest.fixture
    def mock_test_method_annotations(self, mocker):
        return mocker.patch('src.common.testing_list.get_test_method_annotations')

    @pytest.fixture
    def mock_attribute(self, mocker):
        return mocker.patch('src.model.identifier.Attribute')

    @pytest.fixture
    def mock_identifier_type(self, mocker):
        return mocker.patch('src.common.enum.IdentifierType.get_type')

    def test_is_test_method(self, mock_test_method, mock_entity, mock_project, mock_test_method_annotations, mock_identifier_type):
        """
            TC-CMM-9.1
        """

        # Arrange
        mock_entity.file_type = FileType.Test
        mock_entity.language = LanguageType.Java
        mock_test_method_annotations.return_value = ['Test']
        mock_identifier_type.return_value = IdentifierType.Method

        # Act
        val = is_test_method(mock_project, mock_entity, mock_test_method)

        # Assert
        assert val == True

    def test_is_test_method_not_a_test_file(self, mock_test_method, mock_entity, mock_project, mock_test_method_annotations, mock_identifier_type):
        """
            TC-CMM-9.2
        """

        # Arrange
        mock_entity.file_type = FileType.NonTest
        mock_entity.language = LanguageType.Java
        mock_test_method_annotations.return_value = ['Test']
        mock_identifier_type.return_value = IdentifierType.Method

        # Act
        val = is_test_method(mock_project, mock_entity, mock_test_method)

        # Assert
        assert val == False

    def test_is_test_method_fail_not_test_method(self, mock_method, mock_entity, mock_project, mock_identifier_type, mock_test_method_annotations):
        """
            TC-CMM-9.3
        """

        # Arrange
        mock_entity.file_type = FileType.Test
        mock_entity.language = LanguageType.Java
        mock_test_method_annotations.return_value = ['Test']
        mock_identifier_type.return_value = IdentifierType.Method

        # Act
        val = is_test_method(mock_project, mock_entity, mock_method)

        # Assert
        assert val == False

    def test_is_test_method_fail(self, mock_attribute, mock_entity, mock_project, mock_identifier_type):
        """
            TC-CMM-9.4
        """

        # Arrange
        mock_entity.file_type = FileType.Test
        mock_entity.language = LanguageType.Java
        mock_identifier_type.return_value = IdentifierType.Attribute

        # Act
        val = is_test_method(mock_project, mock_entity, mock_attribute)

        # Assert
        assert val == False

    @pytest.fixture
    def mock_is_bool_method(self, mocker):
        return mocker.patch('src.model.identifier.Method')

    def test_is_boolean_type_true_java(self, mock_entity, mock_identifier_type, mock_is_bool_method):
        """
            TC-CMM-10.1
        """

        # Arrange
        mock_entity.language = LanguageType.Java
        mock_identifier_type.return_value = IdentifierType.Method
        mock_is_bool_method.return_type = 'boolean'

        # Act
        val = is_boolean_type(mock_entity, mock_is_bool_method)

        # Assert
        assert val == True

    def test_is_boolean_type_false_java(self, mock_entity, mock_identifier_type, mock_is_bool_method):
        """
            TC-CMM-10.2
        """

        # Arrange
        mock_entity.language = LanguageType.Java
        mock_identifier_type.return_value = IdentifierType.Method
        mock_is_bool_method.return_type = ''

        # Act
        val = is_boolean_type(mock_entity, mock_is_bool_method)

        # Assert
        assert val == False

    def test_is_boolean_type_true_csharp(self, mock_entity, mock_identifier_type, mock_is_bool_method):
        """
            TC-CMM-10.3
        """

        # Arrange
        mock_entity.language = LanguageType.CSharp
        mock_identifier_type.return_value = IdentifierType.Method
        mock_is_bool_method.return_type = 'bool'

        # Act
        val = is_boolean_type(mock_entity, mock_is_bool_method)

        # Assert
        assert val == True

    def test_is_boolean_type_false_java(self, mock_entity, mock_identifier_type, mock_is_bool_method):
        """
            TC-CMM-10.4
        """

        # Arrange
        mock_entity.language = LanguageType.CSharp
        mock_identifier_type.return_value = IdentifierType.Method
        mock_is_bool_method.return_type = ''

        # Act
        val = is_boolean_type(mock_entity, mock_is_bool_method)

        # Assert
        assert val == False

    def test_is_boolean_type_false_not_method(self, mock_entity, mock_identifier_type, mock_attribute):
        """
            TC-CMM-10.5
        """

        # Arrange
        mock_entity.language = LanguageType.CSharp
        mock_identifier_type.return_value = IdentifierType.Attribute

        # Act
        val = is_boolean_type(mock_entity, mock_attribute)

        # Assert
        assert val == False
