from modules.lib import log

from os import path, listdir, chdir
from json import dump, load


def main(argv, origin):
    chdir(origin)
    
    if len(argv) < 1:
        log('red', 'ERROR', 'usage: python winpak.py updMan [directory]')
        exit(1)
    else:
        if path.exists(argv[0]) and path.isdir(argv[0]):
            pass
        else:
            log('red', 'ERROR', "no such path / path isn't a directory")
            exit(1)

    log('', 'LOG', 'successful start')

    res = {}

    manpath = 'manifest.json'
    repopath = argv[0]
    
    with open(path.join(manpath), 'r', encoding='utf-8') as man:
        res = load(man)

    if not listdir(repopath):
        log('yellow', 'WARNING', 'repository directory empty; returning')
        exit(1)

    log('', 'LOG', 'resolving files for the manifest')

    for i in listdir(repopath):
        if path.exists(i):
            if not path.isfile(path.join(repopath, i)):
                log('yellow', 'SKIPPED', f' {i}: is a directory', True)
                continue

            pkg = i[:i.rfind('.')]

            if not pkg in res.keys():
                res[pkg] = {
                    'filename': i,
                    'description': 'TBA',
                    'version': 'TBA'
                }

            log('green', 'RESOLVED', pkg, True)

    with open(manpath, 'w', encoding='utf-8') as file:
        dump(res, file, indent=4, ensure_ascii=False)
