from datetime import UTC, datetime

import pytest
from app.exposed_value import NeverFetchedError

from tests.fakes import FakeClock, FakeInfisical, make_source


def test_first_fetch_logs_in_and_returns_the_exposed_value():
    infisical = FakeInfisical(value='first')
    source = make_source(infisical, FakeClock())

    reading = source.fetch()

    assert infisical.logins == [('reader-id', 'reader-secret')]
    assert infisical.fetches == [
        {
            'secret_name': 'EXPOSED_VALUE',
            'project_id': 'project-123',
            'environment_slug': 'staging',
            'secret_path': '/',
        }
    ]
    assert reading.value == 'first'
    assert reading.rotated_at == datetime(2026, 11, 24, 12, 0, tzinfo=UTC)
    assert reading.stale is False


def test_fetch_within_the_cache_window_does_not_call_infisical_again():
    infisical = FakeInfisical(value='first')
    clock = FakeClock()
    source = make_source(infisical, clock)
    source.fetch()

    infisical.value = 'rotated'
    clock.advance(59)
    reading = source.fetch()

    assert len(infisical.fetches) == 1
    assert reading.value == 'first'
    assert reading.stale is False


def test_fetch_after_the_cache_window_returns_the_rotated_value():
    infisical = FakeInfisical(value='first')
    clock = FakeClock()
    source = make_source(infisical, clock)
    source.fetch()

    infisical.value = 'rotated'
    infisical.updated_at = '2026-11-24T18:00:00.000Z'
    clock.advance(60)
    reading = source.fetch()

    assert reading.value == 'rotated'
    assert reading.rotated_at == datetime(2026, 11, 24, 18, 0, tzinfo=UTC)
    assert reading.last_success_at == clock.now


def test_failed_refresh_serves_the_last_value_marked_stale():
    infisical = FakeInfisical(value='first')
    clock = FakeClock()
    source = make_source(infisical, clock)
    first = source.fetch()

    infisical.fail_fetch = True
    clock.advance(120)
    reading = source.fetch()

    assert reading.value == 'first'
    assert reading.stale is True
    assert reading.last_success_at == first.last_success_at


def test_failed_first_fetch_raises_never_fetched():
    infisical = FakeInfisical()
    infisical.fail_fetch = True
    source = make_source(infisical, FakeClock())

    with pytest.raises(NeverFetchedError):
        source.fetch()


def test_refresh_reuses_the_login_until_the_token_is_about_to_expire():
    infisical = FakeInfisical(token_ttl=300)
    clock = FakeClock()
    source = make_source(infisical, clock)
    source.fetch()

    clock.advance(60)
    source.fetch()
    assert len(infisical.logins) == 1

    clock.advance(180)  # 240s into a 300s token: inside its last minute
    source.fetch()
    assert len(infisical.logins) == 2  # noqa: PLR2004
