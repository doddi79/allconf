import os
import unittest

from allconf import quickloader
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
        if 'PRETEND_API_KEY' in os.environ:
            del os.environ['PRETEND_API_KEY']

    def test_yaml_required_should_fail(self):
        if 'PRETEND_API_KEY' in os.environ:
            del os.environ['PRETEND_API_KEY']
        with self.assertRaises(ValueError):
            quickloader.autoload(os.path.join(_HERE, '../res/rendering/yaml/required_env.yaml'))

    def test_json_required_should_fail(self):
        if 'PRETEND_API_KEY' in os.environ:
            del os.environ['PRETEND_API_KEY']
        with self.assertRaises(ValueError):
            quickloader.autoload(os.path.join(_HERE, '../res/rendering/json/required_env.json'))

    def test_yaml_required_env(self):
        os.environ['PRETEND_API_KEY'] = 'veryimportantvalue'

        cfg = quickloader.autoload(os.path.join(_HERE, '../res/rendering/yaml/required_env.yaml'))

        self.assertEqual('veryimportantvalue', cfg.required_key)

        with open(os.path.join(_HERE, '../res/rendering/expected_required.yaml'), 'r') as fin:
            expected_data = yaml.safe_load(fin)

        self.assertEqual(expected_data, cfg.as_dict(unmaksed=True))

        if 'PRETEND_API_KEY' in os.environ:
            del os.environ['PRETEND_API_KEY']

    def test_json_required_env(self):
        os.environ['PRETEND_API_KEY'] = 'veryimportantvalue'

        cfg = quickloader.autoload(os.path.join(_HERE, '../res/rendering/json/required_env.json'))

        self.assertEqual('veryimportantvalue', cfg.required_key)

        with open(os.path.join(_HERE, '../res/rendering/expected_required.json'), 'r') as fin:
            expected_data = json.load(fin)

        self.assertEqual(expected_data, cfg.as_dict(unmaksed=True))

        if 'PRETEND_API_KEY' in os.environ:
            del os.environ['PRETEND_API_KEY']
