import pytest

from assignment1.main import censor_names_snorkel

testdata = [
    ("My name is Jyotiraditya. Virat is my favorite player", "My name is ██████. █████████ is my favorite player", 2)
]


@pytest.mark.parametrize("input,expected_text,expected_count", testdata)
def test_word(input, expected_text, expected_count):
    actual_text, word_list = censor_names_snorkel(input)

    assert actual_text == expected_text
    assert len(word_list) == expected_count