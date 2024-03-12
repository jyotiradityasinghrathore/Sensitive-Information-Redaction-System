import pytest

from assignment1.main import AddressCensor

testdata = [
    ("I live in 134 classen blvd, apt 10115, Gainesville, FL, 32608","I live in ███████████████████████████████████████████████████",1)
]


@pytest.mark.parametrize("input,expected_text,expected_count", testdata)
def test_word(input, expected_text, expected_count):
    actual_text, word_list = AddressCensor(input)
    assert actual_text == expected_text
    assert len(word_list) == expected_count