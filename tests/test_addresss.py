import pytest

from assignment1.main import AddressCensor

testdata = [
    ("I use to live in 2000SW, apt 231, gainesville, Florida, 32605","I use to live in ██████████████████████████████████████████████",1),
    ("My address is 4000SW 37th street, apt 1114, Gainesville, Florida, 32608","my address is ██████████████████████████████████████████████", 1) 
]


@pytest.mark.parametrize("input,expected_text,expected_count", testdata)
def test_word(input, expected_text, expected_count):
    actual_text, word_list = AddressCensor(input)
    assert actual_text == expected_text
    assert len(word_list) == expected_count