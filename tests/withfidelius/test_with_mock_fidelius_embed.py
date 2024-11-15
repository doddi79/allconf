import os
import unittest

from allconf import quickloader
import yaml
import json
from batutils.structs import Empty

import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

_HERE = os.path.dirname(__file__)


class TestParsingWithMockFideliusEmbedded(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['OS_MOCK'] = 'MockDos'
        if 'ALVISS_FIDELIUS_MODE' in os.environ:
            del os.environ['ALVISS_FIDELIUS_MODE']

        have_fidelius = False
        try:
            import fidelius
            have_fidelius = True
        except ImportError:
            pass

        if not have_fidelius:
            raise unittest.SkipTest('Fidelius is not installed but should be for these tests')

        from fidelius.fideliusapi import FideliusAppProps
        from fidelius.fideliusapi import FideliusFactory
        fia = FideliusFactory.get_admin_class('mock')(FideliusAppProps(app='my-mock-app', group='pretenders', env='unittest'))
        fia._cache.clear()  # noqa
        fia.create_param('DATABASE_USERNAME', 'myusername')
        fia.create_shared_param('DATABASE_SERVER', 'myfolder', 'myserver')
        fia.create_secret('DATABASE_PASSWORD', 'somepassword')

    @classmethod
    def tearDownClass(cls):
        from fidelius.fideliusapi import FideliusAppProps
        from fidelius.fideliusapi import FideliusFactory
        fia = FideliusFactory.get_admin_class('mock')(FideliusAppProps(app='my-mock-app', group='pretenders', env='unittest'))
        fia._cache.clear()  # noqa

    def test_yaml_parsing_with_mock_fidelius(self):
        config = quickloader.autoload(os.path.join(_HERE, '../res/rendering/yaml/with_fidelius_mode_embed.yaml'))
        self.assertIsInstance(config, quickloader.BaseConfig)
        self.assertEqual(config.database.server, 'myserver')
        self.assertEqual(config.database.username, 'myusername')
        self.assertEqual(config.database.password, 'somepassword')

    def test_json_parsing_with_mock_fidelius(self):
        config = quickloader.autoload(os.path.join(_HERE, '../res/rendering/json/with_fidelius_mode_embed.json'))
        self.assertIsInstance(config, quickloader.BaseConfig)
        self.assertEqual(config.database.server, 'myserver')
        self.assertEqual(config.database.username, 'myusername')
        self.assertEqual(config.database.password, 'somepassword')
