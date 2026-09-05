from sys import argv as sys_argv
from os import makedirs, path
from shutil import rmtree
from subprocess import call
from time import perf_counter as time

from modules.lib import *


def main(argv):
    if len(argv) < 2:
        log('red', 'ERROR', 'please provide a proper file path')
        exit(1)
    else:
        if path.exists(argv[1]):
            filename = argv[1]
        else:
            if path.exists(argv[1] + '.pak'):
                filename = argv[1] + '.pak'
            else:
                log('red', 'ERROR', 'no such path / path is a directory')
                exit(1)


    start = time()

    log('', 'LOG', 'successful start')

    if '--clean' in argv:
        if path.exists(argv[1]) and path.isdir(argv[1]) and argv[1] != '.' and argv[1] != '..':
            rmtree(argv[1])

        log('green', '--CLEAN', 'success')
        exit(0)


    commands = []

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            lstr = line.strip()

            if lstr == '[/* FILEWRITE */]':
                fn = next(file).strip()

                log('yellow', 'DEPLOY', f'writing to file {fn}')
                
                with open(fn, 'w', encoding='utf-8') as file_writer:
                    for nline in file:
                        nlstr = nline.strip()

                        if nlstr == '[/* END */]':
                            break
                        else:
                            file_writer.write(nline)

                log('green', 'DEPLOY', f'successfully wrote to file {fn}')

            elif lstr == '[/* MKDIR */]':
                fn = next(file)
                makedirs(fn, exist_ok=True)
                log('green', 'DEPLOY', f'created directory {fn}')

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


if __name__ == "__main__":
    main(sys_argv)