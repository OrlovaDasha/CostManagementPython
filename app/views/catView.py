from app import app, db
from app.models.Goods import Goods


def levenstein(word, pattern, k):
    patternLen, wordLen = len(pattern), len(word)
    prevString = [x for x in range(patternLen + 1)]

    for i in range(1, wordLen+1):
        currentString = [i] + [None] * patternLen
        for j in range(1, patternLen + 1):
            if abs(i - j) <= k:
                if pattern[j-1] == word[i-1]:
                    currentString[j] = prevString[j-1]
                else:
                    insert = currentString[j-1] if currentString[j-1] is not None else 100
                    delete = prevString[j] if prevString[j] is not None else 100
                    change = prevString[j-1] if prevString[j-1] is not None else 100
                    currentString[j] = min(insert, delete, change) + 1
        prevString = currentString
    return prevString[patternLen]


def levenstein3(word, pattern, k):
    patternLen, wordLen = len(pattern), len(word)
    diffMat = [[x for x in range(patternLen + 1)]] + [[x + 1] + [None] * patternLen for x in range(wordLen)]

    for i in range(1, wordLen+1):
        for j in range(1, patternLen+1):
            if abs(i - j) <= k:
                insert = diffMat[i][j - 1] if diffMat[i][j - 1] is not None else 100
                delete = diffMat[i - 1][j] if diffMat[i - 1][j] is not None else 100
                change = diffMat[i - 1][j - 1] if diffMat[i - 1][j - 1] is not None else 100
                diff = 0 if pattern[j-1] == word[i-1] else 1
                diffMat[i][j] = min(insert + 1, delete + 1, change + diff)
    return diffMat[wordLen][patternLen]

@app.route('/categorise', methods=['GET', 'POST'])
def categorise():
    text = "ФОАпепьсинОтборный,кг"
    word = "апельсин"

    for i in range (0, len(text) - len(word)):
        if levenstein(text[i:len(word)].lower(), word, 3) <= 3:
            print(text[i:i+len(word)])
    return None
