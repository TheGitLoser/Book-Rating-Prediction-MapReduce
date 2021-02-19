import sys
import json


def reducer():
    wordList = {}   # {<word>: {<bookID>: <count of word in this.bookId>}}
    bookList = {}    # {<bookID>: {<word>: <count of word in this.bookId>}}

    # read mapper output
    for line in sys.stdin:
        (tempWord, tempBookList) = line.split("-", 1)
        if tempWord not in wordList:
            wordList[tempWord] = {}
        tempBookList = json.loads(tempBookList.replace("'", "\""))    # from string to dict
        for bookId in tempBookList:
            if bookId in wordList[tempWord]:
                wordList[tempWord][bookId] += tempBookList[bookId]
            else:
                wordList[tempWord][bookId] = tempBookList[bookId]
            if bookId in bookList:
                if (tempWord in bookList[bookId]):
                    bookList[bookId][tempWord] += tempBookList[bookId]
                else:
                    bookList[bookId][tempWord] = tempBookList[bookId]
            else:
                bookList[bookId] = {tempWord: tempBookList[bookId]}

    print("wordList = " , wordList, end="\n\n")
    print("bookList = " , bookList, end="\n\n")


    # compute TF
    maxTF = {}      # {<bookID>: <max(tf)>}
    tf = {}         # {<bookID>: {<word>: <tf>}}
    # for each bookId
    for bookId in bookList:
        # get max(tf)
        maxTF[bookId] = 0
        for word in bookList[bookId]:
            if bookList[bookId][word] > maxTF[bookId]:
                maxTF[bookId] = bookList[bookId][word]
        print(f'maxTF of bookId: {bookId} = {maxTF[bookId]}')
        
        tf[bookId] = {}
        # for each word
        for word in bookList[bookId]:
            tf[bookId][word] = bookList[bookId][word] / maxTF[bookId]
    
    print("tf = " , tf, end="\n\n")
    
    # compute IDF
    idf = {}        # {<word>: <idf>}
    import math
    # for each word
    totalNoOfbookId = len(bookList)
    for word in wordList:
        df = len(wordList[word])
        idf[word] = math.log2(totalNoOfbookId / df)
    
    print("idf = " , idf, end="\n\n")

    #output <bookID>-<word>-<df>-<idf>-<df-idf>
    for bookId in tf:
        for word in tf[bookId]:
            tempTF = tf[bookId][word]
            tempIDF = idf[word]
            tempTFIDF = tempTF * tempIDF
            print(bookId, word, tempTF, tempIDF, tempTFIDF, sep="-")

if __name__ == "__main__":
    reducer()