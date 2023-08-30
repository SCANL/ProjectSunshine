import pytest
from src.common.util_parsing import get_class_attribute_names, get_all_items_in_class, get_all_class_fields, is_test_method, is_boolean_type
from src.common.enum import IdentifierType, FileType, LanguageType

@pytest.mark.unit
class TestUtilParsing:
    
    def __mock_attribute(self, mocker, type, name, parent_name, is_array, is_generic, source=""):
        """
            La funzione permette di creare dei mock della classe src.model.identifier.Attribute
            Args:
                mocker: per la creazione del mock
                name: nome dell'attributo
                type: tipo di costrutto che si sta andando a creare, si assegna un valore della enumerazione src.common.enum.IdentifierType
                specifier
                parent_name: nome della classe di appartenenza
                is_array: se si tratta di un array
                is_generic: se può assumere valori generici
                source: il codice sorgente da cui è ottenuto (impostato a "" come valore di default)
            Return:
                il mock di src.model.identifier.Attribute
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
            La funzione permette di creare dei mock della classe src.model.identifier.Method
            Args:
                mocker: per la creazione del mock
                name: nome del metodo
                annotations: array di annotazioni del metodo
                parent_name: nome della classe di appartenenza
                return_type: il tipo restituito dal metodo
                is_array: se si tratta di un array
                variables: variabili presenti all'interno del metodo
                parameters: i parametri che il metodo prende in input
                source: il codice sorgente da cui è ottenuto (impostato a "" come valore di default)
            Return:
                il mock di src.model.identifier.Method
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
            La funzione permette di creare dei mock della classe src.model.identifier.Variable
            Args:
                mocker: per la creazione del mock
                type: tipo di costrutto che si sta andando a creare, si assegna un valore della enumerazione src.common.enum.IdentifierType
                name: nome del metodo
                is_array: se si tratta di un array
                is_generic: se può assumere valori generici
                source: il codice sorgente da cui è ottenuto (impostato a "" come valore di default)
            Return:
                il mock di src.model.identifier.Variable
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
            La funzione permette di creare dei mock della classe src.model.identifier.Parameter
            Args:
                mocker: per la creazione del mock
                type: tipo di costrutto che si sta andando a creare, si assegna un valore della enumerazione src.common.enum.IdentifierType
                name: nome del metodo
                is_array: se si tratta di un array
                is_generic: se può assumere valori generici
                source: il codice sorgente da cui è ottenuto (impostato a "" come valore di default)
            Return:
                il mock di src.model.identifier.Parameter
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
            La funzione effettua il mock di una classe contentete due attributi
        """

        mock = mocker.patch('src.model.identifier.Class')
        mock.attributes = [
            self.__mock_attribute(mocker, type=IdentifierType.Attribute, name="attr1", parent_name="Class", is_array=False, is_generic=False), 
            self.__mock_attribute(mocker, type=IdentifierType.Attribute, name="attr2", parent_name="Class2", is_array=False, is_generic=False)
        ]
        return mock
    
    @pytest.fixture
    def mock_class_items(self, mocker, mock_entity_attributes):
        """
            La funzione effettua il mock di una classe contenente un metodo
        """
        params = [
            self.__mock_parameter(mocker, type=IdentifierType.Parameter, name='param1', is_array=False, is_generic=False),
            self.__mock_parameter(mocker, type=IdentifierType.Parameter, name='param2', is_array=True, is_generic=False)
        ]

        vars = [
            self.__mock_variable(mocker, type=IdentifierType.Variable, name='var1', is_array=False, is_generic=False),
            self.__mock_variable(mocker, type=IdentifierType.Variable, name='var2', is_array=True, is_generic=False)
        ]

        method = self.__mock_method(mocker, 'method1', '', 'Class', 'string', False, vars, params)

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

    def test_get_all_class_fileds(self, mock_class_items):
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
            La funzione effettua il mock di un metodo avente un annotazione di Test
        """
        return self.__mock_method(mocker, name='MyTest', annotations=['Test'], parent_name='MyClass', return_type='', is_array=False, parameters=[], variables=[])

    @pytest.fixture
    def mock_method(self, mocker):
        """
            La funzione effettua il mock di un metodo normale
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