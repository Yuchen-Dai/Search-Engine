from pathlib import Path
from collections import defaultdict
import pickle
import math

def append_inverted(stem, token_list, result):
	tf_raw = defaultdict(int)
	count = len(token_list)
	for token in token_list:
		tf_raw[token] += 1
	for token, c in tf_raw.items():
		result[token].append({'stem':stem,'tf': c/count})


def read_path(path):
	p = Path(path)
	return Path.iterdir(p)

def read_text(file):
	with file.open() as f:
		url = f.readline()
		text = list(map(lambda x: x.rstrip(), f.readlines()))
	return text

def calc_tf_idf(result, total_file):
	for token in result:
		count_token = len(result[token])
		idf = math.log(total_file/(count_token + 1))
		for document in result[token]:
			document['tf'] =  document['tf'] * idf

def main():
	result = defaultdict(list)
	#path of the source file
	path = 'op'
	files = read_path(path)
	
	total_file = 0
	for f in files:
		total_file += 1
		if total_file %1000 == 0 :
			print(total_file)
		token_list = read_text(f)
		append_inverted(f.stem, token_list, result)

	calc_tf_idf(result, total_file)
	print(f'Number Docs: {total_file}')
	print(f'Unique Words: {len(result)}')
	with open('inverted_index.pkl', 'wb') as f:
		pickle.dump(result, f, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
	main()
