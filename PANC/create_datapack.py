import sys
sys.path.insert(0, "..") # to be able to import modules from parent directory
import xml.etree.ElementTree as ET
import html
import re
from itertools import chain
from collections import Counter
from Datasets.DynamicArray import DynamicArray
from Datasets.util import contentToString
import argparse
import os
from datetime import datetime, timezone
import json
from tqdm import tqdm
import random

parser = argparse.ArgumentParser(description='Evaluate a model')
parser.add_argument(
	"--datapackID",
	dest='datapackID',
	help="the unique identifier that the datapack is going to have",
	default="PANC"
)
parser.add_argument(
	"--PAN12datapackID",
	dest='PAN12datapackID',
	help="ID of the PAN12 datapack to use",
	default="PAN12"
)
parser.add_argument(
	"--CC2datapackID",
	dest='CC2datapackID',
	help="ID of the ChatCoder2 datapack to use",
	default="ChatCoder2"
)
parser.add_argument(
	"--description",
	dest='description',
	help="description of the datapack",
	default=None
)
args = parser.parse_args()

print("\n---           Arguments           ---")
for key, val in args.__dict__.items(): print("%20s: %s" % (key, val))
print()

currentDir = os.path.dirname(os.path.abspath(__file__))

# 1. get negative PAN12 segments
print("1. get negative PAN12 segments")

negativeChats = {}
for datasetType in ["train", "test"]:
	path = "PAN12/datapacks/datapack-%s-%s.json" % (
		args.PAN12datapackID, datasetType)
	with open(path, "r") as file:
		PAN12datapack = json.load(file)
		for chatName, chat in PAN12datapack["chats"].items():
			if chat["className"] == "non-predator":
				negativeChats[chatName] = chat

# 2. filter negative PAN12 segments
print("2. filter negative PAN12 segments")

for chatName, chat in list(negativeChats.items()):
	# the organizers said there would be no segments longer than 150 messages,
	# but actually there are. We will filter these for segment comparability.
	hasTooManyMessages = chat["numOfMessages"] > 150
	hasMoreThanTwoUsers = len(chat["authors"]) > 2
	if hasTooManyMessages or hasMoreThanTwoUsers: del negativeChats[chatName]; continue

	string = contentToString(chat["content"])
	isSpam = len(string) > 12970
	isASingleUserWhoSpams = len(chat["authors"]) == 1 and len(string) > 50
	if isSpam or isASingleUserWhoSpams: del negativeChats[chatName]; continue

# 3. get complete positive ChatCoder2 chats
print("3. get complete positive ChatCoder2 chats")

postiveChats = {}
path = "ChatCoder2/datapacks/datapack-%s.json" % args.CC2datapackID
with open(path, "r") as file:
	CC2Datapack = json.load(file)
	positiveChats = CC2Datapack["chats"]
	# These are complete chats. We HAVE to make sure, that the segments in the
	# complete chats which have >150 messages are NOT used for training or
	# evaluation! Nevertheless, we include them in the datapack to be able to
	# evaluate with complete positive chats.

# have all chats
chats = {**positiveChats, **negativeChats}

# 4. generate train and test sets
print("4. generate train and test sets")

random = random.Random(1) # set seed
positiveChatNames = sorted(positiveChats.keys())
negativeChatNames = sorted(negativeChats.keys())
random.shuffle(positiveChatNames)
random.shuffle(negativeChatNames)

trainTestRatio = .6
posSplitIndex = int(len(positiveChats)*trainTestRatio)
negSplitIndex = int(len(negativeChats)*trainTestRatio)

chatNames = {
	"train": positiveChatNames[:posSplitIndex] + negativeChatNames[:negSplitIndex],
	"test": positiveChatNames[posSplitIndex:] + negativeChatNames[negSplitIndex:]
}


def generateDatapack(datasetType):
	datapack = {
		"datapackID": args.datapackID + "-" + datasetType,
		"description": args.description,
		"generatedAtTime": int(datetime.now().timestamp()*1000), # unix timestamp
		"chats": {}
	}

	# filter chats for train/test set
	datasetTypeChats = set(chats.keys()).intersection(chatNames[datasetType])
	for chatName in datasetTypeChats:
		datapack["chats"][chatName] = chats[chatName]

	return datapack

# 5. generate and dump PANC datapack
print("5. generate and dump PANC datapack")

for datasetType in ["train", "test"]:
	datapack = generateDatapack(datasetType)
	print("len(datapack['chats']) = %s" % len(datapack['chats']))

	# dump generated datapack to json file
	outFile = "PANC/datapacks/datapack-%s-%s.json" % (args.datapackID, datasetType)
	with open(outFile, "w") as file: json.dump(datapack, file, indent=4)

	# also dump an info file for development
	infoFile = "PANC/datapacks/datapack-info-%s-%s.json" % (args.datapackID, datasetType)
	with open(infoFile, "w") as file: json.dump(chatNames, file, indent=4)
