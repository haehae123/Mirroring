
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
