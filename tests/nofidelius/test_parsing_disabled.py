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


class TestParsingWithFideliusDisabled(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['OS_MOCK'] = 'MockDos'
        os.environ['ALVISS_FIDELIUS_MODE'] = 'DISABLED'
        have_fidelius = False
        try:
            import fidelius
            have_fidelius = True
        except ImportError:
            pass

        if have_fidelius:
            raise unittest.SkipTest('Fidelius is installed but should not be for these tests')

    def test_yaml_parsing_with_fidelius_disabled(self):
        config = quickloader.autoload(os.path.join(_HERE, '../res/rendering/yaml/with_fidelius.yaml'))
        self.assertIsInstance(config, quickloader.BaseConfig)
        self.assertEqual('${__FID__:myfolder:DATABASE_SERVER}', config.database.server)
        self.assertEqual('${__FID__:DATABASE_USERNAME}', config.database.username)
        self.assertEqual('${__FID__:DATABASE_PASSWORD}', config.database.password)

    def test_json_parsing_with_fidelius_disabled(self):
        config = quickloader.autoload(os.path.join(_HERE, '../res/rendering/json/with_fidelius.json'))
        self.assertIsInstance(config, quickloader.BaseConfig)
        self.assertEqual('${__FID__:myfolder:DATABASE_SERVER}', config.database.server)
        self.assertEqual('${__FID__:DATABASE_USERNAME}', config.database.username)
        self.assertEqual('${__FID__:DATABASE_PASSWORD}', config.database.password)
