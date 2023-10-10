import pytest
from unittest.mock import Mock
from src.model.project import ConfigCustomFileType
from src.nlp.term_list import get_splitter_terms, get_pos_terms
from src.nlp.term_list import get_plural_terms, get_transform_terms_staring
from src.nlp.term_list import get_transform_terms_inner, get_conditional_terms
from src.nlp.term_list import get_validate_terms, get_boolean_terms
from src.nlp.term_list import get_get_terms, get_set_terms


@pytest.mark.unit
class TestTermList:
  
    @pytest.fixture
    def mock_project(self):
        return Mock()

    def test_get_splitter_terms_empty(self, mock_project):
        """
            ID: TC-NLP-9.1
        """
        mock_project.get_config_value.return_value = []

        assert len(get_splitter_terms(mock_project)) >= 1
        mock_project.get_config_value.assert_called_once_with(
            ConfigCustomFileType.Terms, 'Splitter', 'splitter_terms')

    def test_get_splitter_terms_custom(self, mock_project):
        """
            ID: TC-NLP-9.2
        """

        mock_project.get_config_value.return_value = ["a", "b", "c"]
        result = get_splitter_terms(mock_project)

        assert 'a' in result
        assert 'b' in result
        assert 'c' in result

    def test_get_pos_terms_empty(self, mock_project):
        """
            ID: TC-NLP-9.3
        """
        mock_project.get_config_value.return_value = {}

        assert len(get_pos_terms(mock_project)) >= 1
        mock_project.get_config_value.assert_called_once_with(
            ConfigCustomFileType.Terms, 'POS', 'pos_terms')

    def test_get_pos_terms_custom(self, mock_project):
        """
            ID: TC-NLP-9.4
        """

        KEY1 = "Test1"
        KEY2 = "Test2"

        mock_project.get_config_value.return_value = {
            KEY1: "VB",
            KEY2: "NN"
        }
        result = get_pos_terms(mock_project)

        assert KEY1 in result
        assert KEY2 in result

    def test_get_plural_terms_empty(self, mock_project):
        """
            ID: TC-NLP-9.5
        """
        mock_project.get_config_value.return_value = []

        assert len(get_plural_terms(mock_project)) >= 1
        mock_project.get_config_value.assert_called_once_with(
            ConfigCustomFileType.Terms, 'Plural', 'plural_terms')

    def test_get_plural_terms_custom(self, mock_project):
        """
            ID: TC-NLP-9.6
        """
        CUSTOM_PLURAL_TERMS = ["a", "b", "c"]

        mock_project.get_config_value.return_value = CUSTOM_PLURAL_TERMS
        result = get_plural_terms(mock_project)

        # assert that all elements in CUSTOM_PLURAL_TERMS are in result
        assert all(term in result for term in CUSTOM_PLURAL_TERMS)

    def test_get_transform_terms_staring(self, mock_project):
        """
            ID: TC-NLP-9.7
        """
        mock_project.get_config_value.return_value = []
        assert len(get_transform_terms_staring(mock_project)) >= 1
        mock_project.get_config_value.assert_called_once_with(
            ConfigCustomFileType.Terms, 'Terms', 'transform_terms_staring')

    def test_get_transform_terms_staring_custom(self, mock_project):
        """
            ID: TC-NLP-9.8
        """
        CUSTOM_TRANSFORM_TERMS = ["test1", "test2"]

        mock_project.get_config_value.return_value = CUSTOM_TRANSFORM_TERMS
        result = get_transform_terms_staring(mock_project)

        # assert that all elements in CUSTOM_TRANSFORM_TERMS are in result
        assert all(term in result for term in CUSTOM_TRANSFORM_TERMS)

    def test_get_transform_terms_inner(self, mock_project):
        """
            ID: TC-NLP-9.9
        """
        mock_project.get_config_value.return_value = []
        assert len(get_transform_terms_inner(mock_project)) >= 1
        mock_project.get_config_value.assert_called_once_with(
            ConfigCustomFileType.Terms, 'Terms', 'transform_terms_inner')

    def test_get_transform_terms_inner_custom(self, mock_project):
        """
            ID: TC-NLP-9.10
        """
        CUSTOM_TRANSFORM_TERMS = ["test1to", "test2into"]

        mock_project.get_config_value.return_value = CUSTOM_TRANSFORM_TERMS
        result = get_transform_terms_inner(mock_project)

        # assert that all elements in CUSTOM_TRANSFORM_TERMS are in result
        assert all(term in result for term in CUSTOM_TRANSFORM_TERMS)

    def test_get_conditional_terms(self, mock_project):
        """
            ID: TC-NLP-9.11
        """
        mock_project.get_config_value.return_value = []
        assert len(get_conditional_terms(mock_project)) >= 1
        mock_project.get_config_value.assert_called_once_with(
            ConfigCustomFileType.Terms, 'Terms', 'conditional_terms')

    def test_get_conditional_terms_custom(self, mock_project):
        """
            ID: TC-NLP-9.12
        """

        CUSTOM_CONDITIONAL_TERMS = ["test1", "test2"]

        mock_project.get_config_value.return_value = CUSTOM_CONDITIONAL_TERMS
        result = get_conditional_terms(mock_project)

        # assert that all elements in CUSTOM_CONDITIONAL_TERMS are in result
        assert all(term in result for term in CUSTOM_CONDITIONAL_TERMS)

    def test_get_validate_terms(self, mock_project):
        """
            ID: TC-NLP-9.13
        """

        mock_project.get_config_value.return_value = []
        assert len(get_validate_terms(mock_project)) >= 1
        mock_project.get_config_value.assert_called_once_with(
            ConfigCustomFileType.Terms, 'Terms', 'validate_terms')

    def test_get_validate_terms_custom(self, mock_project):
        """
            ID: TC-NLP-9.14
        """
        CUSTOM_VALIDATE_TERMS = ["test1", "test2"]

        mock_project.get_config_value.return_value = CUSTOM_VALIDATE_TERMS
        result = get_validate_terms(mock_project)

        # assert that all elements in CUSTOM_VALIDATE_TERMS are in result
        assert all(term in result for term in CUSTOM_VALIDATE_TERMS)

    def test_get_boolean_terms(self, mock_project):
        """
            ID: TC-NLP-9.15
        """

        mock_project.get_config_value.return_value = []
        assert len(get_boolean_terms(mock_project)) >= 1
        mock_project.get_config_value.assert_called_once_with(
            ConfigCustomFileType.Terms, 'Terms', 'boolean_terms')

    def test_get_boolean_terms_custom(self, mock_project):
        """
            ID: TC-NLP-9.16
        """

        CUSTOM_BOOLEAN_TERMS = ["test1", "test2"]

        mock_project.get_config_value.return_value = CUSTOM_BOOLEAN_TERMS
        result = get_boolean_terms(mock_project)

        # assert that all elements in CUSTOM_BOOLEAN_TERMS are in result
        assert all(term in result for term in CUSTOM_BOOLEAN_TERMS)

    def test_get_get_terms(self, mock_project):
        """
            ID: TC-NLP-9.17
        """

        mock_project.get_config_value.return_value = []
        assert len(get_get_terms(mock_project)) >= 1
        mock_project.get_config_value.assert_called_once_with(
            ConfigCustomFileType.Terms, 'Terms', 'get_terms')

    def test_get_get_terms_custom(self, mock_project):
        """
            ID: TC-NLP-9.18
        """

        CUSTOM_GET_TERMS = ["test1", "test2"]

        mock_project.get_config_value.return_value = CUSTOM_GET_TERMS
        result = get_get_terms(mock_project)

        # assert that all elements in CUSTOM_GET_TERMS are in result
        assert all(term in result for term in CUSTOM_GET_TERMS)

    def test_get_set_terms(self, mock_project):
        """
            ID: TC-NLP-9.19
        """
        mock_project.get_config_value.return_value = []
        assert len(get_set_terms(mock_project)) >= 1
        mock_project.get_config_value.assert_called_once_with(
            ConfigCustomFileType.Terms, 'Terms', 'set_terms')

    def test_get_set_terms_custom(self, mock_project):
        """
            ID: TC-NLP-9.20
        """

        CUSTOM_SET_TERMS = ["test1", "test2"]

        mock_project.get_config_value.return_value = CUSTOM_SET_TERMS
        result = get_set_terms(mock_project)

        # assert that all elements in CUSTOM_SET_TERMS are in result
        assert all(term in result for term in CUSTOM_SET_TERMS)
