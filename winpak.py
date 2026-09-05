from sys import argv as sys_argv
from pathlib import Path
from os import chdir

chdir(Path(__file__).resolve().parent)

import modules.deploy as deploy
import modules.build as build
from modules.lib import log

import modules.server as server
import modules.install as install
import modules.updateManifest as updMan


flag_map = {
    '-d': deploy.main,
    '-b': build.main,
    '-s': server.main,
    '-i': install.main,
    '-u': updMan.main
}

if len(sys_argv) < 3:
    log('red', 'ERROR', 'usage: python winpak.py [flag] [file/dir-name]')
    exit(1)

if sys_argv[1] not in flag_map:
    log('red', 'ERROR', f'no such flag: "{sys_argv[1]}"')
    exit(1)

flag = sys_argv.pop(1)

flag_map[flag](sys_argv)