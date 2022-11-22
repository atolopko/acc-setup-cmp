import dataclasses
import json
import os
import sys
from pprint import pp
from typing import List, Dict
import pandas as pd


# @dataclasses.dataclass
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

    return AccSetup(setup_file, parse_setup_params(setup_params_raw))


def parse_setup_params(setup_params_raw: Dict) -> DataFrame:
    setup_params = {
        **build_diffs_by_tire_pos('psi', extract_path(setup_params_raw, 'basicSetup', 'tyres', 'tyrePressure')),
        **build_diffs_by_tire_pos('toe', extract_path(setup_params_raw, 'basicSetup', 'alignment', 'toe')),
        'ARB F': extract_path(setup_params_raw, 'advancedSetup', 'mechanicalBalance', 'aRBFront'),
        'ARB R': extract_path(setup_params_raw, 'advancedSetup', 'mechanicalBalance', 'aRBRear'),
        **build_diffs_by_tire_pos('wheelRate', extract_path(setup_params_raw, 'advancedSetup', 'mechanicalBalance',
                                                            'wheelRate')),
        **build_diffs_by_tire_pos('bumpUp', extract_path(setup_params_raw, 'advancedSetup', 'mechanicalBalance',
                                                            'bumpStopRateUp')),
        **build_diffs_by_tire_pos('bumpDn', extract_path(setup_params_raw, 'advancedSetup', 'mechanicalBalance',
                                                            'bumpStopRateDn')),
        **build_diffs_by_tire_pos('bumpRng', extract_path(setup_params_raw, 'advancedSetup', 'mechanicalBalance',
                                                            'bumpStopWindow')),
        'Break TQ': extract_path(setup_params_raw, 'advancedSetup', 'mechanicalBalance', 'brakeTorque'),
        'Break Bias': extract_path(setup_params_raw, 'advancedSetup', 'mechanicalBalance', 'brakeBias'),
    }

    return pd.DataFrame.from_dict(setup_params, columns=['values'], orient='index')


def extract_path(d, *path):
    for n in path:
        if n not in d:
            return None
        d = d[n]
    return d


def build_diffs_by_tire_pos(name, vals_by_tire_pos: List) -> Dict:
    if vals_by_tire_pos is None:
        return {}
    return {f"{name} {tire_pos_labels[i]}": vals_by_tire_pos[i]
            for i in range(len(tire_pos_labels))}


def compare_setup_params(setup_a: DataFrame, setup_b: DataFrame) -> DataFrame:
    cmp = pd.concat([setup_a, setup_b], axis=1)
    return cmp


def compare_setups(setup_a: AccSetup, setup_b: AccSetup):
    cmp = compare_setup_params(setup_a.params, setup_b.params)
    cmp['delta'] = cmp.iloc[:, 1] - cmp.iloc[:, 0]
    cmp.columns = [setup_file_short_name(setup_a),
                   setup_file_short_name(setup_b),
                   'delta']
    return cmp


def setup_file_short_name(setup_a):
    return os.path.splitext(os.path.basename(setup_a.file_path))[0]


def keep_only_deltas(cmp: DataFrame):
    return cmp[cmp.delta != 0]


if __name__ == '__main__':
    setup_a_file, setup_b_file = sys.argv[1:3]
    print(keep_only_deltas(compare_setups(read_setup(setup_a_file), read_setup(setup_b_file))))
