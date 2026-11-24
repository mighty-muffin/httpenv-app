"""Read the Exposed Value from Infisical (see docs/adr/0002)."""

import logging
import os
import time
from collections.abc import Callable
from dataclasses import dataclass, replace
from datetime import datetime
from typing import Any, Self

from infisical_sdk import InfisicalSDKClient

SECRET_NAME = 'EXPOSED_VALUE'
DEFAULT_HOST = 'https://app.infisical.com'
# Log in again this many seconds before the access token expires.
TOKEN_RENEWAL_MARGIN = 60.0

logger = logging.getLogger(__name__)


class NeverFetchedError(RuntimeError):
    """No fetch of the Exposed Value has ever succeeded."""


@dataclass(frozen=True)
class Reading:
    """One observation of the Exposed Value."""

    value: str
    rotated_at: datetime
    stale: bool
    last_success_at: float


class InfisicalSource:
    """Fetches the Exposed Value of one Environment from Infisical."""

    def __init__(  # noqa: PLR0913
        self,
        *,
        client: Any,
        client_id: str,
        client_secret: str,
        project_id: str,
        environment: str,
        ttl: float = 60.0,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._client = client
        self._client_id = client_id
        self._client_secret = client_secret
        self._project_id = project_id
        self._environment = environment
        self._ttl = ttl
        self._clock = clock
        self._last: Reading | None = None
        self._token_expires_at = float('-inf')

    @classmethod
    def from_env(cls) -> Self:
        """Build a source from INFISICAL_* environment variables."""
        missing = [
            name
            for name in (
                'INFISICAL_CLIENT_ID',
                'INFISICAL_CLIENT_SECRET',
                'INFISICAL_PROJECT_ID',
                'INFISICAL_ENVIRONMENT',
            )
            if not os.environ.get(name)
        ]
        if missing:
            msg = f'Missing environment variables: {", ".join(missing)}'
            raise RuntimeError(msg)
        return cls(
            # cache_ttl=None: this class owns caching, so a cached SDK response
            # can never pass for a successful fetch (see docs/adr/0003).
            client=InfisicalSDKClient(
                host=os.environ.get('INFISICAL_HOST', DEFAULT_HOST), cache_ttl=None
            ),
            client_id=os.environ['INFISICAL_CLIENT_ID'],
            client_secret=os.environ['INFISICAL_CLIENT_SECRET'],
            project_id=os.environ['INFISICAL_PROJECT_ID'],
            environment=os.environ['INFISICAL_ENVIRONMENT'],
        )

    def fetch(self) -> Reading:
        """Return the Exposed Value, from cache while it is younger than the TTL."""
        now = self._clock()
        if self._last is not None and now - self._last.last_success_at < self._ttl:
            return self._last
        try:
            if now >= self._token_expires_at - TOKEN_RENEWAL_MARGIN:
                login = self._client.auth.universal_auth.login(
                    client_id=self._client_id, client_secret=self._client_secret
                )
                self._token_expires_at = now + login.expiresIn
            secret = self._client.secrets.get_secret_by_name(
                secret_name=SECRET_NAME,
                project_id=self._project_id,
                environment_slug=self._environment,
                secret_path='/',
            )
        except Exception as exc:
            if self._last is None:
                raise NeverFetchedError(
                    'The Exposed Value has never been fetched'
                ) from exc
            logger.warning(
                'Refreshing the Exposed Value failed; serving stale', exc_info=True
            )
            return replace(self._last, stale=True)
        self._last = Reading(
            value=secret.secretValue,
            rotated_at=datetime.fromisoformat(secret.updatedAt),
            stale=False,
            last_success_at=now,
        )
        return self._last
