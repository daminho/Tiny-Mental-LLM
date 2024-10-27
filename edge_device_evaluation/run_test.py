import ollama
import csv
import random
from tqdm import tqdm
import argparse
import time
import os
from datetime import datetime
import json

root = ""
data = os.path.join(root, "data.csv")
logs_dir = os.path.join(root, "logs")

if root == "":
	raise Exception("Path to root folder not found!!!!")


"""
Response template
{
	"model": model name,
	"created_at": timestamp,
	"response": string,
	"done": boolean,
	"done_reason": string,
	"context": array of tokens,
	"total_duration": nano second,
	"load_duration": nano second,
	"prompt_eval_count": prompt token count,
	"prompt_eval_duration": nano second,
	"eval_count": generated token count,
	"eval_duration: nano second
}
"""


def do_benchmark(args):
	NUM_ITERATION = args.num_iteration
	NUM_TURN = args.num_turn
	SLEEP_TIME = args.sleep_time
	log_file_name = os.path.join(logs_dir, args.model +  "_" +  str(args.num_turn) + "_" + str(args.num_iteration) + "_" + "{:%H_%M_%S_%B_%d_%Y}".format(datetime.now()) + ".json")
	with open(log_file_name, "w") as json_output_file:
		print("Writing logs to ", log_file_name)
		logs = []
		with open(data, "r") as data_file:
			reader = csv.reader(data_file)
			texts = [text[0] for text in reader]
			for turn in range(NUM_TURN):
				print("Evaluating Turn {}".format(turn +1))
				random.shuffle(texts)
				_sum_total_duration = 0
				_sum_load_duration = 0
				_sum_prompt_eval_duration = 0
				_sum_eval_duration = 0
				_sum_prompt_eval_count = 0
				_sum_eval_count = 0
				sub_texts = texts[:NUM_ITERATION]
				for text in tqdm(sub_texts):
					response = ollama.generate(model = args.model, prompt = text)
					_sum_total_duration += response["total_duration"] / 1000000
					_sum_load_duration += response["load_duration"] / 1000000
					_sum_prompt_eval_duration += response["prompt_eval_duration"] / 1000000
					_sum_eval_duration += response["eval_duration"] / 1000000
					_sum_prompt_eval_count += response["prompt_eval_count"]
					_sum_eval_count += response["eval_count"]
				_sum_total_duration /= NUM_ITERATION
				_sum_load_duration /= NUM_ITERATION
				_sum_prompt_eval_duration /= NUM_ITERATION
				_sum_eval_duration /= NUM_ITERATION
				_sum_prompt_eval_count /= NUM_ITERATION
				_sum_eval_count /= NUM_ITERATION
				logs.append({str(turn + 1): { \
					"avg_total_duration": _sum_total_duration,\
					"avg_load_duration": _sum_load_duration,\
					"avg_prompt_eval_duration": _sum_prompt_eval_duration,\
					"avg_eval_duration": _sum_eval_duration,\
					"avg_prompt_eval_token": _sum_prompt_eval_count,\
					"avg_eval_token": _sum_eval_count}})
				print("Average for {} runs:".format(NUM_ITERATION))
				print("Avg total duration: {}s".format(_sum_total_duration / 1000))
				print("Avg load duration: {}s".format(_sum_load_duration / 1000))
				print("Avg prompt eval duration: {}s".format(_sum_prompt_eval_duration / 1000))
				print("Avg eval duration: {}s".format(_sum_eval_duration / 1000 ))
				print("Avg prompt eval token count: {} token(s)".format(_sum_prompt_eval_count))
				print("Avg eval token count: {} token(s)".format(_sum_eval_count))
				print("Avg prompt eval token rate: {}token/s".format(_sum_prompt_eval_count/(_sum_prompt_eval_duration / 1000)))
				print("Avg eval token rate: {}token/s".format(_sum_eval_count/(_sum_eval_duration / 1000)))
				if(turn != NUM_TURN - 1):
					time.sleep(SLEEP_TIME * 60)
			data_file.close()
		# print(logs)
		_logs = logs[0]['1']
		for id,log in enumerate(logs):
			if(id == 0):
				continue
			for k in _logs.keys():
				_logs[k] += logs[id][str(id + 1)][k]
		print("After {} turns of {} iterations".format(args.num_turn, args.num_iteration))
		print("Avg total duration: {}ms".format(_logs["avg_total_duration"] / (args.num_turn * 1000)))
		print("Avg load duration: {}ms".format(_logs["avg_load_duration"] / (args.num_turn * 1000)))
		print("Avg prompt eval duration: {}s".format(_logs["avg_prompt_eval_duration"] / (args.num_turn * 1000)))
		print("Avg eval duration: {}s".format(_logs["avg_eval_duration"] / (args.num_turn * 1000)))
		print("Avg prompt eval token count: {} token(s)".format(_logs["avg_prompt_eval_token"] / args.num_turn))
		print("Avg eval token count: {} token(s)".format(_logs["avg_eval_token"] / args.num_turn))
		print("Avg prompt eval token rate: {}token/s".format(_logs["avg_prompt_eval_token"] / (_logs["avg_prompt_eval_duration"] / 1000)))
		print("Avg eval token rate: {}token/s".format(_logs["avg_eval_token"]/(_logs["avg_eval_duration"] / 1000)))

		for k in _logs.keys():
			_logs[k] /= args.num_turn

		json.dump({"model": args.model, "num_iteration": args.num_iteration, "num_turns": args.num_turn, "logs_avg": _logs, "logs_detail": logs}, json_output_file)
		json_output_file.close()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(
                    prog='ROLLAMA',
                    description='Testing OLLAMA efficiency on Raspberry Pi',
                    epilog='Author: Hoangdz')
	parser.add_argument('-m', '--model', default = 'qwen2:0.5b', help = "Name of model")
	parser.add_argument('-nt', '--num-turn', type = int, default = 1, help = "Number of times runing benchmark")
	parser.add_argument('-ni', '--num-iteration', type = int, default = 50, help = "Number of testing iterations per benchmark")
	parser.add_argument('-st', '--sleep-time', type = int, default = 15, help = "Number of minutes the code sleep between turn")
	args = parser.parse_args()
	do_benchmark(args)
