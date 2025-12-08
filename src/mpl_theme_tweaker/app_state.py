from typing import Any

_app: dict[str, Any] = {}


def set_app_key(key: str, value: Any) -> None:
    _app[key] = value
    return


def get_app_key(key: str) -> Any:
    return _app.get(key)
