import json
import bs4
from pathlib import Path
import porter_stemmer as ps
import pickle

def extract_title(file_name:str) -> str:
    text = open(file_name).readline()
    text = json.loads(text)
    soup = bs4.BeautifulSoup(text['content'], "html5lib")
    return soup.title, text['url']

def tokenized(text)-> list:
    result = []
    word=''
    for c in text:
        if c.isascii() and (c.isdigit() or c.isalpha()):
            word += c.lower()
        else:
            if word != '':
                result.append(word)
                word = ''
    if word != '':
        result.append(word)
    return result

def stemmer(wordList: [str]) -> [str]:
    '''
    This stemmer takes a list of token and convert all tokens in the list to its stemmed form
    This stemmer uses Porter Stemmer.
    The source code can be found on https://tartarus.org/martin/PorterStemmer/
    '''
    myStemmer = ps.PorterStemmer()
    stemmedWordList = []
    for word in wordList:
        if(word.isalpha()):# if word is an English word (contains only alphabets)
            word = myStemmer.stem(word, 0, len(word)-1)
        stemmedWordList.append(word)
    return stemmedWordList

if __name__ == "__main__":
    check_dict = {}
    for p in Path('op').iterdir():
        f = open(p, 'r')


    save_path ='title/'
    title_dict = {}
    for p in Path('DEV').iterdir():
        for f in p.iterdir():
            if str(f).split('.')[-1] == 'json':
                text, url= extract_title(f)
                tokens = tokenized(text)
                for t in tokens:
                    token = stemmer(t)
                    if token not in title_dict:
                        title_dict[token] = [url]
                    else:
                        title_dict.append(url)

    for key, item in title_dict.items():
        to_save = open(save_path+key+'.pickle', 'wb')
        pickle.dump(item, to_save)









