from urllib.parse import urlparse


class Bouncer:
    def __init__(self, targets: dict[str, str] = None, active: str = None):
        if targets is None:
            self._targets = {}
        self._active = active

    @staticmethod
    def _validate_url(url: str) -> None:
        """Throws a ValueError if the url is invalid"""
        result = urlparse(url)
        try:
            assert result.netloc
            assert result.scheme
        except AssertionError:
            raise ValueError(f"Bad URL: {url}")

    def add_target(self, name, url) -> None:
        if name in self._targets:
            raise ValueError(f"Target exists: {name}, use 'update'")

        self._validate_url(url)
        self._targets[name] = url

    def add_targets(self, targets: dict[str, str]) -> None:
        for k, v in targets.items():
            self.add_target(k, v)

    def update_target(self, name, url) -> None:
        self._validate_url(url)
        self._targets[name] = url

    def update_targets(self, targets: dict[str, str]) -> None:
        for k, v in targets.items():
            self.update_target(k, v)

    @property
    def active(self) -> tuple[str, str]:
        if not self._targets:
            raise RuntimeError("No targets configured")

        if self._active is None:
            self._active = next(iter(self._targets.keys()))

        return self._active, self._targets[self._active]

    @active.setter
    def active(self, name: str):
        if not name in self._targets:
            raise KeyError("Attempted to set active target to missing key")

        self._active = name

    @property
    def targets(self):
        return self._targets
