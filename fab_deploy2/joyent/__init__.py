import utils
import servers
import gunicorn
import nginx
import postgres
import firewall
import api
import snmp
import celery
import redis
import python
import haproxy

from fabric.api import env

env.platform = 'joyent'
