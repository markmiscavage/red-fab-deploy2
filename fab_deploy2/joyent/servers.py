from fabric.api import run, sudo
from fabric.contrib.files import append

from fab_deploy2.base import servers as base_servers


class JoyentMixin(object):

    def _set_profile(self):
        append('/etc/profile', 'CC="gcc -m64"; export CC', use_sudo=True)
        append('/etc/profile', 'LDSHARED="gcc -m64 -G"; export LDSHARED', use_sudo=True)

    def _ssh_restart(self):
        run('svcadm restart ssh')

class AppMixin(JoyentMixin):
    packages = ['gcc47', 'py27-psycopg2', 'py27-setuptools',
                'py27-imaging', 'py27-expat']

    def _set_profile(self):
        JoyentMixin._set_profile(self)
        base_servers.AppServer._set_profile(self)

    def _install_packages(self):
        for package in self.packages:
            sudo('pkg_add %s' % package)
        sudo('easy_install-2.7 pip')


class LBServer(JoyentMixin,  base_servers.LBServer):
    pass

class AppServer(AppMixin,  base_servers.AppServer):
    pass

class DBServer(JoyentMixin,  base_servers.DBServer):
    pass

class DBSlaveServer(JoyentMixin,  base_servers.DBSlaveServer):
    pass

class DevServer(AppMixin,  base_servers.DevServer):
    pass

AppServer().as_tasks(name="app_server")
LBServer().as_tasks(name="lb_server")
DevServer().as_tasks(name="dev_server")
DBServer().as_tasks(name="db_server")
DBSlaveServer().as_tasks(name="db_slave_server")
