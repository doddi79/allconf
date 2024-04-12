import os
import unittest

from alviss import quickloader
import yaml
import json

import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

_HERE = os.path.dirname(__file__)


class TestRendering(unittest.TestCase):
    def setUp(self):
        os.environ['OS_MOCK'] = 'MockDos'
        if 'ALVISS_FIDELIUS_MODE' in os.environ:
            del os.environ['ALVISS_FIDELIUS_MODE']

    def test_yaml_rendering(self):
        composite_yaml = quickloader.render_load(os.path.join(_HERE, '../res/rendering/yaml/no_fidelius.yaml'),
                                                 skip_env_loading=False,
                                                 skip_fidelius=False)
        composite_data = yaml.safe_load(composite_yaml)

        with open(os.path.join(_HERE, '../res/rendering/expected.yaml'), 'r') as fin:
            expected_data = yaml.safe_load(fin)

        self.assertEqual(expected_data, composite_data)

        from tests.res.rendering.expected import EXPECTED_DICT
        self.assertEqual(EXPECTED_DICT, composite_data)

    def test_json_rendering(self):
        composite_json = quickloader.render_load(os.path.join(_HERE, '../res/rendering/json/no_fidelius.json'),
                                                 skip_env_loading=False,
                                                 skip_fidelius=False)
        composite_data = json.loads(composite_json)

        with open(os.path.join(_HERE, '../res/rendering/expected.json'), 'r') as fin:
            expected_data = json.load(fin)

        self.assertEqual(expected_data, composite_data)

        from tests.res.rendering.expected import EXPECTED_DICT
        self.assertEqual(EXPECTED_DICT, composite_data)
