from src.nlp.related_terms import clean_text, remove_stopwords, are_antonyms, get_synonyms


class TestRelatedTerms:
    """
        Test case specification for these test cases can be found here:
        https://t.ly/0CCGA
    """

    def test_clean_text_empty_string(self):
        """
            ID: TC-NLP-1.1
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
