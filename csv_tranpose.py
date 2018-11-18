import csv
from itertools import izip
import sys

targetFile = sys.argv[1] if len(sys.argv) > 1 else "result.csv"
a = izip(*csv.reader(open(targetFile, "rb"), delimiter="\t"))
csv.writer(open("output.csv", "wb")).writerows(a)
