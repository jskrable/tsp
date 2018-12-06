import matplotlib.pyplot as plt
import sys
import os
import logging as log


def plot_tsp(cities, complete, save, path):
    # plot map of cities

    # empty arrays for coords
    x = []
    y = []

    for city in cities:
        # add each cities coords
        x.append(city.x)
        y.append(city.y)
        try:
            # add city labels
            plt.annotate(xy=[city.x, city.y], s=' ' + str(city.name))
        except TypeError:
            log.info('Cannot label plot.')
        plt.axis('off')
    if complete > 0:
        # add trip back to source
        x.append(cities[0].x)
        y.append(cities[0].y)
        if complete == 1:
            # use full line
            plt.plot(x, y, 'go-')
            filename = path + 'solution.png'
        else:
            # use dotted line
            plt.plot(x, y, 'bo:')
            filename = path + '_partial.png'
            
    else:
        # use points
        plt.plot(x, y, 'ro')
        filename = path + 'problem.png'

    if save:
        # save result figures
        try:
            plt.savefig(filename)
        except FileNotFoundError:
            os.makedirs(path)
            plt.savefig(filename)
    else:
        plt.show()

    plt.clf()


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
        print('writing output file...')
        # Check for empty file
        if f.tell() == 0:
            head = []
            for key in output:
                head.append(str(key))
            headers = ','.join(head)
            headers += '\n'
            f.write(headers)
        f.write(csv)
        f.close()
        print(file + ' written successfully.')
