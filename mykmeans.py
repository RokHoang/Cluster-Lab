import random
import operator
import csv
import sys
import numpy as np
from math import pi
import math 
from math import sqrt
def euclidean(a,b):
	return sqrt(sum([(a[i]-b[i])**2 for i in range(1,len(a))]))
def manhattan(a,b):
	return sum([abs(a[i] - b[i]) for i in range(1,len(a))])
def cosine(a,b):
		#result = sum([a[i]*b[i] for i in range(len(a))])/\
		#	(sqrt(sum([(a[i])**2 for i in range(len(a))]))*\
		#	sqrt(sum([(b[i])**2 for i in range(len(a))])))
	try:
		a_ = np.array(a[1:])
		b_ = np.array(b[1:])
		result = np.dot(a_.T,b_)/(sqrt(np.dot(a_,a_))*sqrt(np.dot(b_,b_)))
		if result >= 1.0:
			return 0.0
		return math.acos(result)
	except:
		raise
def nearest(d,means,dist):
	dist_to_centroid = [dist(m,d) for m in means]
	return dist_to_centroid.index(min(dist_to_centroid))
def center(s):
	return [["x"]] + map(lambda items: sum(items)/len(items),zip(*s)[1:])
def kmean(data, k, dist):
	data_uni = [["x"] + list(y) for y in set(tuple(x[1:]) for x in data)]

	means = [data_uni[i] for i in random.sample(range(len(data_uni)), k)]
	#means = [data[i] for i in random.sample(range(len(data)), k)]
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
		if (means[1:] == means_old[1:]):
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
	"""
	data_list = []
	for i in range(1, len(data)):
		datum_list = []
		for datum in data[i]:
			try:
				datum_list.append(int(datum))
			except:
				pass
		data_list.append(datum_list)
	return data_list
	"""
	return data[0],[[i[0]] + [float(j) for j in i[1:]] for i in data[1:]]
def writefile(fo,data_type,data):
	csvfile = open(fo, "wb")
	writer = csv.writer(csvfile)
	writer.writerow(data_type+["Type"])
	for i in range(len(data)):
		for row in data[i]:
			writer.writerow(row+[i])
if __name__ == "__main__":
	if len(sys.argv) != 6:
		print 'Wrong parameter'
		exit()

	fi = sys.argv[1]
	fo = sys.argv[2]
	k = int(sys.argv[3])
	random_seed = int(sys.argv[4])
	#print "seed: ",random.getstate()
	random.seed(random_seed)
	dist_type = int(sys.argv[5])
	#1:euclid
	#2:manhatta
	#3:cosine
	dist = [euclidean,manhattan,cosine]
	data_type,data = readfile(fi)

	dataout = kmean(data,k,dist[dist_type-1])
	writefile(fo,data_type,dataout)

	#python mykmeans.py fi.txt fo.txt 2 3 1