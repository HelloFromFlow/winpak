import urllib.request as request
import urllib.error as error
from modules.lib import log
import modules.deploy as deploy

from os import path
from json import loads
from shutil import copyfileobj


def main(argv, origin):
    if len(argv) < 2:
        log('red', 'ERROR', 'usage: python winpak.py install [IP:Port] [package name]')
        exit(1)

    log('', 'LOG', 'successful start')

    addr = f'http://{argv[0]}'
    manifest = addr + '/getManifest'
    pkgn = argv[1]

    try:
        with request.urlopen(manifest) as response:
            raw: bytes = response.read()

        avail: dict = loads(raw.decode())

        if not avail:
            log('yellow', 'WARNING', 'no packages in the host manifest; exiting')
            exit(1)

        log('green', 'INSTALLATION', 'fetched available packages')

        if not avail.get(pkgn):
            log('red', 'ERROR', f'invalid package name: {pkgn}')
            exit(1)

        log('green', 'INSTALLATION', f'package {pkgn}:')

        log('', 'DESCRIPTION', avail[pkgn]['description'])
        log('', 'VERSION', avail[pkgn]['version'])

        log('yellow', 'INSTALLATION', 'downloading...')

        with request.urlopen(addr + f'/packages/{avail[pkgn]['filename']}') as content:
            with open(path.join(origin, avail[pkgn]['filename']), 'wb') as file:
                copyfileobj(content, file)
        
    except error.HTTPError as e:
        log('red', 'ERROR', f'returned status code {e}')
    except error.URLError as e:
        log('red', 'ERROR', f'failed to reach server; {e.reason}')
