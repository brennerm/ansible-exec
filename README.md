# ansible-exec [![Build Status](https://travis-ci.org/brennerm/ansible-exec.svg?branch=master)](https://travis-ci.org/brennerm/ansible-exec)
Runs your playbooks, roles and tasks

## Installation
- From source code
```
git clone https://github.com/brennerm/ansible-exec
cd ansible-exec
python setup.py install
```

- With pip
```
pip install ansible-exec
```

## Usage
### Playbook
```
# playbook.yml
---
- hosts: all
  tasks:
    - name: Install apache2
      apt:
        name: apache2
        state: present
        
$ ansible-exec webserver.example.com playbook.yml -- -u root -k
```

### Role
```
- apache2_install/
                  tasks/
                        main.yml
                  defaults/
                        main.yml
                  README
                        
# tasks/main.yml
---
- name: Install apache2
  apt:
    name: apache2
    state: present
        
$ ansible-exec webserver.example.com apache2_install/ -- -u root -k
```

### Tasks
```
# tasks.yml
---
- name: Install apache2
  apt:
    name: apache2
    state: present
        
$ ansible-exec webserver.example.com tasks.yml -- -u root -k
```
