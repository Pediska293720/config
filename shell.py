import socket, sys


LOGIN = "Pediska"
HOSTNAME = socket.gethostname()

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
def another_parse_command(user_input):
    pass
def test_parser():
    test_line = ['""','"', 'cd "kitten"',
                 'ls "hello world"', "cd 'again hello world'",
                 'cd "arg1" "arg2" "arg3"',
                 'ls "arg1" arg2', "''",
                 'command "arg1" arg2 "arg3"',
                 'cmd "partial"arg'
    ]
    for test in test_line:
        cmd, args = parse_command(test)
        print(f"input: '{test}' -> command: {cmd}, args: {args}")

def main():
    while True:
        user_input = input('VFS:/>  ').strip()
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
    if len(sys.argv) == 1:
        print("\n" + "=" * 50 + "\n")
        test_parser()
        print("\n" + "=" * 50 + "\n")
    main()
