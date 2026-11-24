"""Test doubles for the Infisical SDK boundary."""

from types import SimpleNamespace

from app.exposed_value import InfisicalSource

ROTATED_AT = '2026-11-24T12:00:00.000Z'


class FakeClock:
    def __init__(self) -> None:
        self.now = 1000.0

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


class FakeInfisical:
    """Stands in for InfisicalSDKClient at the third-party boundary."""

    def __init__(self, value: str = 'first', token_ttl: int = 7200) -> None:
        self.value = value
        self.updated_at = ROTATED_AT
        self.token_ttl = token_ttl
        self.fail_fetch = False
        self.logins: list[tuple[str, str]] = []
        self.fetches: list[dict[str, str]] = []
        self.auth = SimpleNamespace(universal_auth=SimpleNamespace(login=self._login))
        self.secrets = SimpleNamespace(get_secret_by_name=self._get_secret_by_name)

    def _login(self, client_id: str, client_secret: str) -> SimpleNamespace:
        self.logins.append((client_id, client_secret))
        return SimpleNamespace(accessToken='token', expiresIn=self.token_ttl)

    def _get_secret_by_name(self, **kwargs: str) -> SimpleNamespace:
        if self.fail_fetch:
            raise ConnectionError('infisical unreachable')
        self.fetches.append(kwargs)
        return SimpleNamespace(secretValue=self.value, updatedAt=self.updated_at)


def make_source(infisical: FakeInfisical, clock: FakeClock) -> InfisicalSource:
    return InfisicalSource(
        client=infisical,
        client_id='reader-id',
        client_secret='reader-secret',
        project_id='project-123',
        environment='staging',
        clock=clock,
    )
