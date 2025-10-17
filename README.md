## Управление таблицами

Программа представляет собой консольное приложение, имитирующее работу с базой данных.  
Доступные команды:

| Команда | Описание |
|----------|-----------|
| `create_table <имя> <столбец1:тип> <столбец2:тип> ...` | Создать таблицу |
| `list_tables` | Показать список всех таблиц |
| `drop_table <имя>` | Удалить таблицу |
| `help` | Показать справочную информацию |
| `exit` | Выйти из программы |

Поддерживаемые типы данных: **int**, **str**, **bool**.  
При создании таблицы автоматически добавляется служебный столбец **ID:int** (уникальный ключ).

---

### Пример использования

```bash
$ project

*** База данных запущена ***

Введите команду: create_table users name:str age:int is_active:bool
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool

Введите команду: list_tables
- users

Введите команду: drop_table users
Таблица "users" успешно удалена.

Введите команду: exit
Выход из программы...
```

## Демонстрация работы программы

[![asciicast](https://asciinema.org/a/bilWPp963RfAAYCnqLYBRuXrQ.svg)](https://asciinema.org/a/bilWPp963RfAAYCnqLYBRuXrQ)

## CRUD-операции

Программа поддерживает полный набор операций с данными (Create, Read, Update, Delete).

| Команда | Описание |
|----------|-----------|
| `insert into <имя> values (<v1>, <v2>, ...)` | Добавить запись в таблицу |
| `select from <имя>` | Показать все записи |
| `select from <имя> where <столбец> = <значение>` | Показать записи по условию |
| `update <имя> set <столбец> = <значение> where <столбец> = <значение>` | Обновить запись |
| `delete from <имя> where <столбец> = <значение>` | Удалить запись |
| `info <имя>` | Показать информацию о таблице |

---

### Пример использования CRUD

```bash
$ database
*** База данных запущена ***

*** Операции с данными ***
Функции:
<command> insert into <имя> values (<v1>, <v2>, ...) - создать запись
<command> select from <имя> where <колонка> = <значение> - выбрать по условию
<command> select from <имя> - выбрать все записи
<command> update <имя> set <k1>=<v1>[, ...] where <k>=<v> - обновить записи
<command> delete from <имя> where <k>=<v> - удалить записи
<command> info <имя> - информация о таблице

Общие команды:
<command> exit - выйти из программы
<command> help - справочная информация

Введите команду: create_table users name:str age:int is_active:bool
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool
Введите команду: insert into users values ("Artem", 28, true)
Запись с ID=1 успешно добавлена в таблицу "users".
Введите команду: insert into users values ("Sergei", 31, false)
Запись с ID=2 успешно добавлена в таблицу "users".
Введите команду: select from users
+----+--------+-----+-----------+
| ID |  name  | age | is_active |
+----+--------+-----+-----------+
| 1  | Artem  |  28 |    True   |
| 2  | Sergei |  31 |   False   |
+----+--------+-----+-----------+
Введите команду: select from users where age = 28
+----+-------+-----+-----------+
| ID |  name | age | is_active |
+----+-------+-----+-----------+
| 1  | Artem |  28 |    True   |
+----+-------+-----+-----------+
Введите команду: update users set age = 29 where name = "Artem"
Запись с ID=1 в таблице "users" успешно обновлена.
Введите команду: select from users
+----+--------+-----+-----------+
| ID |  name  | age | is_active |
+----+--------+-----+-----------+
| 1  | Artem  |  29 |    True   |
| 2  | Sergei |  31 |   False   |
+----+--------+-----+-----------+
Введите команду: delete from users where name = "Sergei"
Запись успешно удалена из таблицы "users".
Введите команду: select from users
+----+-------+-----+-----------+
| ID |  name | age | is_active |
+----+-------+-----+-----------+
| 1  | Artem |  29 |    True   |
+----+-------+-----+-----------+
Введите команду: info users
Таблица: users
Столбцы: ID:int, name:str, age:int, is_active:bool
Количество записей: 1
Введите команду: exit
Выход из программы...
```
### Демонстрация работы CRUD

[![asciicast](https://asciinema.org/a/J7S2Ux5qxMstBUnga0DZI6WFE.svg)](https://asciinema.org/a/J7S2Ux5qxMstBUnga0DZI6WFE)
