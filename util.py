
MESSAGE_DELIMITER = " "

def contentToString(content):
	string = ""
	for ct in content:
		if not isNonemptyMsg(ct) or ct["type"] != "message": continue
		if string != "": string += MESSAGE_DELIMITER
		string += ct["body"]
	return string


def getSegments(chat):
	currentSegmentStart = 0
	for i, ct in enumerate(chat["content"] + [{"type": "separator"}]):
		if ct is None or ct["type"] != "separator": continue # await separator

		segment = chat["content"][currentSegmentStart:i]
		yield segment
		currentSegmentStart = i+1

PANC_MIN_MSG_NUM = 6
PANC_MAX_MSG_NUM = 150

# TODO refactor
def isGood(segment, dataset): # which segments should be filtered
	if dataset == "PANC":
		# Filters segments with more than 150 nonempty messages.
		# The few unbehaved PAN12 segments with >150 messages are already
		# filtered in PANC/create_datapack.py, the negative segments with non
		# nonempty messages are as well. This code is only for the segments from
		# the complete positive chats originally from CC2.
		numOfNonemptyMessages = len(filter(isNonemptyMsg, segment))
		return PANC_MIN_MSG_NUM <= numOfNonemptyMessages <= PANC_MAX_MSG_NUM
	if dataset == "VTPAN": return True # don't filter these
	return True # for other datasets also allow all segments

def isNonemptyMsg(msg):
	return msg is not None and bool(msg["body"])
