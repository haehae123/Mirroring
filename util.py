
MESSAGE_DELIMITER = " "

def contentToString(content):
	string = ""
	for ct in content:
		if ct is None or ct["body"] is None or ct["type"] != "message": continue
		if string != "": string += MESSAGE_DELIMITER
		string += ct["body"]
	return string


def getSegments(chat):
	currentSegmentStart = 0
	for i, ct in enumerate(chat["content"] + [{"type": "separator"}]):
		if ct is None: continue

		if ct["type"] == "separator":
			segment = chat["content"][currentSegmentStart:i]
			yield segment
			currentSegmentStart = i+1

# TODO refactor
def isGood(segment, args): # which segments should be filtered
	if args.dataset == "PANC":
		# Filters segments with more than 150 nonempty messages.
		# The few unbehaved PAN12 segments with >150 messages are already
		# filtered in PANC/create_datapack.py, the negative segments with non
		# nonempty messages are as well. This code is only for the segments from
		# the complete positive chats originally from CC2.
		numOfNonemptyMessages = len([msg for msg in segment if msg is not None])
		return 1 <= numOfNonemptyMessages <= 150
	if args.dataset == "VTPAN": return True # don't filter these
	return True # for other datasets also allow all segments
