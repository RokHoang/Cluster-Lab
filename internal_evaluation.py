import collections
import sys
import csv
import os
import math

class InternalEvaluation:
    def __init__(self, inputfile, X, Y):
        self.inputfile = inputfile
        self.X = int(X)
        self.Y = int(Y)
        self.clusters = collections.defaultdict(list)
        self.centroids = []
        self.averagedis = []

    def readData(self):
        if not os.path.isfile(self.inputfile):
            print 'Not a file'
            return -1

        csvfile = open(self.inputfile, 'rb')

        # Read csv file
        data = list(csv.reader(csvfile))

        # Convert to float type
        data_list = [[float(x) for x in datum] for datum in data]

        # Group data into cluster
        for datum in data_list:
            self.clusters[int(datum[-1])].append(datum[:-1])

        # Check X and Y
        if self.X >= len(data_list[0]) - 1:
            print 'Wrong X'
            return -1
        if self.Y >= len(data_list[0]) - 1:
            print 'Wrong Y'
            return -1

        return 0

    def centerData(self, s):
        centroid_X = 0
        centroid_Y = 0
        for datum in s:
            centroid_X += datum[self.X]
            centroid_Y += datum[self.Y]

        return (centroid_X/len(s), centroid_Y/len(s))

    @staticmethod
    def euclideanDis(a, b):
        return math.sqrt(sum([(a[i]-b[i])**2 for i in range(len(a))]))

    # Implement Davies-Bouldin index
    def daviesEval(self):
        # Find centroid by averaging data
        self.centroids = [self.centerData(self.clusters[key]) for key in self.clusters]

        # Find average distance to centroid in each cluster
        for key in self.clusters:
            average_dis = 0.0
            for datum in self.clusters[key]:
                average_dis += self.euclideanDis(self.centroids[key], (datum[self.X], datum[self.Y]))
            self.averagedis.append(average_dis/len(self.clusters[key]))

        # Now apply davies Bouldin index
        distance = 0
        for i in range(len(self.clusters) - 1):
            max_dis = -1
            for j in range(i + 1, len(self.clusters)):
                try:
                    dis = (self.averagedis[i] + self.averagedis[j]) \
                          / self.euclideanDis(self.centroids[i], self.centroids[j])
                # When 2 clusters have the same centroid's position, euclidean will be 0
                except:
                    dis = 0
                if dis > max_dis:
                    max_dis = dis
            distance += max_dis
        print 'Davies-Boudlin index is: %f' % (distance / len(self.clusters))
        return distance / len(self.clusters)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Wrong paramters'
        exit()
    inputfile = sys.argv[1]
    X = sys.argv[2]
    Y = sys.argv[3]
    eval = InternalEvaluation(inputfile, X, Y)
    if eval.readData() != -1:
        eval.daviesEval()