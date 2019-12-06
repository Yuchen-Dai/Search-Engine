import pickle
import time
import porter_stemmer as ps
from collections import defaultdict
from rank import *


def load_data():
	with open('inverted_index/token_dict.pkl', 'rb') as f:
		inverted_index = pickle.load(f)
	return inverted_index


class data_base:
	def __init__(self):
		self.inverted_index = load_data()
		self.myStemmer = ps.PorterStemmer()

	def get_list(self, q):
		number = self.inverted_index[q]
		file_number = int(number/1000)
		address = f'inverted_index/inverted_index{file_number}.data'
		with open(address, 'r') as f:
			for i in range(number - 1000*file_number + 1):
				line = f.readline()

		line = line.rstrip().split()[1:]
		result = []

		for i in range(int(len(line)/2)):
			result.append([line[2*i],line[2*i+1]])
		return result

	def ask(self, query) -> 'set of doc id':
		t = time.time()

				
		querys = query.split()
		answer = []
		score_dict = defaultdict(float)
		for i in range(len(querys)):
			q = querys[i].lower()
			querys[i] = self.myStemmer.stem(q, 0, len(q) - 1)

		for q in querys:
			if q in self.inverted_index:
				doc = self.get_list(q)
				answer.append({i[0] for i in sorted(doc, key = lambda x: x[1], reverse = True)})
				for i in doc:
					score_dict[i[0]] += float(i[1])
		if not len(answer):
			return []
		result = answer[0]
		for a in answer[1:]:
			result = result & a
		final_score = defaultdict(float)
		distances = {}
		counts = {}

		result = sorted(result, key = lambda x: score_dict[x], reverse = True)

		distances, counts, locations = bag(querys, result)


		for score, f in enumerate(sorted(distances, key = lambda x: distances[x], reverse = True)):
			final_score[f] += score**2

		for score, f in enumerate(sorted(counts, key = lambda x: counts[x], reverse = True)):
			final_score[f] += score**2

		# for score, f in enumerate(sorted(locations, key = lambda x: locations[x], reverse = True)):
		# 	final_score[f] += score**2

		for score, f in enumerate(sorted(result, key = lambda x: score_dict[x])):
			final_score[f] += score**2

		key = sorted(final_score, key = lambda x: final_score[x], reverse = True)[:10]
		result = []
		for i in key:
			with open(f'op/{i}.txt') as f:
				result.append(f.readline().rstrip())
		print(time.time() - t)
		return result

if __name__ == '__main__':
	print('Loading data.')
	data = data_base()
	print('Success.')
	data.ask('fuck')