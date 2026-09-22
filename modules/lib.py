from os import path
from base64 import b64encode, b64decode


COLORS = {
    'clear': '\033[0m',
    'red': '\033[31m',
    'yellow': '\033[33m',
    'green': '\033[32m',
} # color constant for the log function

IGNORE_EXTENSIONS = ('.pyc') # formats to ignore for build.py

def readfile(filepath: str) -> str: # function for reading files in binary mode
    if path.exists(filepath) and path.isfile(filepath):
        with open(filepath, 'rb') as file:
            return b64encode(file.read()).decode()
    else:
        return ''

def writefile(filepath: str, data: str) -> None: # function for writing files in binary mode
    with open(filepath, 'wb') as file:
        file.write(b64decode(data))

def writefile_plain(filepath: str, text: str) -> None:
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(text)


def log(color: str, header: str, description: str, indent: bool = False) -> None: # function for easier output during exexcution
    global COLORS

    if indent == False:
        if color.lower() in COLORS:
            print(f"{COLORS[color.lower()]}[{header}]{COLORS['clear']}: {description}")
        else:
            print(f'[{header}]: {description}')
    else:
        if color.lower() in COLORS:
            print(f"\t{COLORS[color.lower()]}[{header}]{COLORS['clear']}: {description}")
        else:
            print(f'\t[{header}]: {description}')
            