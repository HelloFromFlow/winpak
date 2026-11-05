from modules.lib import log

from os import chdir, path
from base64 import b64decode


def main(argv, origin):
    chdir(origin)

    if len(argv) < 2:
        log('red', 'ERROR', 'usage: python winpak.py inspect [filename] [dirs/files/cmds/clean/file]')
        exit(1)
    else:
        if path.exists(argv[0]) and path.isfile(argv[0]):
            pass
        else:
            log('red', 'ERROR', "no such path / path isn't a file")

    filename = argv[0]
    option = argv[1]

    if option == 'dirs':
        dirs = []

        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                lstr = line.strip()

                if lstr == '[/* MKDIRS */]':
                    for nline in file:
                        nlstr = nline.strip()

                        if nlstr == '[/* END */]':
                            break
                        else:
                            dirs.append(nlstr)

        for i in dirs:
            print(i)

    elif option == 'files':
        files = []

        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                lstr = line.strip()

                if lstr == '[/* FILEWRITE */]':
                    fn = next(file).strip()

                    files.append(fn)

        for i in files:
            print(i)

    elif option == 'cmds':
        cmds = []

        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                lstr = line.strip()

                if lstr == '[/* TERMINAL-COMMANDS */]':
                    for nline in file:
                        nlstr = nline.strip()

                        if nlstr == '[/* END */]':
                            break
                        else:
                            cmds.append(nlstr)

        for i in cmds:
            print(i)

    elif option == 'clean':
        clean = []

        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                lstr = line.strip()

                if lstr == '[/* CLEAN-TARGS */]':
                    for nline in file:
                        nlstr = nline.strip()

                        if nlstr == '[/* END */]':
                            break
                        else:
                            clean.append(nlstr)

        for i in clean:
            print(i)

    if option == 'file':
        if len(argv) < 3:
            log('red', 'ERROR', 'usage: python winpak.py inspect file [filename]')
            exit(1)

        fname = argv[2]

        text = ''

        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                lstr = line.strip()

                if lstr == fname:
                    for nline in file:
                        nlstr = nline.strip()

                        if nlstr.strip() == '[/* END */]':
                            break
                        else:
                            text += nlstr

        if text != '':
            print(b64decode(text).decode())
        else:
            log('red', 'ERROR', f'file \"{fname}\" not found in {filename}')