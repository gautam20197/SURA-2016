import os
import re

TAG_RE = re.compile(r'<[^>]+>')
#function to remove xml tags from a string
def remove_tags(text):
    return TAG_RE.sub('', text)

path = "/Users/Apple/Desktop/SURA/duc2002/duc2002/data/test/summaries/duc2002extracts"
os.chdir(path)
#dataFile=open("200e",'r+')
#text = dataFile.read()
#text = remove_tags(text)
#dataFile.close()
#os.chdir("/Users/Apple/Desktop/SURA/Code/Summaries")
#targetFile = open("d082_200(2).txt","a")
#targetFile.write(text)
#targetFile.close()
allFolders = (os.listdir(path))
allFolders = [i for i in allFolders if(i[0]=='d')]
# Folders of all the documents
previous = 0

for i in allFolders:
	os.chdir(i)
	cwd = os.getcwd()
	allFiles = (os.listdir(cwd))
	for j in allFiles:
		if(j=="200e"):
			dataFile=open("200e",'r+')
			text = dataFile.read()
			text = remove_tags(text)
			dataFile.close()
			if(previous == int(i[2:4])):
				os.chdir("/Users/Apple/Desktop/SURA/Code/Summaries")
				targetFile = open(i[0:4]+"_200"+"(2)"+".txt","a")
				targetFile.write(text)
				targetFile.close()
			else:
				os.chdir("/Users/Apple/Desktop/SURA/Code/Summaries")
				targetFile = open(i[0:4]+"_200"+".txt","a")
				targetFile.write(text)
				targetFile.close()
			os.chdir(path)
			os.chdir(i)

		else:
			dataFile=open("400e",'r+')
			text = dataFile.read()
			text = remove_tags(text)
			dataFile.close()
			if(previous == int(i[2:4])):
				os.chdir("/Users/Apple/Desktop/SURA/Code/Summaries")
				targetFile = open(i[0:4]+"_400"+"(2)"+".txt","a")
				targetFile.write(text)
				targetFile.close()
			else:
				os.chdir("/Users/Apple/Desktop/SURA/Code/Summaries")
				targetFile = open(i[0:4]+"_400"+".txt","a")
				targetFile.write(text)
				targetFile.close()
			os.chdir(path)
			os.chdir(i)
	previous = int(i[2:4])
	os.chdir(path)


				


