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


class TestParsing(unittest.TestCase):
    def setUp(self):
        os.environ['OS_MOCK'] = 'MockDos'
        if 'ALVISS_FIDELIUS_MODE' in os.environ:
            del os.environ['ALVISS_FIDELIUS_MODE']

    def test_yaml_parsing(self):
        config = quickloader.autoload(os.path.join(_HERE, '../res/rendering/yaml/no_fidelius.yaml'))

        with open(os.path.join(_HERE, '../res/rendering/expected.yaml'), 'r') as fin:
            expected_data = yaml.safe_load(fin)

        self.assertIsInstance(config, quickloader.BaseConfig)

        self.assertEqual(expected_data, config.as_dict(unmaksed=True))

        from tests.res.rendering.expected import EXPECTED_DICT
        self.assertEqual(EXPECTED_DICT, config.as_dict(unmaksed=True))

        self.assertEqual(config.foo, 'I am foo')
        self.assertEqual(config.bar, 'This is bar')
        self.assertIs(config.moo, Empty)
        self.assertIs(config.moo.shoo, Empty)
        self.assertIs(config.moo.shoo or 'moo_shoo', 'moo_shoo')
        self.assertEqual(config.moo, Empty)

    def test_json_parsing(self):
        config = quickloader.autoload(os.path.join(_HERE, '../res/rendering/json/no_fidelius.json'))

        with open(os.path.join(_HERE, '../res/rendering/expected.json'), 'r') as fin:
            expected_data = json.load(fin)

        self.assertIsInstance(config, quickloader.BaseConfig)

        self.assertEqual(expected_data, config.as_dict(unmaksed=True))

        from tests.res.rendering.expected import EXPECTED_DICT
        self.assertEqual(EXPECTED_DICT, config.as_dict(unmaksed=True))
