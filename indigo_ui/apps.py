""""Indigo UI apps

Copyright 2015 Archive Analytics Solutions

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from django.apps import AppConfig
from indigo import get_config
import logging


class IndigoAppConfig(AppConfig):
    name = 'indigo_ui'
    verbose_name = "Indigo"

    def ready(self):
        from indigo.models import initialise, Collection, User, Group
        
        
        logging.basicConfig(level=logging.WARNING)
        logging.getLogger("models").setLevel(logging.WARNING)
        logging.getLogger("dse.policies").setLevel(logging.WARNING)
        logging.getLogger("dse.cluster").setLevel(logging.WARNING)
        logging.getLogger("dse.cqlengine.management").setLevel(logging.WARNING)

        cfg = get_config(None)
        initialise(keyspace=cfg.get('KEYSPACE', 'indigo'),
                   hosts=cfg.get('CASSANDRA_HOSTS', ('127.0.0.1', )))

        # Try to get the root. It will create it if it doesn't exist
        root = Collection.get_root()
        
        # TODO: Review that at some point
        # Check that the graph vertices for users are still there
        User.check_graph_users()


