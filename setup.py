from distutils.core import setup

setup(
    name='ansible-runner',
    scripts=['ansible-runner'],
    install_requires=['enum34', 'pyaml'],
    version='1.3',
    description='Runs your playbooks, roles and tasks',
    author='Max Brenner',
    author_email='xamrennerb@gmail.com',
    url='https://github.com/brennerm/ansible-runner',
    download_url='https://github.com/brennerm/ansible-runner/archive/1.3.tar.gz',
    keywords=['ansible', 'playbook', 'role', 'task']
)
