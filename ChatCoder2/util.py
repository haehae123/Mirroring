def generalStats(chats):
	numberOfChats = len(chats)
	numberOfMessages = 0
	numberOfPredatorMessages = 0
	noneMessages = 0
	for chatName in chats:
		numberOfMessages += chats[chatName]["messages"].size()
		# print("%s: %s" % (chatName, chats[chatName]["messages"].size()))
		for messageI, message in enumerate(chats[chatName]["messages"], start=0):
			if message == None:
				noneMessages+=1
				# chats[chatName]["hasErrors"] = True
				continue
			if message["isPredator"]:
				numberOfPredatorMessages += 1

	numberOfVictimMessages = numberOfMessages - numberOfPredatorMessages
	# there are only two types of messages

	print("In total: %s chats with a total of %s messages, averaging %s messages per chat" % (numberOfChats, numberOfMessages, round(numberOfMessages/numberOfChats)))
	print("In total: %s `None` Messages" % (noneMessages))

	errorChats = 0
	for chatName in chats:
		if chats[chatName]["hasErrors"]: errorChats += 1
	print("In total: %s error chats" % (errorChats))
