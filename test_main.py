import numpy as np
import pandas as pd
from numpy import nan

from main import extract_path, build_diffs_by_tire_pos, parse_setup_params, AccSetup, \
    compare_setups


def test_extract_path():
    assert extract_path({'a': {'b': 1.0}}, 'a', 'b') == 1.0


def test_build_diffs_by_tire_pos():
    result = build_diffs_by_tire_pos("setup_param_name", [0.0, 1.0, 2.0, 3.0])

    assert result == {'setup_param_name FL': 0.0,
                      'setup_param_name FR': 1.0,
                      'setup_param_name RL': 2.0,
                      'setup_param_name RR': 3.0}


def test_parse_setup():
    setup_params_raw = \
        {
            "carName": "mclaren_720.0s_gt3.0",
            "basicSetup": {
                    "tyres": {
                            "tyreCompound": 0.0,
                            "tyrePressure": [50.0, 57.0, 47.0, 57.0]
                        },
                    "alignment": {
                            "camber": [0.0, 0.0, 0.0, 0.0],
                            "toe": [36.0, 36.0, 20.0, 20.0],
                        }
                },
            "advancedSetup": {
                    "mechanicalBalance": {
                            "aRBFront": 4.0,
                            "aRBRear": 6.0,
                            "wheelRate": [3.0, 3.0, 5.0, 5.0],
                            "bumpStopRateUp": [5.0, 5.0, 2.0, 2.0],
                            "bumpStopRateDn": [0.0, 0.0, 10.0, 10.0],
                            "bumpStopWindow": [3.0, 3.0, 25.0, 25.0],
                            "brakeTorque": 20.0,
                            "brakeBias": 35.0
                        }
            }
        }

    setup = parse_setup_params(setup_params_raw)

    assert setup.to_dict()['values'] == \
           {'psi FL': 50.0,
            'psi FR': 57.0,
            'psi RL': 47.0,
            'psi RR': 57.0,
            'toe FL': 36.0,
            'toe FR': 36.0,
            'toe RL': 20.0,
            'toe RR': 20.0,
            'ARB F': 4.0,
            'ARB R': 6.0,
            'Break Bias': 35.0,
            'Break TQ': 20.0,
            'bumpDn FL': 0.0,
            'bumpDn FR': 0.0,
            'bumpDn RL': 10.0,
            'bumpDn RR': 10.0,
            'bumpRng FL': 3.0,
            'bumpRng FR': 3.0,
            'bumpRng RL': 25.0,
            'bumpRng RR': 25.0,
            'bumpUp FL': 5.0,
            'bumpUp FR': 5.0,
            'bumpUp RL': 2.0,
            'bumpUp RR': 2.0,
            'wheelRate FL': 3.0,
            'wheelRate FR': 3.0,
            'wheelRate RL': 5.0,
            'wheelRate RR': 5.0,
            }


def test_compare_setup_params():
    setup_a = AccSetup('a', parse_setup_params({"basicSetup": {"tyres": {"tyrePressure": [50.0, 57.0, 47.0, 57.0]}}}))
    setup_b = AccSetup('b', parse_setup_params({"basicSetup": {"tyres": {"tyrePressure": [51.0, 58.0, 48.0, 58.0]}}}))

    result = compare_setups(setup_a, setup_b)

    assert result.fillna(-1).to_dict(orient='index') == \
           {
               'psi FL': {'a': 50.0, 'b': 51.0, 'delta': 1.0},
               'psi FR': {'a': 57.0, 'b': 58.0, 'delta': 1.0},
               'psi RL': {'a': 47.0, 'b': 48.0, 'delta': 1.0},
               'psi RR': {'a': 57.0, 'b': 58.0, 'delta': 1.0},
               'ARB F': {'a': -1, 'b': -1, 'delta': -1},
               'ARB R': {'a': -1, 'b': -1, 'delta': -1},
               'Break TQ': {'a': -1, 'b': -1, 'delta': -1},
               'Break Bias': {'a': -1, 'b': -1, 'delta': -1}
           }

