from modules.lib import log

from os import path, listdir, chdir
from json import dump


def main(argv, origin):
    chdir(origin)
    
    if len(argv) < 2:
        log('red', 'ERROR', 'usage: python winpak.py -u [directory]')
        exit(1)
    else:
        if path.exists(argv[1]) and path.isdir(argv[1]):
            pass
        else:
            log('red', 'ERROR', "no such path / path isn't a directory")
            exit(1)

    log('', 'LOG', 'successful start')

    res = {}

    manpath = 'manifest.json'
    repopath = argv[1]

    if not listdir(repopath):
        log('yellow', 'WARNING', 'repository directory empty; returning')
        exit(1)

    log('', 'LOG', 'resolving files for the manifest')

    for i in listdir(repopath):
        if not path.isfile(path.join(repopath, i)):
            log('yellow', 'SKIPPED', f' {i}: is a directory', True)
            continue

        pkg = i[:i.rfind('.')]

        res[pkg] = {
            'filename': i,
            'description': 'TBA',
            'version': 'TBA'
        }

        log('green', 'RESOLVED', pkg, True)

    with open(manpath, 'w', encoding='utf-8') as file:
        dump(res, file, indent=4, ensure_ascii=False)
