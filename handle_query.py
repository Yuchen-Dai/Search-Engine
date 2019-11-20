import pickle
import time

def load_data():
	with open('inverted_index.pkl', 'rb') as f:
		inverted_index = pickle.load(f)
	return inverted_index


class data_base:
	def __init__(self):
		self.inverted_index = load_data()

	def ask(self, query) -> 'set of doc id':
		t = time.time()

				
		querys = query.split()
		answer = []
		for q in querys:
			q = q.lower()
			if q in self.inverted_index:
				doc = self.inverted_index[q]
				answer.append({i[0] for i in sorted(doc, key = lambda x: x[1], reverse = True)})
		if not len(answer):
			return
		result = answer[0]
		for a in answer[1:]:
			result = result & a

	 
		return result

if __name__ == '__main__':
	print('Loading data.')
	data = data_base()
	print('Success.')
	print(len(data.ask('ACM')))
