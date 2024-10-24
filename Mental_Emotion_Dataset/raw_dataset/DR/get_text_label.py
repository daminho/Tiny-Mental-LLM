import pandas as pd
import csv
import copy
names = ["train", "val", "test"]

data_texts = {name: [] for name in names}
data_labels = {name: [] for name in names}

for name in names:
	data = pd.read_csv(f"./original/{name}_raw.csv", encoding = 'unicode_escape')

	texts = [x for x in data['Text']]
	labels = [x for x in data['Label']]
	
	data_texts[name] = copy.deepcopy(texts)
	data_labels[name] = copy.deepcopy(labels)

#	labels_dicts = {}

final_texts = {}
final_texts["train"] = data_texts["train"] + data_texts["val"]
final_texts["test"] = data_texts["test"]

final_labels = {}
final_labels["train"] = data_labels["train"] + data_labels["val"]
final_labels["test"] = data_labels["test"]


for name in names:
	if(name == "val"):
		continue

	labels_dicts = {}

	texts = final_texts[name]
	labels = final_labels[name]

	for label in labels:
		if( not (label in labels_dicts.keys())):
			labels_dicts[label] = 0
		labels_dicts[label] += 1

	with open(f"./raw/{name}.csv", "w") as output_file:
		writer = csv.writer(output_file)
		writer.writerow(["text", "label"])
		print(f"writing {len(texts)} texts and {len(labels)} labels")
		#               print(f"{texts}")
		for i in range (len(texts)):
			writer.writerow([texts[i], labels[i]])
		output_file.close()

	print(f"For Dataset {name} label distribution is {labels_dicts}")


