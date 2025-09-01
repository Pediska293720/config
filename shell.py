def main():

    while True:
        user_input = input('-> ').strip()

        if not user_input:
            continue
        parts_input = user_input.split()
        command_input = parts_input[0]
        args_input = parts_input[1:]

        if command_input == "exit":
            print('EXIT')
            break

        if command_input == "ls":
            print("Вот список файлов и каталогов текущей директории:")

        if command_input == "cd":
            print(f"Переход в указанный каталог по пути {args_input}")

        if command_input == "pwd":
            print("Вот полный путь к текущей директории")

        if command_input == "mkdir":
            print(f"Создание нового каталога с названием {args_input}")

        if command_input == "rm":
            print(f"Удаление файла с названием {args_input}")

        commands = ['ls', 'cd', 'pwd', 'mkdir', 'rm']
main()


