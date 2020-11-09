
VT_ID_paths = {
	"train": 'stuff/VT_train_IDs.txt',
	"test": 'stuff/VT_test_IDs.txt'
}
VT_IDs = {
	"train": [],
	"test": [],
	"all": []
}

# read IDs from file
for datasetType in ["train", "test"]:
	with open(VT_ID_paths[datasetType]) as file:
		IDs = [line.strip() for line in file.readlines()]
	VT_IDs[datasetType] = IDs
	VT_IDs["all"] += IDs

print("len(VT_IDs['train']) = %s" % (len(VT_IDs['train'])))
print("len(VT_IDs['test']) = %s" % (len(VT_IDs['test'])))
