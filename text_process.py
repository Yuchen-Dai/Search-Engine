import json
import bs4
from pathlib import Path
import porter_stemmer as ps

def extract_text(file_name:str) -> str:
    text = open(file_name).readline()
    text = json.loads(text)
    soup = bs4.BeautifulSoup(text['content'], "html5lib")
    for script in soup.find_all(["script", "style"]):
        script.extract()
    return soup.get_text(), text['url']

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

def write(file_path, content, url):
    file = open(file_path,'w')
    file.write(url+'\n')
    for word in content:
        file.write(word+'\n')
    file.close()

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
    count = 1
    save_path ='op/'
    for p in Path('DEV').iterdir():
        for f in p.iterdir():
            if str(f).split('.')[-1] == 'json':
                text, url = extract_text(f)
                tokens = tokenized(text)
                tokens = stemmer(tokens)
                write(save_path+str(count)+'.txt', tokens, url)
                count += 1



