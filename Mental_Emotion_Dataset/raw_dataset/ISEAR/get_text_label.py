import csv


def get_raw():
	with open("./original/ISEAR.csv", "r") as input_file:
		with open("./original/raw.csv", "w") as output_file: 
			reader = csv.reader(input_file)
			writer = csv.writer(output_file)
			writer.writerow(["text", "label"])
			cnt = 0
			label_dict = {}
			for id, row in enumerate(reader):
				if(id == 0):
					continue
				writer.writerow([row[40], row[36]])
				if(not (row[36] in label_dict.keys())):
					label_dict[row[36]] = 0
				label_dict[row[36]] += 1
				cnt += 1
			print(label_dict)
			print(cnt)



if __name__ == "__main__":
	get_raw()
