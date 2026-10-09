from types import SimpleNamespace

from app.cost.cost_service import CostService


def test_cost_calculation():

    execution = SimpleNamespace(
        input_tokens=1000,
        output_tokens=500,
    )

    model = SimpleNamespace(
        input_cost=0.001,
        output_cost=0.002,
    )

    service = CostService()

    result = service.calculate(
        execution=execution,
        model=model,
    )

    assert result.input_cost == 1.0
    assert result.output_cost == 1.0
    assert result.total_cost == 2.0

def test_cost_calculation_with_missing_tokens():

    execution = SimpleNamespace(
        input_tokens=None,
        output_tokens=None,
    )

    model = SimpleNamespace(
        input_cost=0.001,
        output_cost=0.002,
    )

    service = CostService()

    result = service.calculate(
        execution=execution,
        model=model,
    )

    assert result.input_cost == 0.0
    assert result.output_cost == 0.0
    assert result.total_cost == 0.0