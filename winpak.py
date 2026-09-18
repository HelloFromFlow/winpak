from sys import argv as sys_argv
from pathlib import Path
from os import chdir, getcwd

org = getcwd()

chdir(Path(__file__).resolve().parent)

import modules.deploy as deploy
import modules.build as build
from modules.lib import log

import modules.host as host
import modules.install as install
import modules.updateManifest as updMan

flag_map = {
    'deploy': deploy.main,
    'build': build.main,
    'host': host.main,
    'install': install.main,
    'updMan': updMan.main
}

if len(sys_argv) < 2:
    log('red', 'ERROR', 'usage: python winpak.py [flag] ...')
    exit(1)

if sys_argv[1] not in flag_map:
    log('red', 'ERROR', f'no such flag: "{sys_argv[1]}"')
    exit(1)

flag = sys_argv.pop(1)

sys_argv = sys_argv[1:]

flag_map[flag](sys_argv, org)