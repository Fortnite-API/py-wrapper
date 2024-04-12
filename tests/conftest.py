import pytest

from fortnite_api import OptimizationFlags


@pytest.fixture(
    params=[
        (OptimizationFlags.none()),
        (OptimizationFlags.IGNORE_NULL),
    ]
)
def optimization_flags(request: pytest.FixtureRequest):
    yield
