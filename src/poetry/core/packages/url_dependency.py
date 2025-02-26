from __future__ import annotations

from typing import Iterable
from urllib.parse import urlparse

from poetry.core.packages.dependency import Dependency


class URLDependency(Dependency):
    def __init__(
        self,
        name: str,
        url: str,
        groups: Iterable[str] | None = None,
        optional: bool = False,
        resolve_order: int | None = None,
        extras: Iterable[str] | None = None,
    ) -> None:
        self._url = url

        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"{url} does not seem like a valid url")

        super().__init__(
            name,
            "*",
            groups=groups,
            optional=optional,
            allows_prereleases=True,
            source_type="url",
            source_url=self._url,
            resolve_order=resolve_order,
            extras=extras,
        )

    @property
    def url(self) -> str:
        return self._url

    @property
    def base_pep_508_name(self) -> str:
        requirement = self.pretty_name

        if self.extras:
            extras = ",".join(sorted(self.extras))
            requirement += f"[{extras}]"

        requirement += f" @ {self._url}"

        return requirement

    def is_url(self) -> bool:
        return True
