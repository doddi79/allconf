import unittest

from alviss import quickloader
from ccptools.tpu.structs import empty
import os

import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class JsonTest(unittest.TestCase):
    def setUp(self) -> None:
        if 'ALVISS_FIDELIUS_MODE' in os.environ:
            del os.environ['ALVISS_FIDELIUS_MODE']
        self.global_config = quickloader.autoload(os.path.join(os.path.dirname(__file__), '../res/test_file.json'))

    def test_01_base_config(self):
        self.assertIsInstance(self.global_config, quickloader.BaseConfig)
        self.assertEqual(self.global_config.foo, 'I am foo')
        self.assertEqual(self.global_config.bar, 'This is bar')
        self.assertIs(self.global_config.moo, empty.Empty)
        self.assertIs(self.global_config.moo.shoo, empty.Empty)
        self.assertIs(self.global_config.moo.shoo or 'moo_shoo', 'moo_shoo')
        self.assertEqual(self.global_config.moo, empty.Empty)

    def test_03_reload(self):
        self.global_config.load(foo='No more Bar', moo={'shoo': 'moo_shoo'})
        self.assertIsInstance(self.global_config, quickloader.BaseConfig)
        self.assertEqual(self.global_config.foo, 'No more Bar')
        self.assertEqual(self.global_config.bar, empty.Empty)
        self.assertEqual(self.global_config.moo, {'shoo': 'moo_shoo'})
        self.assertIsInstance(self.global_config.moo, empty.EmptyDict)
        self.assertEqual(self.global_config.moo.kroo, empty.Empty)
        self.assertEqual(self.global_config.moo.shoo, 'moo_shoo')

    def test_05_set(self):
        cfg = self.global_config
        cfg.load(foo='No more Bar', moo={'shoo': 'moo_shoo'})
        self.assertIsInstance(cfg, quickloader.BaseConfig)

        self.assertEqual(cfg.foo, 'No more Bar')
        cfg.foo = 'Foo Again'
        self.assertEqual(cfg.foo, 'Foo Again')

        self.assertEqual(cfg.moo, {'shoo': 'moo_shoo'})
        self.assertIsInstance(cfg.moo, empty.EmptyDict)
        self.assertEqual(cfg.moo.kroo, empty.Empty)
        self.assertEqual(cfg.moo.shoo, 'moo_shoo')

    def test_06_reload(self):
        self.assertIsInstance(self.global_config, quickloader.BaseConfig)
        self.global_config.load(foo='No more Bar', moo={'shoo': 'moo_shoo'})
        self.global_config.foo = 'Foo Again'
        self.assertEqual(self.global_config.foo, 'Foo Again')

        self.assertEqual(self.global_config.moo, {'shoo': 'moo_shoo'})
        self.assertIsInstance(self.global_config.moo, empty.EmptyDict)
        self.assertEqual(self.global_config.moo.kroo, empty.Empty)
        self.assertEqual(self.global_config.moo.shoo, 'moo_shoo')

    def test_07_reload(self):
        self.global_config.load(foo='No more Bar', moo={'shoo': 'moo_shoo'})
        self.global_config.foo = 'Foo Again'
        self.global_config.update(foo='Foo Reset')
        self.assertIsInstance(self.global_config, quickloader.BaseConfig)

        self.assertEqual('Foo Reset', self.global_config.foo)

        self.assertEqual(self.global_config.moo, {'shoo': 'moo_shoo'})
        self.assertIsInstance(self.global_config.moo, empty.EmptyDict)
        self.assertEqual(self.global_config.moo.kroo, empty.Empty)
        self.assertEqual(self.global_config.moo.shoo, 'moo_shoo')

