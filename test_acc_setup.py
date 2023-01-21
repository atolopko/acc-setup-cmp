from acc_setup import extract_path, build_diffs_by_tire_pos, parse_setup_params, AccSetup


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
            "carName": "mclaren_720s_gt3",
            "basicSetup":
                {
                    "tyres":
                        {
                            "tyreCompound": 0,
                            "tyrePressure": [56, 62, 58, 64]
                        },
                    "alignment":
                        {
                            "camber": [0, 0, 0, 0],
                            "toe": [38, 38, 25, 25],
                            "staticCamber": [-4.6132869720458984, -4.6103549003601074, -4.3367342948913574,
                                             -4.3318619728088379],
                            "toeOutLinear": [0.0015907743945717812, 0.0015907747438177466, 0.00050982175162062049,
                                             0.00050975591875612736],
                            "casterLF": 11,
                            "casterRF": 11,
                            "steerRatio": 2
                        },
                    "electronics":
                        {
                            "tC1": 3,
                            "tC2": 6,
                            "abs": 4,
                            "eCUMap": 0,
                            "fuelMix": 0,
                            "telemetryLaps": 0
                        },
                    "strategy":
                        {
                            "fuel": 20,
                            "nPitStops": 0,
                            "tyreSet": 0,
                            "frontBrakePadCompound": 0,
                            "rearBrakePadCompound": 0,
                            "pitStrategy": [
                                {
                                    "fuelToAdd": 0,
                                    "tyres":
                                        {
                                            "tyreCompound": 0,
                                            "tyrePressure": [52, 59, 52, 59]
                                        },
                                    "tyreSet": 2,
                                    "frontBrakePadCompound": 1,
                                    "rearBrakePadCompound": 1
                                }
                            ],
                            "fuelPerLap": 2.6084213256835938
                        }
                },
            "advancedSetup":
                {
                    "mechanicalBalance":
                        {
                            "aRBFront": 3,
                            "aRBRear": 2,
                            "wheelRate": [3, 3, 4, 4],
                            "bumpStopRateUp": [5, 5, 2, 2],
                            "bumpStopRateDn": [0, 0, 10, 10],
                            "bumpStopWindow": [4, 4, 50, 50],
                            "brakeTorque": 20,
                            "brakeBias": 57
                        },
                    "dampers":
                        {
                            "bumpSlow": [20, 20, 20, 20],
                            "bumpFast": [23, 23, 30, 30],
                            "reboundSlow": [8, 8, 22, 22],
                            "reboundFast": [20, 20, 27, 27]
                        },
                    "aeroBalance":
                        {
                            "rideHeight": [2, 6, 8, 18],
                            "rodLength": [58.382854461669922, 58.382854461669922, 37.532012939453125,
                                          37.532012939453125],
                            "splitter": 0,
                            "rearWing": 5,
                            "brakeDuct": [4, 3]
                        },
                    "drivetrain":
                        {
                            "preload": 5
                        }
                },
            "trackBopType": 28
        }

    setup = parse_setup_params(setup_params_raw)

    assert setup.to_dict()['value'] == \
           {'ABS': 4.0,
            'ARB F': 3.0,
            'ARB R': 2.0,
            'Brk Cmpnd F': 0.0,
            'Brk Cmpnd R': 0.0,
            'Brake Duct F': 3.0,
            'Brake Duct R': 5.0,
            'Break Bias': 57.0,
            'Break TQ': 20.0,
            'Bump Dn FL': 0.0,
            'Bump Dn FR': 0.0,
            'Bump Dn RL': 10.0,
            'Bump Dn RR': 10.0,
            'Bump Rng FL': 4.0,
            'Bump Rng FR': 4.0,
            'Bump Rng RL': 50.0,
            'Bump Rng RR': 50.0,
            'Bump Up FL': 5.0,
            'Bump Up FR': 5.0,
            'Bump Up RL': 2.0,
            'Bump Up RR': 2.0,
            'Camber FL': 0.0,
            'Camber FR': 0.0,
            'Camber RL': 0.0,
            'Camber RR': 0.0,
            'Caster L': 11.0,
            'Caster R': 11.0,
            'Dampers Bump Fast FL': 23.0,
            'Dampers Bump Fast FR': 23.0,
            'Dampers Bump Fast RL': 30.0,
            'Dampers Bump Fast RR': 30.0,
            'Dampers Bump Slow FL': 20.0,
            'Dampers Bump Slow FR': 20.0,
            'Dampers Bump Slow RL': 20.0,
            'Dampers Bump Slow RR': 20.0,
            'Dampers Rebound Fast FL': 23.0,
            'Dampers Rebound Fast FR': 23.0,
            'Dampers Rebound Fast RL': 30.0,
            'Dampers Rebound Fast RR': 30.0,
            'Dampers Rebound Slow FL': 20.0,
            'Dampers Rebound Slow FR': 20.0,
            'Dampers Rebound Slow RL': 20.0,
            'Dampers Rebound Slow RR': 20.0,
            'Eng Map': 0.0,
            'F Splitter': 0.0,
            'Fuel': 20.0,
            'PSI FL': 56.0,
            'PSI FR': 62.0,
            'PSI RL': 58.0,
            'PSI RR': 64.0,
            'R Wing': 5.0,
            'Ride Height F': 37.532012939453125,
            'Ride Height R': 58.38285446166992,
            'Spring Rate FL': 3.0,
            'Spring Rate FR': 3.0,
            'Spring Rate RL': 4.0,
            'Spring Rate RR': 4.0,
            'Steer Ratio': 2.0,
            'TC 1': 3.0,
            'TC 2': 6.0,
            'Toe FL': 38.0,
            'Toe FR': 38.0,
            'Toe RL': 25.0,
            'Toe RR': 25.0}
