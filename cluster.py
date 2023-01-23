import re
import sys

import matplotlib.pyplot as plt
import pandas as pd
from scipy.cluster import hierarchy

from acc_setup import read_setup

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)


def load_data(setup_files_files: str) -> pd.DataFrame:

    with open(setup_files_files) as setup_files_file:
        setup_files = [lines.strip() for lines in setup_files_file.readlines()]
    setups = [read_setup(f).params.transpose() for f in setup_files]
    columns_to_drop = ['PSI FL', 'PSI FR', 'PSI RL', 'PSI RR', 'Fuel']
    X = pd.concat(setups, axis=0).drop(columns=columns_to_drop)

    labels = [re.match(r'.+/(.+/.+).json', file_name).group(1) for file_name in setup_files]
    X.index = labels

    return X


def cluster(X):
    return hierarchy.linkage(X, 'single')


def display(Z, labels):
    plt.figure(figsize=(10, 10), dpi=600, clear=True)
    rendering = hierarchy.dendrogram(Z, orientation='left', labels=labels, leaf_font_size=6)
    plt.show()


if __name__ == '__main__':
    setups = load_data(sys.argv[1])
    display(cluster(setups), labels=setups.index)
    print("done")



