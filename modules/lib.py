from os import path
from pathlib import Path


COLORS = {
    'clear': '\033[0m',
    'red': '\033[31m',
    'yellow': '\033[33m',
    'green': '\033[32m',
} # color constant for the log function

ROOTPATH = Path(__file__).resolve().parent.parent

def readfile(filepath: str) -> str: # function for reading files
    if path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception:
            return ""
    else:
        return ""

def writefile(filepath: str, data: bytes) -> None: # function for writing / overwriting / creating files
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(data)


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