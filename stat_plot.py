import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline


def plot_stats(data_file, output):
    # Function to plot statistics
    # Holder arrays for data
    x = []
    y1 = []
    y2 = []
    
    # Read and sort csv
    data = pd.read_csv(data_file, sep=',')
    data.sort_values(by='size')
    # Fill axes
    for i, r in data.iterrows():
        x.append(r['size'])
        y1.append(r['duration'])
        y2.append(r['alpha'])

    # Best fit line
    """
    par = np.polyfit(x,y1,1,full=True)
    slope = par[0][0]
    intercept = par[0][1]
    bf_x1 = [min(x),max(x)]
    bf_y1 = [slope*x + intercept for x in bf_x1]
    plt.plot(bf_x1, bf_y1, '-r')
    """
    # Smooth y2 line
    """
    s_x = np.linspace(min(x),max(x),300)
    spl = make_interp_spline(x,y2,k=3)
    s_y2 = spl(s_x)
    """

    # Split plot for 2 y-axes
    fig, ax1 = plt.subplots()
    color = 'tab:blue'
    ax1.set_ylabel('alpha', color=color)
    ax1.plot(x, y2, color=color)

    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_xlabel('number of cities')
    ax2.set_ylabel('solve time (s)', color=color)
    ax2.scatter(x, y1, s=5, color=color)

    plt.show()


def main():

    file = 'run_stats.txt'
    plot_stats(file)
