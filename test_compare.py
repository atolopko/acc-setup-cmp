from acc_setup import AccSetup, parse_setup_params
from compare import compare_setups


def test_compare_setup_params():
    setup_a = AccSetup('a', parse_setup_params({"basicSetup": {"tyres": {"tyrePressure": [50.0, 57.0, 47.0, 57.0]}}}))
    setup_b = AccSetup('b', parse_setup_params({"basicSetup": {"tyres": {"tyrePressure": [51.0, 58.0, 48.0, 58.0]}}}))

    result = compare_setups(setup_a, setup_b)

    assert result.dropna().to_dict(orient='index') == \
           {'PSI FL': {('a', 'value'): 50.0, ('b', 'delta'): 1.0, ('b', 'value'): 51.0},
            'PSI FR': {('a', 'value'): 57.0, ('b', 'delta'): 1.0, ('b', 'value'): 58.0},
            'PSI RL': {('a', 'value'): 47.0, ('b', 'delta'): 1.0, ('b', 'value'): 48.0},
            'PSI RR': {('a', 'value'): 57.0, ('b', 'delta'): 1.0, ('b', 'value'): 58.0}}
