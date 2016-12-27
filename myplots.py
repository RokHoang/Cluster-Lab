from mykmeans import *
import csv
import os
import matplotlib.pyplot as plt
import numpy as np


class MyPlot():
    def __init__(self, input, output, x, y):
        self.inputfile = input
        self.output = output
        self.x = int(x)
        self.y = int(y)

    # Read data
    def readData(self):
        if not os.path.isfile(self.inputfile):
            print 'Cannot find the file'
            return -1
        csvfile = open(self.inputfile, 'rb')

        # Get data from csv file
        data = list(csv.reader(csvfile))

        # Convert data to float
        self.data = [[float(j) for j in i] for i in data]

        # Get the cluster
        clusters = [data[-1] for data in self.data]
        self.clusters = set(clusters)

        # Close csv file
        csvfile.close()
        return 1

    # Plot data according to x and y
    def plotData(self):
        # Check x and y
        if self.x < 0 or self.x > len(self.data[0]) - 2:
            print 'Wrong coordinate for x'
            return -1
        if self.y < 0 or self.y > len(self.data[0]) - 2:
            print 'Wrong coordinate for y'
            return -1

        # Create color for each cluster
        colors = plt.cm.Spectral(np.linspace(0, 1, len(self.clusters)))
        for datum in self.data:
            col = colors[int(datum[-1]), :]
            plt.plot(datum[self.x], datum[self.y], 'o', markerfacecolor=col, markersize=14)

        plt.title('Clusters according to attributes in x and y')
        plt.savefig(self.output)
        return 1

if __name__ == '__main__':
    input = sys.argv[1]
    output = sys.argv[2]
    x = sys.argv[3]
    y = sys.argv[4]
    plot = MyPlot(input, output, x, y)
    if plot.readData():
        plot.plotData()



