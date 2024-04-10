import os
import unittest

from alviss import quickloader
import yaml
import json
from ccptools.structs import Empty

import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

_HERE = os.path.dirname(__file__)


class TestParsingWithFideliusSubstitute(unittest.TestCase):
    def setUp(self):
        os.environ['OS_MOCK'] = 'MockDos'
        os.environ['ALVISS_FIDELIUS_MODE'] = 'SUBSTITUTE_ENV'

        os.environ['mygroup__DATABASE_SERVER'] = 'myserver'
        os.environ['DATABASE_USERNAME'] = 'myusername'
        os.environ['DATABASE_PASSWORD'] = 'somepassword'

    def test_yaml_parsing_with_fidelius_substitute(self):
        config = quickloader.autoload(os.path.join(_HERE, '../res/rendering/yaml/with_fidelius.yaml'))
        self.assertIsInstance(config, quickloader.BaseConfig)
        self.assertEqual(config.database.server, 'myserver')
        self.assertEqual(config.database.username, 'myusername')
        self.assertEqual(config.database.password, 'somepassword')

    def test_json_parsing_with_fidelius_substitute(self):
        config = quickloader.autoload(os.path.join(_HERE, '../res/rendering/json/with_fidelius.json'))
        self.assertIsInstance(config, quickloader.BaseConfig)
        self.assertEqual(config.database.server, 'myserver')
        self.assertEqual(config.database.username, 'myusername')
        self.assertEqual(config.database.password, 'somepassword')
