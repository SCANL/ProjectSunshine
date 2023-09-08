import pytest
from src.nlp.pos_tag import generate_tag, POSTaggerStanford
from src.nlp import pos_tag


@pytest.mark.unit
class TestPosTag:
    """
        Test case specification for these test cases can be found here:
        https://t.ly/0CCGA
    """

    def setUp(self):
        self.postaggerstanford = POSTaggerStanford
        POSTaggerStanford.__init__ = lambda self: None

    def tearDown(self):
        pos_tag.POSTaggerStanford = self.postaggerstanford

    @pytest.fixture
    def mock_get_pos_terms(self, mocker):
        """
            Mock for src.nlp.term_list.get_pos_terms (used in src.nlp.pos_tag.generate_tag)
        """
        return mocker.patch("src.nlp.term_list.get_pos_terms")

    @pytest.fixture
    def mock_get_pos(self, mocker):
        return mocker.patch("src.nlp.pos_tag.POSTaggerStanford.get_pos")

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

    def test_generate_tag_stanford(self, mock_get_pos_terms, mock_get_pos):
        """
            ID: TC-NLP-5.3
            Note: The two `with` statements are used to mock the constructor and the `get_pos` method of the `POSTaggerStanford` class
        """
        mock_get_pos_terms.return_value = {
            "apple": "NNP"}
        mock_get_pos.return_value = "PRP"
        # None passed as Project instance as it is not used in the function (mocked)
        result = generate_tag(None, term="your")
        # This means the mocked function was called so the function uses the POSTaggerStanford class to generate the tag
        assert result == "PRP"
