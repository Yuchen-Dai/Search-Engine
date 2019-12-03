# cosine similarity and duplicate detection implementation
import numpy
from pathlib import Path
from collections import defaultdict
from copy import deepcopy

similarityThreshold = 0.99 # customizable similarity threshold
debug = False

def cosineSimilarity(dictX: dict, dictY: dict):
	"""
	Source code can be seen on 
	www.biaodianfu.com/cosine-similarity.html
	"""
	listX = convertToVector(dictX)
	listY = convertToVector(dictY)
	vectorX = numpy.array(listX)
	vectorY = numpy.array(listY)
	dotProduct = numpy.dot(vectorX, vectorY)
	normalizedX = numpy.linalg.norm(vectorX)
	normalizedY = numpy.linalg.norm(vectorY)
	return dotProduct / (normalizedX * normalizedY)

# print(f"cos sim for [1,1,1] and [1,1,1] = {cosineSimilarity([1,1,1], [1,1,1])}\tshould be 1")
# print(f"cos sim for [1,0,1] and [0,1,0] = {cosineSimilarity([1,0,1], [0,1,0])}\tshould be 0")

def readText(file) -> str:
	with file.open() as f:
		url = f.readline()
		text = list(map(lambda x: x.rstrip(), f.readlines()))
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
		if not key in tokenDictY:
			tokenDictY[key] = 0

	for key in tokenDictY.keys():
		if not key in tokenDictX:
			tokenDictX[key] = 0

	return (tokenDictX, tokenDictY) 

def duplicateCheck(allFiles) -> list:

	global similarityThreshold
	# allFiles = iterdir(Path("op"))
	fileList = list(allFiles)

	x = 0
	while(x != len(fileList)):

		fileX = fileList[x]
		y = x + 1
		while(y != len(fileList)): 

			fileY = fileList[y]
			tokenListX = readText(fileX)
			tokenListY = readText(fileY)
			tokenDictX = calculateTermFreq(tokenListX)
			tokenDictY = calculateTermFreq(tokenListY)
			tokenDictX, tokenDictY = addMissingTerms(tokenDictX, tokenDictY)
			score = cosineSimilarity(tokenDictX, tokenDictY)
			
			if debug:
				print(f"{fileX.name} compare to {fileY.name}\nScore is {score}")
			
			if (score >= similarityThreshold):
				if debug: print(f"remove {fileY.name}, current y: {y}")
				fileList.remove(fileY)
				y -= 1
			# end if
			y += 1
		# end inner while
		x += 1
	# end outer while

	return fileList

if __name__ == '__main__':
	testFolder = "C:\\Users\\hower\\Documents\\CS 121\\project3\\testFolder"
	outputFolder = "C:\\Users\\hower\\Documents\\CS 121\\project3\\op"
	fileList = duplicateCheck(Path(testFolder).iterdir())
	if debug: print(fileList)






