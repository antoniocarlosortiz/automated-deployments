# prod/fabfile.py
import os
from fabric.contrib.files import sed
from fabric.api import env, local, run

# initialize the base directory
abs_dir_path = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))


# declare environment global variables

# root user
env.user = 'root'

# list of remote IP addresses
env.hosts = ['<123.456.789.10>']

# user group
env.user_group = 'deployers'

# user for the above group
env.user_name = 'deployer'

# ssh key path
env.ssh_keys_dir = os.path.join(abs_dir_path, 'ssh-keys')


def start_provision():
    """
    Start server provisioning
    """
    # Create a new directory for a new remote server
    env.ssh_keys_name = os.path.join(env.ssh_keys_dir, 'prod_key')
    local('ssh-keygen -t rsa -b 2048 -f {0}'.format(env.ssh_keys_name))
    local('cp {0} {1}/authorized_keys'.format(
        env.ssh_keys_name + '.pub', env.ssh_keys_dir))
    # Prevent root SSHing into the remote server
    sed('/etc/ssh/sshd_config', '^UsePAM yes', 'UsePAM no')
    sed('/etc/ssh/sshd_config', '^PermitRootLogin yes',
        'PermitRootLogin no')
    sed('/etc/ssh/sshd_config', '^#PasswordAuthentication yes',
        'PasswordAuthentication no')
    sed('/etc/ssh/sshd_config', '^PasswordAuthentication yes',
        'PasswordAuthentication no')

    create_deployer_group()
    create_deployer_user()
    upload_keys()
    run('service sshd reload')
    # update_locales()
    upgrade_server()


def create_deployer_group():
    """
    Create a user group for all project developers
    """
    run('groupadd {}'.format(env.user_group))
    run('mv /etc/sudoers /etc/sudoers-backup')
    run('(cat /etc/sudoers-backup; echo "%' +
        env.user_group + ' ALL=(ALL) ALL") > /etc/sudoers')
    run('chmod 440 /etc/sudoers')


def create_deployer_user():
    """
    Create a user for the user group
    """

    # TODO: use useradd instead of adduser so password and other details can
    # be added with just one command.
    run('adduser {}'.format(env.user_name))
    run('usermod -a -G {} {}'.format(env.user_group, env.user_name))
    run('mkdir /home/{}/.ssh'.format(env.user_name))
    run('chown -R {} /home/{}/.ssh'.format(env.user_name, env.user_name))
    run('chgrp -R {} /home/{}/.ssh'.format(
        env.user_group, env.user_name))


def upload_keys():
    """
    Upload the SSH public/private keys to the remote server via scp
    """
    scp_command = 'scp {} {}/authorized_keys {}@{}:~/.ssh'.format(
        env.ssh_keys_name + '.pub',
        env.ssh_keys_dir,
        env.user_name,
        env.host_string
    )
    local(scp_command)


# TODO: currently not work. fix issue in the future.
def update_locales():
    run(("export LANGUAGE=en_US.UTF-8; export LANG=en_US.UTF-8;"
         " export LC_ALL=en_US.UTF-8; locale-gen en_US.UTF-8"))


def upgrade_server():
    """
    Upgrade the server as a root user
    """
    run('apt-get update && apt-get -y upgrade')

    # because ubuntu 16.04 no longer has python2.7
    run('sudo apt-get -y install python-simplejson')
    run('sudo reboot')
