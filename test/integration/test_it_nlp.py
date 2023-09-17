import pytest
from src.nlp.related_terms import clean_text, remove_stopwords, are_antonyms, get_synonyms
from src.nlp.splitter import Splitter
from src.nlp.pos_tagger_stanford import POSTaggerStanford


@pytest.mark.integration
class TestItPOSTaggerStanford:

    @pytest.fixture
    def tagger(self):
        return POSTaggerStanford()
    
    def test_get_pos_empty_string(self, tagger: POSTaggerStanford):
        """
            ID: TC-NLP-5.1
        """
        result = tagger.get_pos("apple")
        assert result == "NN"


@pytest.mark.integration
class TestItNlp:

    def test_clean_text_empty_string(self):
        """
            ID: TC-NLP-1.1 [integration]
        """
        result = clean_text("")
        assert result == []

    def test_clean_text_non_empty_string(self):
        """
            ID: TC-NLP-1.2
        """
        result = clean_text("Hello world, this is a test string.")
        assert result == ["Hello", "world",
                          "this", "is", "a", "test", "string"]

    def test_clean_text_unique(self):
        """
            ID: TC-NLP-1.3
        """
        result = clean_text(
            "Hello string world, this is a test string.", return_unique=True)
        assert result.count("string") == 1

    def test_clean_text_not_unique(self):
        """
            ID: TC-NLP-1.4
        """
        result = clean_text(
            "Hello string world, this is a test string.", return_unique=False)
        assert result.count("string") == 2

    def test_remove_stopwords(self):
        """
            ID: TC-NLP-2.1
        """
        result = remove_stopwords(
            ["that", "dog", "cat", "sea", "python", "the"])
        assert result == ["dog", "cat", "sea", "python"]

    def test_remove_stopwords_no_stopwords_input(self):
        """
            ID: TC-NLP-2.2
        """
        result = remove_stopwords(
            ["dog", "cat", "sea", "python"])
        assert result == ["dog", "cat", "sea", "python"]

    def test_are_antonyms_empty_strings(self):
        """
            ID: TC-NLP-3.1
        """
        result = are_antonyms("", "")
        assert result == False

    def test_are_antonyms_one_empty_string(self):
        """
            ID: TC-NLP-3.2
        """
        result = are_antonyms("", "good")
        assert result == False

    def test_are_antonyms_false(self):
        """
            ID: TC-NLP-3.3
        """
        result = are_antonyms("exit", "good")
        assert result == False

    def test_are_antonyms_true(self):
        """
            ID: TC-NLP-3.4
        """
        result = are_antonyms("bad", "good")
        assert result == True

    def test_are_antonyms_one_mixed_case(self):
        """
            ID: TC-NLP-3.5
            Note: The function should ignore case
        """
        result = are_antonyms("bad", "GoOd")
        assert result == True

    def test_are_antonyms_mixed_case(self):
        """
            ID: TC-NLP-3.6
        """
        result = are_antonyms("HappY", "sAD")
        assert result == True

    def test_get_synonyms_empty_string(self):
        """
            ID: TC-NLP-4.1
            Note: pos tags to be used in this fn are from wordnet (not Stanford)
        """
        result = get_synonyms("", "a")
        assert len(result) == 0

    def test_get_synonyms_invalid_pos(self):
        """
            ID: TC-NLP-4.2
        """
        result = get_synonyms("dog", "XYZ")
        assert len(result) == 0

    def test_get_synonyms(self):
        """
            ID: TC-NLP-4.3
        """
        result = get_synonyms("good", "a")  # use wordnet pos tags
        self.good_synonyms_number = len(result)
        assert len(result) > 0

    def test_get_synonyms_mixed_case(self):
        """
            ID: TC-NLP-4.4
        """
        result = get_synonyms("goOD", "a")
        assert len(result) > 0

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

    @pytest.mark.xfail(reason="not the desired behavior")
    def test_split_word_tokens_mixed(self):
        """
            ID: TC-NLP-6.3
            Note: not sure if this is the desired behaviour
        """
        result = Splitter.split_word_tokens("Happy,dog|Another sentence")
        assert result == ["Happy", "dog", "Another", "sentence"]
        # ------------------------------------------------------------
    #     AssertionError: assert ['Happy', 'sentence', 'Another', 'sentence'] == []
    # E         Left contains 2 more items, first extra item: 'Happy'
    # E         Full diff:
    # E         - []
    # E         + ['Happy', 'sentence']
