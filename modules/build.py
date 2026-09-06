from sys import argv as sys_argv
from os import walk
from time import perf_counter as time

from modules.lib import *


def main(argv):

    if len(argv) < 2:
        log('red', 'ERROR', 'please provide a proper directory name')
        exit(1)
    else:
        if path.exists(argv[1]) and path.isdir(argv[1]):
            pass
        else:
            log('red', 'ERROR', "no such path / path isn't a directory")
            exit(1)

    start = time()

    log('', 'LOG', 'successful start')


    target = argv[1]
    main = target + '.pak'
    text = ''
    cmds = ''

    final_files = {}
    final_dirs = []

    log('yellow', 'PRE-BUILD', 'collecting requirements')
        
    for root, dirs, files in walk(target):

        if files:
            for file in files:
                if file.lower().endswith(IGNORE_EXTENSIONS):
                    continue

                filepath = path.join(root, file)

                if file.lower().endswith(BINARY_EXTENSIONS):
                    final_files[filepath] = readfile_bin(filepath)
                else:
                    final_files[filepath] = readfile(filepath)

        if dirs:
            for direc in dirs:
                if '__pycache__' in direc or direc.endswith('.zip'):
                    pass
                else:
                    dirpath = path.join(root, direc)

                    final_dirs.append(dirpath)

    log('yellow', 'BUILD', 'resolving directories:')

    text += '[/* MKDIRS */]\n' + target + '\n'
    for fdir in final_dirs:
        text += fdir + '\n'
        log('green', 'RESOLVED', f'{str(fdir)}', True)

    text += '[/* END */]\n\n'

    log('yellow', 'BUILD', 'resolving files:')

    for ffile, ffcontent in final_files.items():
        if ffile.endswith(BINARY_EXTENSIONS):
            text += '[/* FILEWRITE-BIN */]\n' + ffile + '\n' + ffcontent + '\n' + '[/* END */]\n\n'
        else:
            text += '[/* FILEWRITE */]\n' + ffile + '\n' + ffcontent + '\n' + '[/* END */]\n\n'

        log('green', 'RESOLVED', f'{str(ffile)}', True)

    if '--compile' in argv:
        for ffile in final_files.keys():
            ffile: str
            if ffile.endswith('.c'):
                cmds += f'gcc {ffile} -o {ffile[:-2]}\n'
                log('green', 'ADDED', f'compiler instruction for {ffile}')
            elif ffile.endswith('.cpp'):
                cmds += f'g++ {ffile} -o {ffile [:-4]}\n'
                log('green', 'ADDED', f'compiler instruction for {ffile}')

    if cmds:
        text += '[/* TERMINAL-COMMANDS */]\n' + cmds + '[/* END */]\n\n'

    text += '[/* CLEAN-TARGS */]\n' + target + '\n[/* END */]\n\n'

    log('green', 'ADDED', 'added clean instructions')

    writefile(main, text)

    log('green', 'LOG', f'successfully wrote to {main}')

    end = time()

    log('', 'LOG', f'took {end - start}')

if __name__ == "__main__":
    main(sys_argv)