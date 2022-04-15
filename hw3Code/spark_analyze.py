import findspark
findspark.init()

import pyspark
import sys
import json
import os

wordList = sys.argv[1].split(',')
weights = json.loads(sys.argv[2])
outfile = sys.argv[3]

print("wordList", wordList, type(wordList))
print("weights", weights, type(weights))
print("outfile", outfile)

os.system("rm -rf " + outfile)

def file_splitter(f):
        l = f.split('\n')
        res = []
        for line in l:
                for word in wordList:
                        if word in line:
                                res.append((word, line))
        return res 

def mapWeightFunc(x):
        weight = 0
        for c in x[1]:
                if c in weights:
                        weight += weights[c]
        return (x[0], x[1], weight)

def redFunc(v1, v2):
        print(v1, v2)
        return max(v1, v2, key=lambda x : x[-1])

sc = pyspark.SparkContext()

file = sc.textFile("War_and_Peace.txt")

lines = file.flatMap(lambda x : file_splitter(x) )

linesWeight = lines.map(mapWeightFunc).map(lambda x : (x[0], x)).reduceByKey(lambda x1, x2: max(x1, x2, key=lambda $

linesWeight.saveAsTextFile(outfile)

os.system("cat analyzed/part-00000 analyzed/part-00001 > analyzed/merged")
