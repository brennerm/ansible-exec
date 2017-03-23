import argparse
import enum
import distutils.spawn
import logging
import os
import sys
import tempfile

import yaml

logging.basicConfig()
_logger = logging.getLogger('ansible-runner')

LOG_LEVEL = {
    0: logging.ERROR,
    1: logging.WARN,
    2: logging.INFO
}


class RUNTYPE(enum.Enum):
    PLAYBOOK = 'playbook'
    ROLE = 'role'
    TASKS = 'tasks'


PLAYBOOK_ROLE_TEMPLATE = """
- hosts: {host}
  roles:
    - {role}
"""


PLAYBOOK_TASKS_TEMPLATE = """
- hosts: {host}
  tasks:
    - include: {tasks}
"""


def detect_run_type(path):
    if os.path.isdir(path):
        return RUNTYPE.ROLE

    with open(path, 'r') as f:
        playbook = yaml.safe_load(f)
    f.close()

    for el in playbook:
        if 'hosts' not in el:  # distinction of tasks vs playbook could be improved
            return RUNTYPE.TASKS

    return RUNTYPE.PLAYBOOK


def prepare_inventory_file(host):
    inventory_file = tempfile.NamedTemporaryFile()

    inventory_file.write(host)
    inventory_file.flush()

    return inventory_file


def prepare_role_playbook(host, path):
    return PLAYBOOK_ROLE_TEMPLATE.format(
        host=host,
        role=path
    )


def prepare_tasks_playbook(host, path):
    return PLAYBOOK_TASKS_TEMPLATE.format(
        host=host,
        tasks=path
    )


def main():
    argparser = argparse.ArgumentParser('Runs any kind of playbook, role or task list...\n')
    argparser.add_argument('host', help='Host to provision')
    argparser.add_argument('path', help='Path to playbook file, role directory or tasks file')
    argparser.add_argument('-v', '--verbose', action='count', default=0)
    argparser.usage = argparser.format_usage().rstrip().replace('usage: ', '') + ' -- [ansible-playbook args]'

    args, unknown = argparser.parse_known_args()

    _logger.setLevel(LOG_LEVEL.get(args.verbose, logging.DEBUG))

    playbook_bin_path = distutils.spawn.find_executable('ansible-playbook')
    if playbook_bin_path is None:
        raise EnvironmentError('Failed to find "ansible-playbook" executable')

    sys.argv[0] = playbook_bin_path  # fix script name to make ansible's command magic work

    if '--' in sys.argv:
        index = sys.argv.index('--')
        sys.argv[1:index+1] = []
    else:
        sys.argv[1:] = []

    if '-i' not in unknown and '--inventory' not in unknown:
        _logger.info('No inventory file given. Creating it...')
        inventory_file = prepare_inventory_file(args.host)
        sys.argv.extend(
            ['-i', inventory_file.name]
        )

    path = os.path.abspath(args.path)
    run_type = detect_run_type(path)
    _logger.info('Detected run type "%s"', run_type.value)

    if run_type == RUNTYPE.PLAYBOOK:
        playbook_path = path
    else:
        if run_type == RUNTYPE.ROLE:
            playbook_content = prepare_role_playbook(args.host, path)
        else:
            playbook_content = prepare_tasks_playbook(args.host, path)

        playbook_file = tempfile.NamedTemporaryFile()
        playbook_file.write(playbook_content)
        playbook_file.flush()
        playbook_path = playbook_file.name

    if _logger.getEffectiveLevel() == logging.DEBUG:
        with open(playbook_path, 'r') as f:
            _logger.debug('Playbook content: \n%s', f.read())

    sys.argv.append(playbook_path)
    _logger.debug('arguments for ansible-playbook: %s', str(sys.argv))

    execfile(playbook_bin_path)

if __name__ == '__main__':
    main()
