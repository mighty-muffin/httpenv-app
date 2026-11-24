"""Fixtures that swap the app's Infisical reader for a fake."""

from collections.abc import Iterator

import pytest
from app.main import app, get_exposed_value_source

from tests.fakes import FakeClock, FakeInfisical, make_source


@pytest.fixture
def clock() -> FakeClock:
    return FakeClock()


@pytest.fixture
def infisical(
    monkeypatch: pytest.MonkeyPatch, clock: FakeClock
) -> Iterator[FakeInfisical]:
    monkeypatch.setenv('APP_ENVIRONMENT', 'staging')
    monkeypatch.setenv('APP_VERSION', '1.2.3')
    fake = FakeInfisical(value='first')
    source = make_source(fake, clock)
    app.dependency_overrides[get_exposed_value_source] = lambda: source
    yield fake
    app.dependency_overrides.clear()
