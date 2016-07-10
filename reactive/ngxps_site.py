import os

from shutil import rmtree

from charmhelpers.core import hookenv
from charmhelpers.core.hookenv import status_set
from charmhelpers.fetch.archiveurl import ArchiveUrlFetchHandler

from charms.reactive import when
from charms.reactive.helpers import data_changed

config = hookenv.config()


@when('web-engine.available', 'vhost.valid')
def install_site(engine):
    if not data_changed('config', config):
        return

    site_path = os.path.join('/usr/local/nginx/html', hookenv.service_name())
    rmtree(site_path)

    handler = ArchiveUrlFetchHandler()
    handler.install(config['default_site'], site_path)

    root = os.path.join(site_path, config['root'])

    engine.configure(root=root,
                     listen=config['listen'],
                     server_name=config['server_name'],
                     RewriteLevel=config['RewriteLevel'],
                     EnableFilters=config['EnableFilters'],
                     LearningMode=config['LearningMode'])

    status_set('active', '{} running'.format(config['default_site']))
