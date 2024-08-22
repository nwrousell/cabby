def print_green(text: str, end: str = "\n"):
    print("\x1b[32m" + str(text) + "\x1b[0m", end=end)


def print_red(text: str, end: str = "\n"):
    print("\x1b[31m" + str(text) + "\x1b[0m", end=end)


def print_blue(text, end: str = '\n'):
    print(f'\033[34m' + str(text) + '\033[0m', end=end)