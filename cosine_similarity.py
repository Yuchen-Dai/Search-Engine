# cosine similarity and duplicate detection implementation
import numpy
from pathlib import Path
from collections import defaultdict
from copy import deepcopy

similarityThreshold = 0.99 # customizable similarity threshold
debug = True # for debug print

def cosineSimilarity(dictX: dict, dictY: dict):
	"""
	Source code can be found on 
	www.biaodianfu.com/cosine-similarity.html
	"""
	listX = convertToVector(dictX)
	listY = convertToVector(dictY)
	vectorX = numpy.array(listX)
	vectorY = numpy.array(listY)
	dotProduct = numpy.dot(vectorX, vectorY)
	normalizedX = numpy.linalg.norm(vectorX)
	normalizedY = numpy.linalg.norm(vectorY)
	if normalizedX * normalizedY == 0:
		# print(dictX,"\n",dictY)
		# print(listX,"\n",listY)
		# print(vectorX,"\n", vectorY)
		# print(normalizedX, "\n", normalizedY)
		# print("cannot divide by 0")
		return -1
	return dotProduct / (normalizedX * normalizedY)

# print(f"cos sim for [1,1,1] and [1,1,1] = {cosineSimilarity([1,1,1], [1,1,1])}\tshould be 1")
# print(f"cos sim for [1,0,1] and [0,1,0] = {cosineSimilarity([1,0,1], [0,1,0])}\tshould be 0")

def readText(file) -> list:
	with file.open() as f:
		url = f.readline()
		text = list(map(lambda x: x.rstrip(), f.readlines()))
		# if(len(text) == 0):
		# 	print(f"{url} is empty!!")
	return text

def calculateTermFreq(tokenList: list) -> dict:

	termFreqDict = defaultdict(int)
	for token in tokenList:
		termFreqDict[token] += 1
	return termFreqDict

def convertToVector(tokenDict: dict) -> list:

	rawVector = sorted(tokenDict.items())
	tokenVector = [x[1] for x in rawVector] # only preserve the frequency values
	return tokenVector

def addMissingTerms(tokenDictX: dict, tokenDictY: dict) -> (dict, dict):

	for key in tokenDictX.keys():
		if not (key in tokenDictY):
			tokenDictY[key] = 0

	for key in tokenDictY.keys():
		if not (key in tokenDictX):
			tokenDictX[key] = 0

	return (tokenDictX, tokenDictY) 

def queryDocSimiliarity(query: [str], fileName: str) -> float:
	queryDict = calculateTermFreq(query)
	tokenList = readText(Path(fileName))
	tokenDict = calculateTermFreq(tokenList)
	queryDict, tokenDict = addMissingTerms(queryDict, tokenDict)
	score = cosineSimilarity(queryDict, tokenDict)
	# print(score)
	return score

def duplicateCheck(allFiles) -> list:

	global similarityThreshold
	# allFiles = iterdir(Path("op"))
	fileList = list(allFiles)
	dupeList = list()
	emptyList = list()
	count = 0

	x = 0
	while(x != len(fileList)):

		fileX = fileList[x]
		y = x + 1

		tokenListX = readText(fileX)
		if len(tokenListX) == 0:
			if debug: print(f"remove {fileX.name}, current x: {x}")
			fileList.remove(fileX)
			emptyList.append(fileX)
			continue

		while(y != len(fileList)): 
			if fileList[x] != fileList[y]:
				fileY = fileList[y]
				tokenListX = readText(fileX)
				tokenListY = readText(fileY)

				if len(tokenListY) == 0:
					if debug: print(f"remove {fileY.name}, current y: {y}")
					fileList.remove(fileY)
					emptyList.append(fileY)
					continue

				tokenDictX = calculateTermFreq(tokenListX)
				tokenDictY = calculateTermFreq(tokenListY)
				tokenDictX, tokenDictY = addMissingTerms(tokenDictX, tokenDictY)
				score = cosineSimilarity(tokenDictX, tokenDictY)
				
				if debug:
					# print(f"{fileX.name} compare to {fileY.name}\nScore is {score}")
					if count % 1000 == 0: print(f"current count: {count}")
					# print(count)
					count+= 1
				
				if (score >= similarityThreshold):
					if debug: print(f"remove {fileY.name}, current y: {y}")
					fileList.remove(fileY)
					dupeList.append(fileY)
					y -= 1
			# end if !=
			y += 1
		# end inner while
		x += 1
	# end outer while
	print(dupeList)
	return fileList

if __name__ == '__main__':
	testFolder = Path("C:\\Users\\hower\\Documents\\CS 121\\project3\\testFolder")
	outputFolder = Path("C:\\Users\\hower\\Documents\\CS 121\\project3\\op")
	noDupeList = duplicateCheck(outputFolder.iterdir())
	print(noDupeList)
	with open("C:\\Users\\hower\\Documents\\CS 121\\project3\\noDupeList.txt", 'w') as f:
		for filePath in noDupeList:
			f.write(filePath.name)
	# if debug: print(fileList)

	# score = queryDocSimiliarity(["fuck"],"C:\\Users\\hower\\Documents\\CS 121\\project3\\op\\10237.txt")

	# query = ["comput"]
	# result = []
	# for file in outputFolder.iterdir():
	# 	# print(file.name)
	# 	score = queryDocSimiliarity(query, file)
	# 	if score == -1:
	# 		print(f"doc id {file.name} is empty")
	# 	result.append(score)
	# print(result)



