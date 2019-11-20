import pickle
import time
import porter_stemmer as ps
from collections import defaultdict

def load_data():
	with open('inverted_index.pkl', 'rb') as f:
		inverted_index = pickle.load(f)
	return inverted_index


class data_base:
	def __init__(self):
		self.inverted_index = load_data()
		self.myStemmer = ps.PorterStemmer()

	def ask(self, query) -> 'set of doc id':
		t = time.time()

				
		querys = query.split()
		answer = []
		score_dict = defaultdict(float)
		for q in querys:
			q = q.lower()
			q = self.myStemmer.stem(q, 0, len(q)-1)
			if q in self.inverted_index:
				doc = self.inverted_index[q]
				answer.append({i[0] for i in sorted(doc, key = lambda x: x[1], reverse = True)})
				for i in doc:
					score_dict[i[0]] += i[1]
		if not len(answer):
			return
		result = answer[0]
		for a in answer[1:]:
			result = result & a

		print(time.time() - t)
		key = sorted(result, key = lambda x: score_dict[x], reverse = True)[:10]
		result = []
		for i in key:
			with open(f'op/{i}.txt') as f:
				result.append(f.readline().rstrip())
		return result

if __name__ == '__main__':
	print('Loading data.')
	data = data_base()
	print('Success.')
	
