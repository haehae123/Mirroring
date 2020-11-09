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

def isGood(segment): # which segments should be filtered
	if args.dataset == "PANC":
		# filter empty segments and those with more than 150 messages
		# the latter are a few unbehaved PAN12 segments and long CC2 segments
		return 1 <= len([msg for msg in segment if msg is not None]) <= 150
	if args.dataset == "VTPAN": return True # allow all segments
	return True # for other datasets also allow all segments

def writeCSV(file, datapack, datasetType):
	writer = csv.writer(file, quotechar='"', quoting=csv.QUOTE_ALL)
	writer.writerow(["label", "chatName", "segment"]) # header

	for chatName, chat in datapack["chats"].items():
		for i, segment in enumerate(getSegments(chat)):
			if not isGood(segment): continue

			# add segment number if segment is not whole chat
			segmentName = "%s-%s" % (chatName, i) \
				if len(segment) != len(chat["content"]) else chatName

			writer.writerow([chat["className"], segmentName, contentToString(segment)])

def printStatistics(datapack, datasetType):

	chatClassCount = Counter()
	segmentClassCount = Counter()

	for chatName, chat in datapack["chats"].items():
		chatClassCount.update([chat["className"]])
		for i, segment in enumerate(getSegments(chat)):
			if not isGood(segment): continue

			segmentClassCount.update([chat["className"]])

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

		# write TSV
		with open(csvPath, 'w', newline='') as file:
			writeCSV(file, datapack, datasetType)
			printStatistics(datapack, datasetType)

print("\nSuccessfully wrote all csv files")
