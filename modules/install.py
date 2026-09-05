import urllib.request as request
import urllib.error as error
from modules.lib import log, ROOTPATH

from os import path
from sys import argv as sys_argv
from json import loads


def main(argv):
    if len(argv) < 2:
        log('red', 'ERROR', 'please provide proper parameters')
        exit(1)

    log('', 'LOG', 'successful start')

    addr = f'http://{argv[1]}'

    manifest = addr + '/getManifest'


    try:
        with request.urlopen(manifest) as response:
            raw: bytes = response.read()

        avail: dict = loads(raw.decode())

        if not avail:
            log('yellow', 'WARNING', 'no packages in the host manifest; exiting')
            exit(1)

        log('green', 'INSTALLATION', 'fetched available packages')

        print('Available packages:')

        for i, j in avail.items():
            print(f"\t{i} ({j['version']}); {j['description']}")

        pkgn = input('\nEnter package name: ')

        if not avail.get(pkgn):
            log('red', 'ERROR', f'invalid package name: {pkgn}')
            exit(1)

        with request.urlopen(addr + f'/packages/{avail[pkgn]['filename']}') as content:
            raw: bytes = content.read()

        text = raw.decode()

        with open(path.join(ROOTPATH, 'downloads', avail[pkgn]['filename']), 'w', encoding='utf-8') as file:
            file.write(text)

        
    except error.HTTPError as e:
        log('red', 'ERROR', f'returned status code {e}')
    except error.URLError as e:
        log('red', 'ERROR', f'failed to reach server; {e.reason}')

if __name__ == '__main__':
    main(sys_argv)