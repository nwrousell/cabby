from datetime import datetime

''' Printing Utility Functions '''

def debug_print(statements=[], end='\n'):
    ct = datetime.now()
    print('[', str(ct)[:19], '] ', sep='', end='')
    for statement in statements:
        print(statement, end=' ')
    print(end=end)


def print_green(text: str, end: str = "\n"):
    print("\x1b[32m" + str(text) + "\x1b[0m", end=end)


def print_red(text: str, end: str = "\n"):
    print("\x1b[31m" + str(text) + "\x1b[0m", end=end)


def print_blue(text, end: str = '\n'):
    print(f'\033[34m' + str(text) + '\033[0m', end=end)


def inspect_prompt(system_prompt: str, user_prompt: str):
    print('----------------')
    print(system_prompt)
    print('----------------')
    print_green(user_prompt)


def inspect_response(response: str):
    print('----------------')
    print_red(response)
    print('----------------')


def inspect_retrieved_chunks(chunks: list):
    for i in range(len(chunks)):
        print(f'Chunk {i}:\n\n')
        print_blue(chunks[i])
        print('----------------')

def prettyprint_json(d: dict):
    res = ''
    for k, v in d.items():
        res += f'#### {k}:\n {v}\n\n'
    return res


def format_sources(sources: dict) -> str:
    if sources is None:
        return 'NONE'
    sources_string = ''
    for name, source in sources.items():
        sources_string += f'<{name}>\n'
        for chunk in source:
            sources_string += f"<{chunk['title']}>\n {chunk['data']}\n </{chunk['title']}>"
        sources_string += '\n</{name}>\n\n'
    return sources_string
