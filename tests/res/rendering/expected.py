EXPECTED_DICT = {
    'import_test': {
        'generic': 'Overridden',
        'because': "that's cool",
        'imported_key': {
            'import1': 'one',
            'import2': 'Tveir',
            'import3': 'three',
            'included_env_stuff': 'MockDos'
        }
    },
    'group': {
        'beta': 'B',
        'delta': 'NewDeltaRocks!',
        'gamma_with_var': 'Foo:I am foo',
        'alpha': 'AAAAA!'
    },
    'foo': 'I am foo',
    'internal_ref': {
        'deeper': {
            'there': 'Something',
            'everywhere': 'My heart will go on!'
        }
    },
    'base_key': 'is basic',
    'foo_inherited': 'Should be static!',
    'bar': 'This is bar',
    'my_list': [
        'one',
        'two',
        'three',
        'I am foo',
        'This is B group',
        'No ${var}',
        '${__ENV__:I_DONT_WANT_THIS_GUY_TO_RESOLVE_TO_ANYTHING}'
    ],
    'an_integer': 7,
    'a_float': 3.5,
    'a_bool': True,
    'a_false_bool': False,
    'a_none': None,
    'a_zero': 0,
    'a_default_env': "I'm a default value!",
    'an_empty': '',
    'should_be_seven': 7,
    'new_delta': 'NewDeltaRocks!',
    'env_stuff': 'MockDos',
    'collapsed': {
        'group': {
            'in': {
                'one': {
                    'string': 'Yes!'
                }
            },
            'successful': True
        }
    },
    'another_integer': 42
}
