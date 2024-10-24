import csv
import random
import copy
names = ["train", "test"]

datas = {name: [] for name in names}


with open("./original/raw.csv", "r") as input_file:
	reader = csv.reader(input_file)
	text_label = []
	group_by_label = {}
	cnt = 0
	for id, row in enumerate(reader):
		if(id == 0):
			continue
		cnt += 1
		if(not (row[1] in group_by_label.keys())):
			group_by_label[row[1]] = []
		text = row[0]
		text = text.replace('\n', '')
		text = text.replace("  ", " ")
		group_by_label[row[1]].append([text, row[1]])
	
	print(group_by_label.keys())
	
	for key in group_by_label.keys():
		n = len(group_by_label[key])
		tmp = group_by_label[key]
		random.shuffle(tmp)
		datas["train"] += copy.deepcopy(tmp[:int(0.9 * n)])
		datas["test"] += copy.deepcopy(tmp[int(0.9 * n) :])
	a = len(datas["train"])
	b = 0
	c = len(datas["test"])
	print(f"total have {cnt}")
	print(f"sum of all dataset {a} + {b} + {c} = {a + b + c}")
	input_file.close()

for name in names:
	with open(f"./raw/{name}.csv", "w") as output_file:
		writer = csv.writer(output_file)
		writer.writerow(["text", "label"])
		for row in datas[name]:
			writer.writerow(row)
		output_file.close()

