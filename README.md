Automating Django Deployments With Fabric and Ansible
=====================================================
Fork of [realpython/automated-deployments](realpython/automated-deployments)

The automation process comes in two parts; the first one being the initial server setup using fabric and the next one, the deployment of a specified django project within the remote server

Usage
-----
1. update ip address in `env.hosts` in `prod/fabfile.py`
2. run `fab -f ./prod/fabfile.py start_provision`
3. fill up empty field in `group_vars/all.template` and `create a group_vars/all` file from it
4. run deploy_prod.sh

Access the server
-----------------
inside the project folder: `ssh -i ./ssh-keys/prod_key deployer@<ip address of server or whatever the name is in the config>`

Things to do
------------
- [x] adjust to work on ubuntu 16.04
- [x] remove use of virtualenv
- [x] create systemd script for Gunicorn
- [x] Move NGINX config from conf.d to sites-available
- [x] Create a more detailed README.md
- [ ] Update fabric to automatically set the new password of a remote server
- [ ] Update fabric to fix language not found bug on initial servers
