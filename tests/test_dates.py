import pytest

from assignment1.main import DatesCensor

testdata = [
    ("My Birthday is 12/21/2001,birthday is on December, 21st, 2001", "My Birthday is ███████████████████ is on ████████████████████", 2),
]

@pytest.mark.parametrize("input,expected_text,expected_count", testdata)
def test_word(input, expected_text, expected_count):
    actual_text, word_list = DatesCensor(input)
    assert actual_text == expected_text
    assert len(word_list) == expected_count