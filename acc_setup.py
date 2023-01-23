import dataclasses
import json
from typing import List, Dict

import numpy as np
import pandas as pd
from pandas import DataFrame

tire_pos_labels = ['FL', 'FR', 'RL', 'RR']
FL = 0
FR = 1
RL = 2
RR = 3


@dataclasses.dataclass
class AccSetup:
    file_path: str
    params: DataFrame

#     track: str
#     tire_compound: int
#     tire_pressures: List[int]
#     pass


def read_setup(setup_file) -> AccSetup:
    with open(setup_file, 'rt') as f:
        setup_params_raw = json.load(f)

    return AccSetup(setup_file.replace(' ', '_'), parse_setup_params(setup_params_raw))


def parse_setup_params(setup_params_raw: Dict) -> DataFrame:
    setup_params = {
        **build_diffs_by_tire_pos('PSI', extract_path(setup_params_raw, 'basicSetup', 'tyres', 'tyrePressure')),
        **build_diffs_by_tire_pos('Toe', extract_path(setup_params_raw, 'basicSetup', 'alignment', 'toe')),
        **build_diffs_by_tire_pos('Camber', extract_path(setup_params_raw, 'basicSetup', 'alignment', 'camber')),
        'Caster L': extract_path(setup_params_raw, 'basicSetup', 'alignment', 'casterLF'),
        'Caster R': extract_path(setup_params_raw, 'basicSetup', 'alignment', 'casterRF'),
        'Steer Ratio': extract_path(setup_params_raw, 'basicSetup', 'alignment', 'steerRatio'),
        'TC 1': extract_path(setup_params_raw, 'basicSetup', 'electronics', 'tC1'),
        'TC 2': extract_path(setup_params_raw, 'basicSetup', 'electronics', 'tC2'),
        'ABS': extract_path(setup_params_raw, 'basicSetup', 'electronics', 'abs'),
        'Eng Map': extract_path(setup_params_raw, 'basicSetup', 'electronics', 'eCUMap'),
        'Fuel': extract_path(setup_params_raw, 'basicSetup', 'strategy', 'fuel'),
        'Brk Cmpnd F': extract_path(setup_params_raw, 'basicSetup', 'strategy', 'frontBrakePadCompound'),
        'Brk Cmpnd R': extract_path(setup_params_raw, 'basicSetup', 'strategy', 'rearBrakePadCompound'),

        'ARB F': extract_path(setup_params_raw, 'advancedSetup', 'mechanicalBalance', 'aRBFront'),
        'ARB R': extract_path(setup_params_raw, 'advancedSetup', 'mechanicalBalance', 'aRBRear'),
        **build_diffs_by_tire_pos('Spring Rate', extract_path(setup_params_raw, 'advancedSetup', 'mechanicalBalance',
                                                              'wheelRate')),
        **build_diffs_by_tire_pos('Bump Up', extract_path(setup_params_raw, 'advancedSetup', 'mechanicalBalance',
                                                          'bumpStopRateUp')),
        **build_diffs_by_tire_pos('Bump Dn', extract_path(setup_params_raw, 'advancedSetup', 'mechanicalBalance',
                                                          'bumpStopRateDn')),
        **build_diffs_by_tire_pos('Bump Rng', extract_path(setup_params_raw, 'advancedSetup', 'mechanicalBalance',
                                                           'bumpStopWindow')),
        'Break TQ': extract_path(setup_params_raw, 'advancedSetup', 'mechanicalBalance', 'brakeTorque'),
        'Break Bias': extract_path(setup_params_raw, 'advancedSetup', 'mechanicalBalance', 'brakeBias'),
        **build_diffs_by_tire_pos('Dampers Bump Slow',
                                  extract_path(setup_params_raw, 'advancedSetup', 'dampers', 'bumpSlow')),
        **build_diffs_by_tire_pos('Dampers Rebound Slow',
                                  extract_path(setup_params_raw, 'advancedSetup', 'dampers', 'bumpSlow')),
        **build_diffs_by_tire_pos('Dampers Bump Fast',
                                  extract_path(setup_params_raw, 'advancedSetup', 'dampers', 'bumpFast')),
        **build_diffs_by_tire_pos('Dampers Rebound Fast',
                                  extract_path(setup_params_raw, 'advancedSetup', 'dampers', 'bumpFast')),
        'Ride Height F': extract_path(setup_params_raw, 'advancedSetup', 'aeroBalance', 'rodLength', missing=[np.nan] * 4)[2],
        'Ride Height R': extract_path(setup_params_raw, 'advancedSetup', 'aeroBalance', 'rodLength', missing=[np.nan] * 4)[0],
        'R Wing': extract_path(setup_params_raw, 'advancedSetup', 'aeroBalance', 'rearWing'),
        'F Splitter': extract_path(setup_params_raw, 'advancedSetup', 'aeroBalance', 'splitter'),
        'Brake Duct F': extract_path(setup_params_raw, 'advancedSetup', 'aeroBalance', 'brakeDuct', missing=[np.nan] * 2)[1],
        'Brake Duct R': extract_path(setup_params_raw, 'advancedSetup', 'aeroBalance', 'brakeDuct', missing=[np.nan] * 2)[0],
        'Diff Preload': extract_path(setup_params_raw, 'advancedSetup', 'drivetrain', 'preload'),
    }

    return pd.DataFrame.from_dict(setup_params, columns=['value'], dtype=float, orient='index')


def extract_path(d, *path, missing=None):
    for n in path:
        if n not in d:
            return missing
        d = d[n]
    return d


def build_diffs_by_tire_pos(name, vals_by_tire_pos: List) -> Dict:
    if vals_by_tire_pos is None:
        return {}
    return {f"{name} {tire_pos_labels[i]}": vals_by_tire_pos[i]
            for i in range(len(tire_pos_labels))}


