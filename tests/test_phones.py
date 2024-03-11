import pytest
from assignment1.main import censor_phones

testdata = [
    ("My contact is changed to phone number +1(352)3282522, +917877386322","My contact is changed to phone number ██████████████, █████████████",2),
    ("Phone no. is +1(352)477-3788, +917229967111", "My Phone no. is ███████████████, █████████████", 2),
]

@pytest.mark.parametrize("input,expected_text,expected_count", testdata)
def test_word(input, expected_text, expected_count):
    actual_text, word_list = censor_phones(input)
    assert actual_text == expected_text
    assert len(word_list) == expected_count