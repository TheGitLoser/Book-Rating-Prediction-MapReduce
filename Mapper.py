import sys

def map():
    wordList = {}
    for line in sys.stdin:
        line = " ".join(line.split())     # remove duplicated space
        (docName, docWords) = line.split(" ", 1)
        docWords = docWords.split(" ")
        for word in docWords:
            if word not in wordList:
                wordList[word] = {}

            if docName in wordList[word]:
                wordList[word][docName] += 1
            else:
                wordList[word][docName] = 1

    for word in wordList:
        print(word, wordList[word], sep="-")

        
if __name__ == "__main__":
    map()