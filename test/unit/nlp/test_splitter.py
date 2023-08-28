from src.nlp.splitter import Splitter
import pytest


@pytest.mark.unit
class TestSplitter:
    """
        Test case specification for these test cases can be found here:
        https://t.ly/0CCGA
    """

    def test_split_word_tokens(self):
        """
            ID: TC-NLP-6.1
        """
        result = Splitter.split_word_tokens(
            "Hello world this is a test string")
        assert result == ["Hello", "world",
                          "this", "is", "a", "test", "string"]

    def test_split_word_tokens_non_alpha(self):
        """
            ID: TC-NLP-6.2
        """
        result = Splitter.split_word_tokens("1231,-.#$%")
        assert result == []

    def test_split_word_tokens_non_alpha(self):
        """
            ID: TC-NLP-6.3
            Note: not sure if this is the desired behaviour
        """
        result = Splitter.split_word_tokens("Happy,dog|Another sentence")
        assert result == []
