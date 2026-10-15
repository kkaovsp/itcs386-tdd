import pytest
from shipping import shipping_fee


# Rule 1: The weight must be more than 0 kg. Otherwise raise ValueError.
def test_negative_weight_raises_error():
    with pytest.raises(ValueError, match="weight must be more than 0 kg"):
        shipping_fee(-1)


# Breaks Rule 1: weight must be more than 0 kg; 0 kg must raise ValueError
def test_zero_weight_raises_error():
    with pytest.raises(ValueError, match="weight must be more than 0 kg"):
        shipping_fee(0)


# Rule 2: A parcel of up to 1 kg costs 40 baht.
def test_rule_2_inside_range():
    assert shipping_fee(0.5) == 40


# Breaks Rule 2: parcel of exactly 1 kg costs 40 baht, but buggy code returns 60
def test_rule_2_edge_one_kg():
    assert shipping_fee(1.0) == 40


# Rule 3: A parcel of more than 1 kg and up to 5 kg costs 60 baht.
@pytest.mark.parametrize("weight, expected_fee", [
    (1.1, 60),
    (3.0, 60),
    (5.0, 60),
])
def test_rule_3_fee(weight, expected_fee):
    assert shipping_fee(weight) == expected_fee


# Breaks Rule 4: 5.2 kg parcel must cost 70 baht, but buggy code returns 60
def test_rule_4_started_kilogram_fraction():
    assert shipping_fee(5.2) == 70


# Rule 4: Whole kilograms above 5 kg
def test_rule_4_whole_kilogram():
    assert shipping_fee(6.0) == 70
    assert shipping_fee(7.0) == 80
