import json
import os


def load_metadata(filepath):
    """Загружает метаданные из JSON-файла."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    """Сохраняет метаданные в JSON-файл."""
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


DATA_DIR = "data"


def _ensure_data_dir() -> None:
    """Создать каталог data/ при необходимости."""
    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)


def _table_path(table_name: str) -> str:
    """Вернуть путь к файлу данных таблицы."""
    _ensure_data_dir()
    return os.path.join(DATA_DIR, f"{table_name}.json")


def load_table_data(table_name: str) -> list[dict]:
    """
    Загрузить данные таблицы из data/<table>.json. 
    Если файла нет — вернуть пустой список.
    """
    path = _table_path(table_name)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_table_data(table_name: str, data: list[dict]) -> None:
    """Сохранить данные таблицы в data/<table>.json."""
    path = _table_path(table_name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
