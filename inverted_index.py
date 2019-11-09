from pathlib import Path
from collection import defaultdict
import pandas as pd
import math

def append_inverted(url, token_list, result):
	tf_raw = defaultdict(int)
	count = len(token_list)
	for token in token_list:
		tf_raw[token] += 1
	for token, c in tf_raw.items():
		result[token].append({'url':url,'tf': c/count,'idf': None,'tf-idf':None})


def read_path(path):
	p = Path(path)
	return Path.iterdir(p)

def read_text(file):
	with Path.open() as f:
		url = f.readline()

	return url

def calc_tf_idf(result, total_file):
	for token in result:
		count_token = len(result[token])
		idf = math.log(total_file/(count_token + 1))
		for document in result[token]:
			document['idf'] = idf
			document['tf_idf'] =  document['tf'] * idf

def main():
	result = defaultdict{list}
	#path of the source file
	path = ''
	files = read_path(path)
	
	total_file = 0
	for f in files:
		total_file += 1
		url, token_list = read_text(f)
		append_inverted(url, token_list, result)

	calc_tf_idf(result, total_file)
	df = pd.DataFrame(result,index=[0])
	df.to_csv('op.csv')

if __name__ == "__main__":
	main()