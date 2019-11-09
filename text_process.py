import json
import bs4
from pathlib import Path

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

if __name__ == "__main__":
    count = 1
    save_path ='/home/fanfanwu9898/Downloads/developer/tokenized/'
    for p in Path('/home/fanfanwu9898/Downloads/developer/DEV').iterdir():
        for f in p.iterdir():
            if str(f).split('.')[-1] == 'json':
                text, url = extract_text(f)
                tokens = tokenized(text)
                write(save_path+str(count)+'.txt', tokens, url)
                count += 1



