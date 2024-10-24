import csv

names = ["DR", "Dreaddit", "DepSeverity", "SDCNL", "ISEAR"]
datasets = ["train", "test"]

    

for dataset in datasets:
    text_label = []
    label_dict = dict()
    for name in names:
        with open(f"./prompted_dataset/{name}/{dataset}.csv", "r") as input_file:
            reader = csv.reader(input_file)
            for id, row in enumerate(reader):
                if(id == 0):
                    continue
                prompted_text = row[0]
                label = row[1]
                if(not (label in label_dict.keys())):
                    label_dict[label] = 0
                label_dict[label] += 1
                text_label.append([prompted_text, label])
        input_file.close()
    with open(f"./final_merged_dataset/{dataset}.csv", "w") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["text-prompted", "label"])
        for row in text_label:
            writer.writerow(row)
