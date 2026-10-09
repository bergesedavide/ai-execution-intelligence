from app.selector.scoring import (
    normalize_higher_is_better,
    normalize_lower_is_better,
)


def test_normalize_lower_is_better():

    assert normalize_lower_is_better(
        value=500,
        minimum=500,
        maximum=2000,
    ) == 1.0

    assert normalize_lower_is_better(
        value=2000,
        minimum=500,
        maximum=2000,
    ) == 0.0


def test_normalize_higher_is_better():

    assert normalize_higher_is_better(
        value=1.0,
        minimum=0.0,
        maximum=1.0,
    ) == 1.0

    assert normalize_higher_is_better(
        value=0.0,
        minimum=0.0,
        maximum=1.0,
    ) == 0.0