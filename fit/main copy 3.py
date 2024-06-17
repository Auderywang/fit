import scipy
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
import csv
import math

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['font.family'] = 'Times New Roman'
# plt.rcParams['mathtext.default'] = 'regular'
plt.rcParams['mathtext.fontset'] = 'stix'

from read import read_raw

read_env = True

# 改这个
file_list = [
    ('hydrophilic membrane', 3),
    ('Hydrophilic membrane + ethanol', 3),
    ('hydrogel', 3),
]

color_list = [
    'red',
    'blue',
    'black'
]

fig, ax = plt.subplots(dpi=300)

t_min = []
t_max = []
T_min = []
T_max = []

min_size = None

for (file_name, data_col), color in zip(file_list, color_list):
    (substance, concentration, t, T) = read_raw(file_name, data_col=data_col)
    
    current_size = t.size

    if min_size == None:
        min_size = current_size
    else:
        if min_size > current_size:
            min_size = current_size

for (file_name, data_col), color in zip(file_list, color_list):

    print(file_name)
    (substance, concentration, t, T) = read_raw(file_name, data_col=data_col)

    substance = '$\mathrm{' + substance + '}$'

    t = t[:min_size]
    T = T[:min_size]

    t_min.append(t.min())
    t_max.append(t.max())
    T_min.append(T.min())
    T_max.append(T.max())

    a0 = T.max() - T.min()
    a1 = t[t.size // 2]
    a2 = T.min()
    p0 = [a0, a1, a2]

    def target_fn(x, a0, a1, a2):
        return a0 * np.exp(-x / a1) + a2

    para, cov = opt.curve_fit(target_fn, t, T, p0=p0)

    T_fit = np.asarray([
        target_fn(x, *para) for x in t
    ])

    ax.plot(t, T_fit, label=substance + ' ' + concentration, linewidth='2', color=color)

    loc_list = ['top', 'bottom', 'left', 'right']

    for loc in loc_list:
        ax.spines[loc].set_linewidth(1.5)

ax.grid(False)
ax.tick_params(width=1.5)   
ax.set_xlabel('t (s)', fontdict={'weight': 'bold'})
ax.set_ylabel('ΔT (°C)', fontdict={'weight': 'bold'})
ax.set_xlim([min(t_min)-10, max(t_max)+10])
ax.set_ylim([math.floor(min(T_min)), math.ceil(max(T_max))])
ax.set_yticklabels(ax.get_yticks(), weight='bold')
ax.set_xticklabels(ax.get_xticks(), weight='bold')
ax.legend(frameon=False, framealpha=0, prop={'family': 'Times New Roman'})

plt.savefig('fig3.png', dpi=300, bbox_inches='tight')
plt.show()