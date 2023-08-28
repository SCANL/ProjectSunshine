from src.nlp.related_terms import clean_text, remove_stopwords, are_antonyms, get_synonyms
import pytest


@pytest.mark.unit
class TestRelatedTerms:
    """
        Test case specification for these test cases can be found here:
        https://t.ly/0CCGA
    """

    @pytest.fixture
    def mock_word_tokenize(self, mocker):
        """
            Mock for nltk.tokenize.word_tokenize
        """
        return mocker.patch("src.nlp.related_terms.word_tokenize")

    def test_clean_text_empty_string(self, mock_word_tokenize):
        """
            ID: TC-NLP-1.1
        """
        mock_word_tokenize.return_value = []
        result = clean_text("")
        assert result == []
        mock_word_tokenize.assert_called_once_with("")
