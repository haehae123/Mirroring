import sys
sys.path.insert(0, "..") # to be able to import modules from parent directory
import xml.etree.ElementTree as ET
import html
import re
from itertools import chain
from collections import Counter
from Datasets.DynamicArray import DynamicArray
import argparse
import os
from datetime import datetime, timezone
import numpy as np
import json
from util import contentToString, getSegments
import csv
from pathlib import Path
from util import isGood, isNonemptyMsg

parser = argparse.ArgumentParser(description='Create a tsv dataset from a datapack')
parser.add_argument(
	"--dataset",
	dest='dataset',
	help="from which dataset the datapack is",
	required=True
)
parser.add_argument(
	"--datapackID",
	dest='datapackID',
	help="the unique identifier that the datapack is going to have"
)
args = parser.parse_args()
if args.datapackID is None: args.datapackID = args.dataset

print("\n---           Arguments           ---")
for key, val in args.__dict__.items(): print("%20s: %s" % (key, val))
print()

# will be aggregated
segmentLengths = {"predator": [], "non-predator": []}

def getStatistics(datapack, datasetType):

	chatClassCount = Counter()
	segmentClassCount = Counter()


	for chatName, chat in datapack["chats"].items():
		chatClassCount.update([chat["className"]])
		for i, segment in enumerate(getSegments(chat)):
			if not isGood(segment, args.dataset): continue

			segmentClassCount.update([chat["className"]])
			numOfNonemptyMessages = len(filter(isNonemptyMsg, segment))
			segmentLengths[chat["className"]].append(numOfNonemptyMessages)

	print("In %s:" % datasetType)
	total = segmentClassCount["predator"] + segmentClassCount["non-predator"]
	print("\tnumber of segments: %s" % total)
	print("\tchatClassCount = %s" % chatClassCount)
	print("\tsegmentClassCount = %s" % segmentClassCount)
	print("\tpredator class ratio: predator/all = %s/%s = %s%%" % (
		segmentClassCount["predator"], total,
		np.round(segmentClassCount["predator"]/total*100, 2)
	))


for datasetType in ["train", "test"]:
	datapackPath = "%s/datapacks/datapack-%s-%s.json" % (
		args.dataset, args.datapackID, datasetType)
	csvPath = "%s/csv/%s-%s.csv" % (
		args.dataset, args.datapackID, datasetType)
	with open(datapackPath, "r") as file:
		datapack = json.load(file)

		getStatistics(datapack, datasetType)

# save segment lengths to file
outPath = "%s/statistics/" % args.dataset
Path(outPath).mkdir(parents = True, exist_ok = True)
with open(outPath + "segment-lengths-%s.json" % args.datapackID, "w") as file:
	json.dump(segmentLengths, file)
