import pytest

from assignment1.main import Snorkel_Censor_Name

testdata = [
    ("My name is Aditya Singh. James Lebron is my favorite player", "My name is ████████████. ████████████ is my favorite player", 2)
]


@pytest.mark.parametrize("input,expected_text,expected_count", testdata)
def test_word(input, expected_text, expected_count):
    actual_text, word_list = Snorkel_Censor_Name(input)

    assert actual_text == expected_text
    assert len(word_list) == expected_count