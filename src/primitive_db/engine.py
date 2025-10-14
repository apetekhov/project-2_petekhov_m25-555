import prompt

def welcome():
    """
    Приветственная функция.
    Отображает команды help/exit и принимает ввод пользователя.
    """
    print("***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")

    while True:
        command = prompt.string("Введите команду: ")

        if command == "exit":
            print("Выход из программы...")
            break
        elif command == "help":
            print("<command> exit - выйти из программы")
            print("<command> help - справочная информация")
        else:
            print(f"Неизвестная команда: {command}")
