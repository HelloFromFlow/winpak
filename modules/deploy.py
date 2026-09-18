from modules.lib import *

from os import makedirs, path, chdir
from shutil import rmtree
from subprocess import call
from time import perf_counter as time


def main(argv, origin):
    chdir(origin)

    if len(argv) < 1:
        log('red', 'ERROR', 'usage: python winpak.py deploy [filename]')
        exit(1)
    else:
        if path.exists(argv[0]) and path.isfile(argv[0]):
            filename = argv[0]
        else:
            if path.exists(argv[0] + '.pak') and path.isfile(argv[0] + '.pak'):
                filename = argv[0] + '.pak'
            else:
                log('red', 'ERROR', 'no such path / path is a directory')
                exit(1)

    
    start = time()

    log('', 'LOG', 'successful start')

    if '--clean' in argv:
        clean, _ = path.splitext(filename)
        if path.exists(clean) and path.isdir(clean) and not '.' in clean and not '..' in clean:
            rmtree(clean)
            log('green', '--CLEAN', 'success')
            exit(0)
        else:
            log('red', '--CLEAN', 'no such directory')
            exit(1)


    commands = []

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            lstr = line.strip()

            if lstr == '[/* FILEWRITE */]':
                fn = next(file).strip()

                log('yellow', 'DEPLOY', f'writing to file {fn}')

                write_text = ''

                for nline in file:
                    nlstr = nline.strip()

                    if nlstr == '[/* END */]':
                        break
                    else:
                        write_text += nlstr

                writefile(fn, write_text)

            elif lstr == '[/* MKDIRS */]':
                for nline in file:
                    nlstr = nline.strip()

                    if nlstr == '[/* END */]':
                        break
                    else:
                        makedirs(nlstr, exist_ok=True)
                        log('green', 'DEPLOY', f'created directory {nlstr}')

            elif lstr == '[/* TERMINAL-COMMANDS */]':
                for nline in file:
                    nlstr = nline.strip()

                    if nlstr in '\n\t ':
                        continue
                    elif nlstr == '[/* END */]':
                        break
                    else:
                        commands.append(nlstr)

    if '--run' in argv:
        if len(commands) > 0:
            for i in commands:
                call(i, shell=True)

    end = time()

    log('', 'LOG', f'took {end - start}')
