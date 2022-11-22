from main import extract_path, build_diffs_by_tire_pos, parse_setup_params, compare_setup_params, AccSetup, \
    compare_setups


def test_extract_path():
    assert extract_path({'a': {'b': 1}}, 'a', 'b') == 1


def test_build_diffs_by_tire_pos():
    result = build_diffs_by_tire_pos("setup_param_name", [0, 1, 2, 3])

    assert result == {'setup_param_name FL': 0,
                      'setup_param_name FR': 1,
                      'setup_param_name RL': 2,
                      'setup_param_name RR': 3}


def test_parse_setup():
    setup_params_raw = \
        {
            "carName": "mclaren_720s_gt3",
            "basicSetup": {
                    "tyres": {
                            "tyreCompound": 0,
                            "tyrePressure": [50, 57, 47, 57]
                        },
                    "alignment": {
                            "camber": [0, 0, 0, 0],
                            "toe": [36, 36, 20, 20],
                        }
                },
            "advancedSetup": {
                    "mechanicalBalance": {
                            "aRBFront": 4,
                            "aRBRear": 6,
                            "wheelRate": [3, 3, 5, 5],
                            "bumpStopRateUp": [5, 5, 2, 2],
                            "bumpStopRateDn": [0, 0, 10, 10],
                            "bumpStopWindow": [3, 3, 25, 25],
                            "brakeTorque": 20,
                            "brakeBias": 35
                        }
            }
        }

    setup = parse_setup_params(setup_params_raw)

    assert setup.to_dict()['values'] == \
           {'psi FL': 50,
            'psi FR': 57,
            'psi RL': 47,
            'psi RR': 57,
            'toe FL': 36,
            'toe FR': 36,
            'toe RL': 20,
            'toe RR': 20,
            'ARB F': 4,
            'ARB R': 6,
            'Break Bias': 35,
            'Break TQ': 20,
            'bumpDn FL': 0,
            'bumpDn FR': 0,
            'bumpDn RL': 10,
            'bumpDn RR': 10,
            'bumpRng FL': 3,
            'bumpRng FR': 3,
            'bumpRng RL': 25,
            'bumpRng RR': 25,
            'bumpUp FL': 5,
            'bumpUp FR': 5,
            'bumpUp RL': 2,
            'bumpUp RR': 2,
            'wheelRate FL': 3,
            'wheelRate FR': 3,
            'wheelRate RL': 5,
            'wheelRate RR': 5,
            }


def test_compare_setup_params():
    setup_a = AccSetup('a', parse_setup_params({"basicSetup": {"tyres": {"tyrePressure": [50, 57, 47, 57]}}}))
    setup_b = AccSetup('b', parse_setup_params({"basicSetup": {"tyres": {"tyrePressure": [51, 58, 48, 58]}}}))

    result = compare_setups(setup_a, setup_b)

    assert result.to_dict(orient='index') == \
           {'psi FL': {'a': 50, 'b': 51},
            'psi FR': {'a': 57, 'b': 58},
            'psi RL': {'a': 47, 'b': 48},
            'psi RR': {'a': 57, 'b': 58}}

