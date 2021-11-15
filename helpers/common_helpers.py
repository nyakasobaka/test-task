from typing import Any


def not_none_or_empty(value: Any, message: str = "Value should not be none or empty"):
    if not value:
        raise ValueError(message)
    return value


def not_none(value: Any, message: str = "Value should not be none"):
    if value is None:
        raise ValueError(message)
    return value


def ignore_case_xpath(attribute: str, value: str):
    return f"translate({attribute}, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') = '{value.lower()}'"
