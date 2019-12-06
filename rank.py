import pickle
#private

def match(query:[str], page:str, loc_dict:[dict]):
    index = []
    prev = -1
    for q in range(len(query)):
        found = False
        for i in loc_dict[q][page]:
            if i> prev:
                prev = i 
                index.append(i)
                found = True
        if found == False:
            index.append(-1)
    return index

def cal_score(query:[str], page:str, dicts):
    index = match(query, page, dicts)
    count = 0
    while -1 in index:
        index.remove(-1)
        count += 1
    distance = 0
    indi = False
    for i in range(len(index)):
        if i+1< len(index):
            indi = True
            distance += index[i+1] - index[i]

    if indi == False:
        distance = 9223372036854775807
    return distance, count, sum(index)


def bag(query:[str], pages:[str]):
    dicts = []
    for w in query:
        to_read = open('/home/fanfanwu9898/developer/post/' + w + '.pickle', 'rb')
        dicts.append(pickle.load(to_read))
        to_read.close()

    distances = {}
    counts = {}
    location = {}

    for p in pages:
        scores = cal_score(query, p, dicts)
        distances[p] = scores[0]
        counts[p] = scores[1]
        location[p] = scores[2]

    return distances, counts, location
