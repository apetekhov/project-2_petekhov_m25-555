import shlex

from prettytable import PrettyTable

from src.primitive_db.constants import META_FILE
from src.primitive_db.core import (
    create_table,
    drop_table,
)
from src.primitive_db.core import (
    delete as core_delete,
)
from src.primitive_db.core import (
    insert as core_insert,
)
from src.primitive_db.core import (
    select as core_select,
)
from src.primitive_db.core import (
    update as core_update,
)
from src.primitive_db.parser import parse_set, parse_values, parse_where
from src.primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


def print_help() -> None:
    """Вывод справочной информации о командах."""
    print("\n*** Операции с данными ***")
    print("Функции:")
    print("<command> insert into <имя> values (<v1>, <v2>, ...) - создать запись")
    print(
        "<command> select from <имя> where <колонка> = <значение> "
        "- выбрать по условию"
    )
    print("<command> select from <имя> - выбрать все записи")
    print("<command> update <имя> set <k1>=<v1>[, ...] where <k>=<v> - обновить записи")
    print("<command> delete from <имя> where <k>=<v> - удалить записи")
    print("<command> info <имя> - информация о таблице")
    print("\nОбщие команды:")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация\n")


def _print_table(rows: list[dict]) -> None:
    """Вывести записи в виде таблицы PrettyTable."""
    if not rows:
        print("Нет записей.")
        return
    headers = list(rows[0].keys())
    table = PrettyTable()
    table.field_names = headers
    for r in rows:
        table.add_row([r.get(h, "") for h in headers])
    print(table)


def run() -> None:
    """Главный цикл консольного приложения."""
    metadata = load_metadata(META_FILE)

    print("\n*** База данных запущена ***")
    print_help()

    while True:
        try:
            user_input = input("Введите команду: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход из программы...")
            break

        if not user_input:
            continue

        args = shlex.split(user_input)
        cmd = args[0]

        if cmd == "exit":
            print("Выход из программы...")
            break

        elif cmd == "help":
            print_help()

        elif cmd == "list_tables":
            if metadata:
                for t in metadata.keys():
                    print("-", t)
            else:
                print("Таблиц пока нет.")

        elif cmd == "create_table":
            if len(args) < 3:
                print("Ошибка: недостаточно аргументов.")
                continue
            table_name = args[1]
            columns = args[2:]
            metadata = create_table(metadata, table_name, columns)
            save_metadata(META_FILE, metadata)

        elif cmd == "drop_table":
            if len(args) < 2:
                print("Ошибка: укажите имя таблицы.")
                continue
            table_name = args[1]
            metadata = drop_table(metadata, table_name)
            save_metadata(META_FILE, metadata)

        # ---------- CRUD-команды ----------
        elif cmd == "insert":
            if len(args) < 5 or args[1] != "into" or args[3] != "values":
                print("Ошибка: используйте формат: insert into <имя> values (<...>)")
                continue
            table_name = args[2]
            try:
                after_values = user_input.split("values", maxsplit=1)[1].strip()
                values = parse_values(after_values)
            except Exception as e:
                print(f"Некорректное значение: {e}. Попробуйте снова.")
                continue

            rows = load_table_data(table_name)
            rows = core_insert(metadata, table_name, values, rows)
            save_table_data(table_name, rows)

        elif cmd == "select":
            if len(args) < 3 or args[1] != "from":
                print("Ошибка: используйте формат: select from <имя> [where ...]")
                continue
            table_name = args[2]
            rows = load_table_data(table_name)

            where = None
            if len(args) > 3:
                if args[3] != "where":
                    print("Ошибка: используйте формат: select from <имя> [where ...]")
                    continue
                where_segment = user_input.split("where", maxsplit=1)[1].strip()
                try:
                    where = parse_where(where_segment)
                except Exception as e:
                    print(f"Некорректное значение: {e}. Попробуйте снова.")
                    continue

            result = core_select(rows, where)
            _print_table(result)

        elif cmd == "update":
            if len(args) < 5 or args[2] != "set":
                print("Ошибка: используйте формат: update <имя> set <...> where <...>")
                continue
            table_name = args[1]
            if " where " not in user_input:
                print("Ошибка: укажите условие where.")
                continue

            set_segment = (
                user_input.split(" set ", maxsplit=1)[1]
                .split(" where ", maxsplit=1)[0]
                .strip()
            )
            where_segment = user_input.split(" where ", maxsplit=1)[1].strip()
            try:
                set_clause = parse_set(set_segment)
                where = parse_where(where_segment)
            except Exception as e:
                print(f"Некорректное значение: {e}. Попробуйте снова.")
                continue

            rows = load_table_data(table_name)
            rows, count = core_update(rows, set_clause, where)
            save_table_data(table_name, rows)
            if count > 0:
                ids = [
                    r["ID"]
                    for r in rows 
                    if all(r.get(k) == v for k, v in set_clause.items())
                ]
                if len(ids) == 1:
                    print(
                        f'Запись с ID={ids[0]} в таблице "{table_name}" '
                        f'успешно обновлена.'
                    )
                else:
                    print(f"Обновлено записей: {count}")
            else:
                print("Подходящих записей не найдено.")

        elif cmd == "delete":
            if len(args) < 4 or args[1] != "from" or args[3] != "where":
                print("Ошибка: используйте формат: delete from <имя> where <...>")
                continue
            table_name = args[2]
            where_segment = user_input.split("where", maxsplit=1)[1].strip()
            try:
                where = parse_where(where_segment)
            except Exception as e:
                print(f"Некорректное значение: {e}. Попробуйте снова.")
                continue

            rows = load_table_data(table_name)
            rows, count = core_delete(rows, where)
            save_table_data(table_name, rows)
            if count == 1:
                print(f'Запись успешно удалена из таблицы "{table_name}".')
            elif count > 1:
                print(f"Удалено записей: {count}")
            else:
                print("Подходящих записей не найдено.")

        elif cmd == "info":
            if len(args) < 2:
                print("Ошибка: укажите имя таблицы.")
                continue
            table_name = args[1]
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue
            schema = metadata[table_name]
            rows = load_table_data(table_name)
            cols_str = ", ".join(f"{k}:{v}" for k, v in schema.items())
            print(f"Таблица: {table_name}")
            print(f"Столбцы: {cols_str}")
            print(f"Количество записей: {len(rows)}")

        else:
            print(f"Функции {cmd!r} нет. Попробуйте снова.")
