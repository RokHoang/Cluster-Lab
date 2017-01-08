import sys
import random
import csv
import copy
import math
from collections import defaultdict
from mykmeans import euclidean
from pprint import pprint

def readfile(filename):
    file_data = {}
    csvfile = open(filename, 'rb')
    data = list(csv.reader(csvfile))
    csvfile.close()

    for index, line in enumerate(data[1:]):
        file_data[index] = {'features': [float(x) for x in line[1:]], 'label': line[0]}

    return file_data

def region_query(data, count, eps):
    '''
    clus: -1 -> noise, -2 -> not visite, >0: cluster_id
    '''
    neighbours = defaultdict(lambda : {'n' : set(), 'label' : '', 'clus' : -2, 'max' : 0})
    length = count

    for i in range(length - 1) :
        for j in range(i + 1, length) :
            dist = euclidean(data[i]['features'], data[j]['features'])
            if dist <= eps :
                # 2 points are neighbors
                neighbours[i]['n'].add(j)
                neighbours[j]['n'].add(i)

    for i in range(length) :
        neighbours[i]['label'] = data[i]['label']
        neighbours[i]['max'] = len(neighbours[i]['n'])
        # NOISE
        if neighbours[i]['max'] == 0 :
            neighbours[i]['clus'] = -1
    return neighbours

def select_unvisited(neighbours):
    maxsub = -1
    max_neighbours_num = 0
    for key, val in neighbours.iteritems() :
        if val['clus'] == -2 :
            if val['max'] > max_neighbours_num :
                maxsub = key
                max_neighbours_num = val['max']
    return maxsub

def expand_cluster(neighbours, point, minpts):
    candidates = copy.deepcopy(neighbours[point]['n'])
    while len(candidates) > 0:
        _point = candidates.pop()
        # skip noise
        if neighbours[_point]['clus'] > -1:
            continue
        neighbours[_point]['clus'] = point
        if neighbours[_point]['max'] >= minpts:
            candidates.union(neighbours[_point]['n'])

def dbscan(data, count, eps, minpts, fileout):
    neighbours = region_query(data, count, eps)
    while True:
        point = select_unvisited(neighbours)
        if point < 0:
            break
        if neighbours[point]['max'] > minpts:
            neighbours[point]['clus'] = point
            expand_cluster(neighbours, point, minpts)
        else:
            neighbours[point]['clus'] = -1
            for key, val in neighbours.iteritems():
                if val['clus'] == -2:
                    neighbours[key]['clus'] = -1
    evaluate(neighbours, fileout)

def evaluate(data, fileout):
    stat = defaultdict(lambda : defaultdict(lambda : 0))
    for k, v in data.iteritems() :
        stat[v['clus']][v['label']] += 1

    wholecount = 0
    wholecorrect = 0
    norecall = 0
    for k, v in stat.iteritems() :
        with open(fileout, 'at') as f:
            allcount = 0
            maxj = 0
            maxi = ''
            for i, j in v.iteritems() :
                allcount += j
                if j > maxj :
                    maxj = j
                    maxi = i
            if k != -1 :
                wholecorrect += maxj
                wholecount += allcount
            else :
                norecall += allcount
            f.write("Cluster: {}\n|Correct: {}\n|Precision: {}\n|Label: {}\n".format(k, allcount, maxj, float(maxj) / allcount, maxi))

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print "Wrong argument format."
    else:
        filein, fileout, eps, minpts = sys.argv[1:]
        print filein, fileout, eps, minpts
        data = readfile(filein)
        count = len(data.keys())
        dbscan(data, count, float(eps), int(minpts), fileout)
