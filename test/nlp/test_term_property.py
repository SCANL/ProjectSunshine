import pytest
from unittest.mock import patch, Mock
from src.nlp.term_property import is_singular, is_plural
from src.nlp import term_list, pos_tag


class TestTermProperty:
    """
        Test case specification for these test cases can be found here:
        https://t.ly/0CCGA
    """

    CUSTOM_PLURAL_TERMS_MOCK = {"apples": "NNS",
                                "oranges": "NNS", "bananas": "NNS"}

    @pytest.fixture
    def mock_get_plural_terms(self, mocker):
        """
            Mock for src.nlp.term_list.get_plural_terms
        """
        return mocker.patch("src.nlp.term_list.get_plural_terms", return_value=self.CUSTOM_PLURAL_TERMS_MOCK)

    def test_is_singular_custom_term(self, mock_get_plural_terms):
        """
            ID: TC-NLP-7.1
        """
        result = is_singular(None, "apples")
        assert result == False

    def test_is_singular_proper_name(self, mock_get_plural_terms):
        """
            ID: TC-NLP-7.2
        """
        with patch("src.nlp.term_property.generate_tag", return_value="NNP"):
            result = is_singular(None, "Paris")
            assert result == True

    def test_is_singular_plural_input(self, mock_get_plural_terms):
        """
            ID: TC-NLP-7.3
        """
        with patch("src.nlp.term_property.generate_tag", return_value="NNS"):
            result = is_singular(None, "rooms")
            assert result == False

    def test_is_plural_custom_term(self, mock_get_plural_terms):
        """
            ID: TC-NLP-8.1
        """
        result = is_plural(None, "apples")
        assert result == True

    def test_is_plural_proper_name(self, mock_get_plural_terms):
        """
            ID: TC-NLP-8.2
        """
        with patch("src.nlp.term_property.generate_tag", return_value="NNP"):
            result = is_plural(None, "Chris")
            assert result == False

    def test_is_plural(self, mock_get_plural_terms):
        """
            ID: TC-NLP-8.3
        """
        with patch("src.nlp.term_property.generate_tag", return_value="NNS"):
            # "buildings" is not in CUSTOM_PLURAL_TERMS_MOCK
            result = is_plural(None, "buildings")
            assert result == True
