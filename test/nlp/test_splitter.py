from src.nlp.splitter import Splitter


class TestSplitter:

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

