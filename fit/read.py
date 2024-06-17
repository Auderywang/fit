import csv
import numpy as np


def read_raw(name: str, data_col: int):
    t = []
    T2 = []

    concentration: str = None
    substance: str = None

    reader = csv.reader(open(name + '.csv'))

    for i, line in enumerate(reader):
        if i > 0:
            T2.append(float(line[data_col]))
            t.append(float(line[2]))
        else:
            concentration = line[-2]
            substance = line[-1]



    t = np.asarray(t)
    T2 = np.asarray(T2)

    return (substance, concentration, t, T2)