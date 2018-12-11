import sys
import os
import pandas as pd
import logging as log
import imageio as im
import matplotlib.pyplot as plt


def plot_tsp(state):
    # plot state of problem

    # empty arrays for coords
    x = []
    y = []

    # Legend
    txt = 'temp = ' + str(round(state.temp, 6)) + ' cost = ' + str(state.cost)
    # Add text to figure, not plot
    plt.gcf().text(0.02, 0.02, txt)

    for city in state.tour:
        # add each cities coords
        x.append(city.x)
        y.append(city.y)
        try:
            # add city labels
            plt.annotate(xy=[city.x, city.y], s=' ' + str(city.name))
        except TypeError:
            log.info('Cannot label plot.')
        plt.axis('off')

    if state.complete > 0:
        # add trip back to source
        x.append(state.tour[0].x)
        y.append(state.tour[0].y)
        if state.complete == 1:
            # use full line
            plt.plot(x, y, 'go-')
            filename = state.path + 'solution.png'
        else:
            # use dotted line
            plt.plot(x, y, 'bo:')
            filename = state.path + '.png'

    else:
        # use points
        plt.plot(x, y, 'ro')
        filename = state.path + 'initial.png'

    if state.save:
        # save result figures
        try:
            # DPI = dots per inch
            plt.savefig(filename, format='png', dpi=300)
        except FileNotFoundError:
            # Create path if non-existent
            os.makedirs(state.path)
            plt.savefig(filename, format='png', dpi=300)
    else:
        plt.show()
    # clear plot for next call
    plt.clf()


def plot_stats(data_file, output):
    # Function to plot statistics 

    x = []
    y = []

    datafile = pd.read_csv('run_stats.txt',sep=',')

    plt.plot(x, y, 'ro')
    plt.show()

def write_results(filename, output):
    # function to write results to output file

    data = []
    file = filename + '.txt'
    # Drop tour description
    del output['tour']

    # Arrange in csv
    for key in output:
        data.append(str(output[key]))

    csv = ','.join(data)
    csv += '\n'
    # Write results to file
    with open(file, 'a+') as f:
        if f.tell() == 0:
            # Write headers if file empty
            head = []
            for key in output:
                head.append(str(key))
            headers = ','.join(head)
            headers += '\n'
            f.write(headers)
        f.write(csv)
        f.close()


def animate(path):
    # Function to animate progress plots

    image_dir = os.fsencode(path)
    files = os.listdir(image_dir)

    # Get list of filenames including path
    fnames = [path+os.fsdecode(f) for f in files if f.endswith(b'.png')]
    fnames.sort()

    # Read images
    images = [im.imread(f) for f in fnames]

    # Write GIF
    # Duration per frame
    im.mimsave(os.path.join(path+'animate.gif'), images, duration=0.33)

    # Delete partial PNGs
    files = [path+os.fsdecode(f) for f in files]
    deleted = [os.remove(f) for f in files if 'partial' in f] 
