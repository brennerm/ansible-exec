from distutils.core import setup

setup(
    name='ansible-exec',
    scripts=['ansible-exec'],
    install_requires=['enum34', 'pyaml'],
    version='1.3',
    description='Runs your playbooks, roles and tasks',
    author='Max Brenner',
    author_email='xamrennerb@gmail.com',
    url='https://github.com/brennerm/ansible-exec',
    download_url='https://github.com/brennerm/ansible-exec/archive/1.3.tar.gz',
    keywords=['ansible', 'playbook', 'role', 'task']
)
