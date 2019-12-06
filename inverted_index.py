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
		result[token].append([stem,1+math.log(c/count)])


def read_path(path):
	p = Path(path)
	return Path.iterdir(p)

def read_text(file):
	with file.open() as f:
		url = f.readline()
		text = list(map(lambda x: x.rstrip(), f.readlines()))
	return text

def calc_tf_idf(result, total_file):
	#cal for all token in result
	for token in result:
		count_token = len(result[token])
		idf = math.log(total_file/(count_token))
		for document in result[token]:
			document[1] =  document[1] * idf

def dump_file(result,file_number):
	with open(f'/home/fanfanwu9898/developer/inverted_index/{file_number}.temp', 'w') as f:
		for token in sorted(result):
			f.write(f'{token} ')
			for token in result[token]:
				f.write(f'{token[0]} {round(token[1], 2)} ')
			f.write('\n')


def merge(temp_count):
	temp_file = [] 
	temp_line = []
	token_dict = {}
	#load each file
	for i in range(temp_count):
		temp_file.append(open(f'/home/fanfanwu9898/developer/inverted_index/{i + 1}.temp', 'r'))
	for f in temp_file:
		temp_line.append(f.readline())

	#merge
	count = 0
	while len(temp_line):
		if count % 1000 == 0:
			inverted_index = open(f'/home/fanfanwu9898/developer/inverted_index/inverted_index{int(count/1000)}.data','w')
		token = min([i.split()[0] for i in temp_line])
		token_dict[token] = count
		count += 1
		inverted_index.write(f'{token} ')
		length = len(temp_line)
		f = 0
		while f < length:
			if temp_line[f].split()[0] == token:
				inverted_index.write(temp_line[f][len(token) + 1:-1])
				line = temp_file[f].readline()
				if line == '':
					temp_file[f].close()
					del temp_file[f]
					del temp_line[f]
					length -= 1
				else:
					temp_line[f] = line
			f += 1
		inverted_index.write('\n')
	with open('/home/fanfanwu9898/developer/inverted_index/token_dict.pkl', 'wb') as f:
		pickle.dump(token_dict, f, pickle.HIGHEST_PROTOCOL)


def main():
	result = defaultdict(list)
	#path of the source file
	path = '/home/fanfanwu9898/developer/op'
	files = read_path(path)
	
	total_file = 0
	for f in files:
		total_file += 1
		if total_file %1000 == 0 :
			print(total_file)
		token_list = read_text(f)
		append_inverted(f.stem, token_list, result)

		#dump to file each reading of 20000 files.
		if total_file % 20000 == 0:
			dump_file(result, int(total_file/20000))
			result = defaultdict(list)

	dump_file(result, int(total_file/20000) + 1)

	temp_count = int(total_file/20000) + 1
	merge(temp_count)


	print(f'Number Docs: {total_file}')
	# print(f'Unique Words: {len(result)}')


if __name__ == "__main__":
	main()
