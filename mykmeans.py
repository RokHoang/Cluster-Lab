import random
import operator
import csv
import sys
from math import sqrt
def euclidean(a,b):
	return sqrt(sum([(a[i]-b[i])**2 for i in range(len(a))]))
def manhattan(a,b):
	return sum([abs(a[i] - b[i]) for i in range(len(a))])
def cosine(a,b):
	return sum([a[i]*b[i] for i in range(len(a))])/\
			(sqrt(sum([(a[i])**2 for i in range(len(a))]))*\
			sqrt(sum([(b[i])**2 for i in range(len(a))])))
def nearest(d,means,dist):
	dist_to_centroid = [dist(m,d) for m in means]
	return dist_to_centroid.index(min(dist_to_centroid))
def center(s):
	return map(lambda items: sum(items)/len(items),zip(*s))
def kmean(data, k, dist):
	means = [data[i] for i in random.sample(range(len(data)), k)]	
	subset = [[] for i in range(k)]
	for d in data:
		subset[nearest(d,means,dist)].append(d)
	means = [center(s) for s in subset]
	
	while (True):
		means_old = means
		subset = [[] for i in range(k)]	
		for d in data:
			subset[nearest(d,means,dist)].append(d)
		means = [center(s) for s in subset]
		if (means == means_old):
			break
	SSE = 0.0
	for i in range(len(subset)):
		for point in subset[i]:
			SSE += dist(point,means[i])**2
	print "SSE =",SSE
	return subset
def readfile(fi):
	csvfile = open(fi, 'rb')
	data = list(csv.reader(csvfile))
	csvfile.close()
	return [[float(j) for j in i] for i in data]
def writefile(fo,data):
	csvfile = open(fo, "wb")
	writer = csv.writer(csvfile)
	for i in range(len(data)):
		for row in data[i]:
			writer.writerow(row+[i])
if __name__ == "__main__":
	fi = sys.argv[1]
	fo = sys.argv[2]
	k = int(sys.argv[3])
	random_seed = int(sys.argv[4])
	#random.seed(random_seed)
	dist_type = int(sys.argv[5])
	#1:euclid
	#2:manhatta
	#3:cosine
	dist = [euclidean,manhattan,cosine]
	data = readfile(fi)
	#print data
	dataout = kmean(data,k,dist[dist_type-1])
	writefile(fo,dataout)

	#python mykmeans.py fi.txt fo.txt 2 3 1