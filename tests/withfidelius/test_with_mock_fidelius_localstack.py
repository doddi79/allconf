import os
import unittest

from alviss import quickloader
from typing import *

import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

_HERE = os.path.dirname(__file__)


def _extract_param_names(response: Dict) -> List[str]:
    return [p.get('Name') for p in response.get('Parameters', [])]


def _get_param_names_by_path(ssm, path: str) -> List[str]:
    return _extract_param_names(ssm.get_parameters_by_path(Path=path,
                                                           Recursive=True,
                                                           WithDecryption=False))


def _delete_all_params(ssm):
    paths = [
        '/fidelius/tempunittestgroup/',
    ]
    param_set = set()
    for p in paths:
        param_set.update(_get_param_names_by_path(ssm, p))

    if param_set:
        res = ssm.delete_parameters(Names=list(param_set))
        log.debug('_delete_all_params -> %s', res)


class TestParsingWithMockFideliusLocalstack(unittest.TestCase):
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

        fia = FideliusFactory.get_admin_class('paramstore')(
            FideliusAppProps(app='my-mock-app', group='tempunittestgroup', env='unittest'),
            aws_access_key_id='somemadeupstuff',
            aws_secret_access_key='notarealkey',
            aws_key_arn='arn:aws:kms:eu-west-1:123456789012:alias/fidelius-key',
            aws_region_name='eu-west-1',
            aws_endpoint_url='http://localhost:4566',
            flush_cache_every_time=True)

        _delete_all_params(fia._ssm)  # noqa

        fia.create_param('DATABASE_USERNAME', 'myusername')
        fia.create_shared_param('DATABASE_SERVER', 'myfolder', 'myserver')
        fia.create_secret('DATABASE_PASSWORD', 'somepassword')

    @classmethod
    def tearDownClass(cls):
        from fidelius.fideliusapi import FideliusAppProps
        from fidelius.fideliusapi import FideliusFactory

        fia = FideliusFactory.get_admin_class('paramstore')(
            FideliusAppProps(app='my-mock-app', group='tempunittestgroup', env='unittest'),
            aws_access_key_id='somemadeupstuff',
            aws_secret_access_key='notarealkey',
            aws_key_arn='arn:aws:kms:eu-west-1:123456789012:alias/fidelius-key',
            aws_region_name='eu-west-1',
            aws_endpoint_url='http://localhost:4566',
            flush_cache_every_time=True)

        _delete_all_params(fia._ssm)  # noqa

    def test_yaml_parsing_with_mock_fidelius(self):
        config = quickloader.autoload(os.path.join(_HERE, '../res/rendering/yaml/with_fidelius_localstack.yaml'))
        self.assertIsInstance(config, quickloader.BaseConfig)
        self.assertEqual(config.database.server, 'myserver')
        self.assertEqual(config.database.username, 'myusername')
        self.assertEqual(config.database.password, 'somepassword')

    def test_json_parsing_with_mock_fidelius(self):
        config = quickloader.autoload(os.path.join(_HERE, '../res/rendering/json/with_fidelius_localstack.json'))
        self.assertIsInstance(config, quickloader.BaseConfig)
        self.assertEqual(config.database.server, 'myserver')
        self.assertEqual(config.database.username, 'myusername')
        self.assertEqual(config.database.password, 'somepassword')
