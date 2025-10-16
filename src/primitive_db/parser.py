import shlex
from typing import Any


def _parse_literal(token: str) -> Any:
    """
    Преобразовать строковый токен в Python-тип: int, bool, str (в кавычках).
    """
    if (
        len(token) >= 2
        and (
            (token[0] == token[-1] == '"')
            or (token[0] == token[-1] == "'")
        )
    ):
        return token[1:-1]

    low = token.lower()
    if low == "true":
        return True
    if low == "false":
        return False

    if token.isdigit() or (token.startswith("-") and token[1:].isdigit()):
        try:
            return int(token)
        except ValueError:
            pass

    return token


def parse_values(values_segment: str) -> list[Any]:
    """Разобрать часть вида: '(\"Sergei\", 28, true)' → список значений."""
    text = values_segment.strip()
    if text.startswith("(") and text.endswith(")"):
        text = text[1:-1]

    lexer = shlex.shlex(text, posix=True)
    lexer.whitespace = ","
    lexer.whitespace_split = True
    tokens = list(lexer)
    return [_parse_literal(t.strip()) for t in tokens if t.strip() != ""]


def parse_where(where_segment: str) -> dict:
    """Разобрать 'age = 28' → {'age': 28}. Поддерживаем одно равенство."""
    parts = where_segment.split("=", maxsplit=1)
    if len(parts) != 2:
        raise ValueError("Ожидалось выражение формата: <столбец> = <значение>")
    key = parts[0].strip()
    val = _parse_literal(parts[1].strip())
    return {key: val}


def parse_set(set_segment: str) -> dict:
    """Разобрать 'age = 29, is_active = false' → {'age': 29, 'is_active': False}."""
    lexer = shlex.shlex(set_segment, posix=True)
    lexer.whitespace = ","
    lexer.whitespace_split = True
    pairs = [p.strip() for p in lexer if p.strip()]

    result: dict = {}
    for pair in pairs:
        kv = pair.split("=", maxsplit=1)
        if len(kv) != 2:
            raise ValueError(f"Некорректное выражение в set: {pair!r}")
        key = kv[0].strip()
        val = _parse_literal(kv[1].strip())
        result[key] = val
    return result
