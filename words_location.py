import pickle
from pathlib import Path

index = {}
for p in Path("op").iterdir():
    f = open(p, 'r')
    p_name = str(p).split("/")[-1][:-4]
    f.readline()
    count = 0
    for l in f.readlines():
        if l.strip() not in index:
            index[l.strip()] = {p_name:[count]}
        else:
            if p_name not in index[l.strip()]:
                index[l.strip()][p_name] = [count]
            else:
                index[l.strip()][p_name].append(count)
        count += 1
    f.close()

for key, value in index.items():
    if len(key) < 254:
        to_save = open("post/"+key+".pickle", 'wb')
        pickle.dump(value, to_save)
        to_save.close()
    else:
        print(key, value)

