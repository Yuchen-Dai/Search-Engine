import json, bs4, pathlib, hashlib
# IMPORTANT: THIS FILE IS ABANDONED

def compare_html(fileAString, fileBString) -> bool:

	soupA = bs4.BeautifulSoup(fileAString, "lxml")
	fileAtxt = soupA.get_text()
	soupB = bs4.BeautifulSoup(fileBString, "lxml")
	fileBtxt = soupB.get_text()
	# you can change the hashing function to whatever you want
	filaAHash = hashlib.sha1(str.encode(fileAtxt))
	fileBHash = hashlib.sha1(str.encode(fileBtxt))
	# print(filaAHash, fileBHash) 
	return filaAHash == fileBHash

def openFile(filePath: pathlib.Path) -> str:

	with open(filePath) as file:
		# we want the html content in the json file
		webpageString = json.loads(file.read())["content"]
	return webpageString

def main():
	# file path change to whatever you want
	fileCompPath = pathlib.Path("C:\\Users\\hower\\Documents\\CS 121\\project3\\developer\\DEV")
	DEVDirList = [p for p in fileCompPath.iterdir()]
	allFileList = []
	fileCount = 0
	for path in DEVDirList:
		for p in path.iterdir():
			allFileList.append(p)
			fileCount += 1
			if fileCount % 10000 == 0:
				print(f"processed file count = {fileCount}")
	print(f"total file count = {fileCount}")
	noDuplicateList = allFileList
	# compare file and remove duplicate file
	for fileA in allFileList:
		for fileB in allFileList:
			if fileA != fileB:
				fileAString = openFile(fileA)
				fileBString = openFile(fileB)
				if compare_html(fileAString, fileBString) == True:
					noDuplicateList.remove(fileB)
	# print all files to shell
	for file in allFileList:
		print(file.name, end = '\t')
		if file not in noDuplicateList:
			print("REMOVED", end = '')
		print()

if __name__ == '__main__':
	main()