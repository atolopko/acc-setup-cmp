import pandas as pd
from pandas import DataFrame

from acc_setup import AccSetup
from main import setup_file_short_name


def compare_setup_params(setup_a: DataFrame, setup_b: DataFrame) -> DataFrame:
    cmp = pd.concat([setup_a, setup_b], axis=1)
    return cmp


def compare_setups(*setups: AccSetup):
    values: pd.DataFrame = pd.concat([s.params for s in setups], axis=1,
                                     keys=[setup_file_short_name(s) for s in setups])

    deltas = pd.concat([pd.Series(s.params['value'], name='delta') - setups[0].params['value'] for s in setups[1:]],
                       axis=1,
                       keys=[(setup_file_short_name(s), 'delta') for s in setups[1:]])
    return pd.concat([values, deltas], axis=1)


def keep_only_deltas(cmp: DataFrame):
    return cmp[cmp.iloc[:, 2] != 0]
