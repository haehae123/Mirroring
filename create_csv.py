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
from util import isGood

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

def writeCSV(file, datapack, datasetType):
	writer = csv.writer(file, quotechar='"', quoting=csv.QUOTE_ALL)
	writer.writerow(["label", "chatName", "segment"]) # header

	for chatName, chat in datapack["chats"].items():
		for i, segment in enumerate(getSegments(chat)):
			if not isGood(segment, args.dataset): continue

			# add segment number if segment is not whole chat
			segmentName = "%s-%s" % (chatName, i) \
				if len(segment) != len(chat["content"]) else chatName

			writer.writerow([chat["className"], segmentName, contentToString(segment)])

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

print("\nSuccessfully wrote all csv files")
