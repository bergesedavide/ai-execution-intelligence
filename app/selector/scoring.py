

def normalize_lower_is_better(
    value: float,
    minimum: float,
    maximum: float,
) -> float:

    if maximum == minimum:
        return 1.0

    return (maximum - value) / (maximum - minimum)


def normalize_higher_is_better(
    value: float,
    minimum: float,
    maximum: float,
) -> float:

    if maximum == minimum:
        return 1.0

    return (value - minimum) / (maximum - minimum)