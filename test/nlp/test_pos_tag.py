import pytest
from src.nlp.pos_tag import generate_tag

class TestPosTag:

    @pytest.fixture
    def mock_get_pos_terms(self, mocker):
        """
            Mock for src.nlp.term_list.get_pos_terms (used in src.nlp.pos_tag.generate_tag)
        """
        return mocker.patch("src.nlp.term_list.get_pos_terms")


    def test_generate_tag_custom_pos_term(self, mock_get_pos_terms):
        """
            ID: TC-NLP-5.1
        """
        mock_get_pos_terms.return_value = {
            "apple": "NNP"}  # Mocking the return value of get_pos_terms
        # None passed as Project instance as it is not used in the function (mocked)
        result = generate_tag(None, "apple")
        assert result == "NNP"

    def test_generate_tag_custom_pos_term_mixed_case(self, mock_get_pos_terms):
        """
            ID: TC-NLP-5.2
        """
        mock_get_pos_terms.return_value = {
            "apple": "NNP"}  # Mocking the return value of get_pos_terms
        # None passed as Project instance as it is not used in the function (mocked)
        result = generate_tag(None, "Apple")
        assert result == "NNP"
