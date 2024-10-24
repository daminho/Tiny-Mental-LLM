import csv


names = ["train", "test"]

for name in names:
	with open(f"./raw/{name}.csv", "w") as output_file:
		writer = csv.writer(output_file)
		writer.writerow(["text", "label"])
		with open(f"./{name}ing-set.csv", "r", encoding = "utf8") as input_file:
			reader = csv.reader(input_file)
			label_dicts = {}
			for id, row in enumerate(reader):
				if(id == 0):
					continue
				text = row[2]
				label = "suicidal" if row[5] == '1' else "depression"
				if(not (label in label_dicts.keys())):
					label_dicts[label] = 0
				label_dicts[label] += 1
				writer.writerow([text, label])
			input_file.close()
		output_file.close()
	print(f"For {name} dataset, the label distribution is {label_dicts}")
