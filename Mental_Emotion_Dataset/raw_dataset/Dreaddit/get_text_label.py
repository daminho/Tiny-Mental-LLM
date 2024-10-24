import pandas as pd
import csv
names = ["train", "test"]


for name in names:
	data = pd.read_csv(f"./original/{name}_raw.csv", encoding = 'unicode_escape')

	texts = [x for x in data['text']]
	labels = [("yes" if x == 1 else "no") for x in data['label']]

	labels_dicts = {}

	for label in labels:
		if( not (label in labels_dicts.keys())):
			labels_dicts[label] = 0
		labels_dicts[label] += 1

	with open(f"./raw/{name}.csv", "w") as output_file:
		writer = csv.writer(output_file)
		writer.writerow(["text", "label"])
		print(f"writing {len(texts)} texts and {len(labels)} labels")
#		print(f"{texts}")
		for i in range (len(texts)):
			writer.writerow([texts[i], labels[i]])
		output_file.close()

	print(f"For Dataset {name} label distribution is {labels_dicts}")
		
