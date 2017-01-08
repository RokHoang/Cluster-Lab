from mykmeans import *
import pprint
from collections import defaultdict
import itertools
def main():
	num_run = 20
	weak_sign = 1
	data_type,data = readfile("animal-dental.csv")
	#d = [[] for i in range(num_run)]
	ddict = defaultdict(lambda:defaultdict(int))
	for i in range(num_run):
		d = sorted(kmean(data, 6, euclidean),key = len)
		for group in d:
			for x,y in itertools.permutations(group,2):	
				ddict[x[0]][y[0]] += 1
	#pprint.pprint(ddict)
	weaklink = defaultdict(int)
	for key,value in ddict.iteritems():
		for v in value.values():
			if (v <= 1):
				weaklink[key] += 1
	for key,value in weaklink.iteritems():
		if (value <= weak_sign):
			print key
	#print [[len(j) for j in i]for i in d]
	#pprint.pprint(ddict)
main()