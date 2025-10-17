import time
from typing import Any, Callable


def handle_db_errors(func: Callable) -> Callable:
    """Декоратор для централизованной обработки ошибок."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(
                "Ошибка: Файл данных не найден. "
                "Возможно, база данных не инициализирована."
            )
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
    return wrapper

def confirm_action(action_name: str) -> Callable:
    """Декоратор для подтверждения опасных действий."""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            answer = input(
                f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            ).strip().lower()
            if answer != "y":
                print("Операция отменена пользователем.")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator

def log_time(func: Callable) -> Callable:
    """Декоратор для измерения времени выполнения функции."""
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        end = time.monotonic()
        elapsed = end - start
        print(f"Функция {func.__name__} выполнилась за {elapsed:.3f} секунд.")
        return result
    return wrapper

def create_cacher() -> Callable:
    """Создает функцию для кэширования результатов."""
    cache: dict[str, Any] = {}

    def cache_result(key: str, value_func: Callable[[], Any]) -> Any:
        if key in cache:
            print(f"(из кэша) Запрос '{key}' найден.")
            return cache[key]
        result = value_func()
        cache[key] = result
        return result

    return cache_result
