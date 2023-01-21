import os
import sys

import pandas as pd

from acc_setup import read_setup, AccSetup
from compare import compare_setups, keep_only_deltas


def setup_file_short_name(setup_a: AccSetup):
    return os.path.splitext(os.path.basename(setup_a.file_path))[0]


if __name__ == '__main__':
    setup_files = sys.argv[1:]
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.float_format', '{:,.1f}'.format)
    comparison = compare_setups(*[read_setup(setup_file) for setup_file in setup_files])

    output = keep_only_deltas(comparison)
    delta_cols = output.columns[output.columns.get_level_values(1) == 'delta']
    print(output)

