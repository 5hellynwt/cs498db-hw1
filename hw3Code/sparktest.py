import findspark
findspark.init()

import pyspark
import sys

if len(sys.argv) != 3:
        raise Exception("2 Arguments required!")

inputUrl = sys.argv[1]
outputUrl = sys.argv[2]

def myMapFunc(x):
        return (len(x),1)

def myReduceFunc(v1, v2):
        return v1 + v2

sc = pyspark.SparkContext()
print("Spark Context Initialized~")

lines = sc.textFile(sys.argv[1])

words = lines.flatMap(lambda line : line.split('\n') )
wordCount = words.map(myMapFunc).reduceByKey(myReduceFunc)
print("Map Reduce Complete!")

wordCount.saveAsTextFile(sys.argv[2])
print("Output saved as text file~")
