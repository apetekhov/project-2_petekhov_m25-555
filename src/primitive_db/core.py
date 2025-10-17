from typing import Any

from src.primitive_db.decorators import confirm_action, handle_db_errors

VALID_TYPES = {"int", "str", "bool"}


@handle_db_errors
def create_table(metadata, table_name, columns):
    """Создает таблицу с указанными столбцами."""
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    table_structure = {"ID": "int"}

    for col in columns:
        try:
            name, col_type = col.split(":")
            if col_type not in VALID_TYPES:
                print(f"Некорректный тип данных: {col_type}. Попробуйте снова.")
                return metadata
            table_structure[name] = col_type
        except ValueError:
            print(f"Некорректное значение: {col}. Попробуйте снова.")
            return metadata

    metadata[table_name] = table_structure
    print(f'Таблица "{table_name}" успешно создана со столбцами: '
          f'{", ".join([f"{k}:{v}" for k, v in table_structure.items()])}')
    return metadata


@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


def _python_type(type_name: str) -> type:
    return {"int": int, "str": str, "bool": bool}[type_name]


def _validate_and_cast(values: list[Any], column_types: list[str]) -> list[Any]:
    """
    Проверить соответствие типов и при необходимости 
    привести (значения уже обычно Python-типы).
    """
    if len(values) != len(column_types):
        raise ValueError("Количество значений не соответствует количеству столбцов.")
    casted: list[Any] = []
    for val, type_name in zip(values, column_types, strict=False):
        py_t = _python_type(type_name)
        if isinstance(val, py_t):
            casted.append(val)
        else:
            if py_t is bool:
                if isinstance(val, str):
                    low = val.lower()
                    if low in {"true", "false"}:
                        casted.append(low == "true")
                        continue
                raise ValueError(f"Ожидался bool, получено: {val!r}")
            try:
                casted.append(py_t(val))
            except Exception as exc:
                raise ValueError(
                    f"Некорректный тип значения: {val!r} "
                    f"для {type_name}"
                ) from exc
    return casted


def _next_id(rows: list[dict]) -> int:
    """Вернуть следующий ID: max+1, если есть строки; иначе 1."""
    if not rows:
        return 1
    return max(int(r["ID"]) for r in rows) + 1


@handle_db_errors
def insert(
    metadata: dict, 
    table_name: str, 
    values: list[Any], 
    rows: list[dict],
) -> list[dict]:
    """Добавить запись (без ID в values, ID генерируется автоматически)."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return rows

    schema = metadata[table_name]
    columns = list(schema.keys())
    non_id_columns = columns[1:]
    non_id_types = [schema[c] for c in non_id_columns]

    try:
        casted = _validate_and_cast(values, non_id_types)
    except ValueError as e:
        print(f"Некорректное значение: {e}. Попробуйте снова.")
        return rows

    new_id = _next_id(rows)
    row = {"ID": new_id}
    for c, v in zip(non_id_columns, casted, strict=False):
        row[c] = v

    rows.append(row)
    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
    return rows


def _match_where(row: dict, where: dict | None) -> bool:
    if not where:
        return True
    for k, v in where.items():
        if k not in row or row[k] != v:
            return False
    return True


@handle_db_errors
def select(rows: list[dict], where: dict | None = None) -> list[dict]:
    """Вернуть все строки или отфильтрованные по where (словари с равенством)."""
    if not where:
        return rows
    return [r for r in rows if _match_where(r, where)]


@handle_db_errors
def update(
    rows: list[dict], 
    set_clause: dict, 
    where: dict | None = None,
) -> tuple[list[dict], int]:
    """Обновить строки по where, вернуть (rows, count)."""
    count = 0
    for r in rows:
        if _match_where(r, where):
            r.update(set_clause)
            count += 1
    return rows, count


@handle_db_errors
@confirm_action("удаление таблицы")
def delete(rows: list[dict], where: dict | None = None) -> tuple[list[dict], int]:
    """Удалить строки по where, вернуть (rows, count)."""
    if not where:
        filtered = []
        count = len(rows)
    else:
        filtered = [r for r in rows if not _match_where(r, where)]
        count = len(rows) - len(filtered)
    return filtered, count