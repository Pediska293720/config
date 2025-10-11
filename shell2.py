import socket, os, sys

LOGIN = "Pediska"
HOSTNAME = socket.gethostname()

def parse_arguments():
    vfs_path = None
    script = None

    if '--vfs-path' in sys.argv:
        idx = sys.argv.index('--vfs-path')
        if idx + 1 < len(sys.argv):
            vfs_path = sys.argv[idx + 1]
    if '--script' in sys.argv:
        idx = sys.argv.index('--script')
        if idx + 1 < len(sys.argv):
            script = sys.argv[idx + 1]
    return vfs_path, script


def parse_command(user_input):
    args = []
    user_input = user_input.replace("'", '"')
    command = user_input.split()[0]

    args_in_quotes = []
    line_in_quotes = ""
    quotes_is_open = False

    for symbol in user_input:
        if symbol == '"':
            if quotes_is_open:
                quotes_is_open = False
                args_in_quotes.append(f'"{line_in_quotes}"')
                line_in_quotes = ""
            else:
                quotes_is_open = True
        else:
            if quotes_is_open:
                line_in_quotes += symbol
    if quotes_is_open:
        print("Error: unterminated quotes")
        return None, []

    if args_in_quotes:
        arg = args_in_quotes[0].removesuffix('"').removeprefix('"')
        if arg in command:
            command = arg
            user_input = user_input.replace(f'"{arg}"', "", 1)
        else:
            args.append(arg)
            user_input = user_input.replace(f'"{arg}"', "", 1)

        for arg in args_in_quotes[1:]:
            args.append(arg.removeprefix('"').removesuffix('"'))
            user_input = user_input.replace(f'{arg}', "", 1)

    another_args = user_input.split()[1:]
    args.extend(another_args)

    return command, args

def setup_vfs(vfs_path=None):
    if vfs_path is None:
        vfs_path = "vfs_data"

    if not os.path.exists(vfs_path):
        os.makedirs(vfs_path)

    return vfs_path

def execute_script(script_path):
    if not os.path.exists(script_path):
        print(f"Error: script file not found: {script_path}")
        return False
    try:
        with open(script_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        print(f'--- Выполнение скрипта: {script_path} ---')

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):#обработка комментариев
                continue
            print(f'{LOGIN}@{HOSTNAME}:/>  {line}')
            command, args = parse_command(line)

            if command == "exit":
                print('Exit from the shell. Bye.')
                return True
            elif command == "ls":
                print(f"Command: {command}, arguments: {args}")
            elif command == "cd":
                print(f"Command: {command}, arguments: {args}")
        return False

    except Exception as e:
        print(f"Error {e}")
        return False

def test_parser():
    test_line = ['""','"', 'cd "kitten"',
                 'ls "hello world"', "cd 'again hello world'",
                 'cd "arg1" "arg2" "arg3"',
                 'ls "arg1" arg2', "''",
                 'command "arg1" arg2 "arg3"',
                 'cmd "partial"arg'
    ]
    print('===== TEST PARSER =====')
    for test in test_line:
        cmd, args = parse_command(test)
        print(f"input: '{test}' -> command: {cmd}, args: {args}")


def main():
    vfs, scr = parse_arguments()

    print(f'VFS Path: {vfs or "vfs_data (default)"}')
    print(f'Script: {scr or "not specified"}')

    vfs_root = setup_vfs(vfs)

    if scr:
        should_exit = execute_script(scr)
        if should_exit:
            return

    while True:
        user_input = input(f'{LOGIN}@{HOSTNAME}:/>  ').strip()
        if not user_input:
            continue
        command, args = parse_command(user_input)

        if command == "exit":
            print('Exit from the shell. Bye.')
            break
        elif command == "ls":
            print(f"Command: {command}, arguments: {args}")
        elif command == "cd":
            print(f"Command: {command}, arguments: {args}")


if __name__ == "__main__":
    main()
