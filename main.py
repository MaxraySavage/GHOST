from datetime import datetime
startTime = datetime.now()
from string import ascii_letters
from string import upper
import random

#Depending on the mode there are one or two possible previous moves
def getPrecedingWords(word,mode):
    if mode == 'super':
        res=(word[0:len(word)-1],word[1:len(word)])
    else:
        res=(word[0:len(word)-1],'')
    return(res)

def buildData (wordFile):
    #logic for translate
    title_trans=''.join(chr(c) if chr(c).isupper() or chr(c).islower()else '_' for c in range(256))
    stateDict = {}
    wordSet = set()
    wordCount = 0
    for line in wordFile:
        line = line.translate(title_trans)
        line = line.partition('_')[0]
        
        line = upper(line)
        
        #Only count words with 3 or more letters
        lLength = len(line)
        if lLength >= 3:
            wordCount += 1
            wordSet.add(line)
            if lLength in stateDict:
                stateDict[lLength][line] = (line,True)
            else:
                stateDict[lLength] = {line: (line,True)}
    n = stateDict.keys()
    n.sort()
    n = n[-1]

    #Implement the trickle down method for finding possible game states and
    #Whether or not the current player wins from them

    while n >= 1:
        n = n-1
        if n-1 not in stateDict:
            stateDict[n-1] ={}
        currentTier = stateDict[n].values()
        for tState in currentTier:
            preds = getPrecedingWords(tState[0],'0')
            for word in preds:
                if word != '':
                    if word in stateDict[n-1]:
                        predState = stateDict[n-1][word]
                        stateDict[n-1][word] = (word, predState[1] or (not tState[1]))
                    else:
                        stateDict[n-1][word] = (word, (not tState[1]))
    secondPlayerLoses = False
    for vals in stateDict[1].values():
        secondPlayerLoses = secondPlayerLoses or (not vals[1])

    #An imaginary zero-th move that stores whether the first or second player loses
        
    stateDict[0][''] = ('', secondPlayerLoses)
    return (stateDict, wordCount, wordSet)


#Choose word list

wordFile = open("WORDS.txt")

#Contain words in a set

wordSet = set()

#Set up data structure to hold the list of game states.
#This dictionary will end up holding dictionaires

stateDict = {}

#It is nice to keep a wordCount for debugging

wordCount = 0

#Read lines from wordList into both the wordSet and stateDict
#stateDict becomes a dictionary of dictionaries with inner dictionaries containing n-length game states (just words for now)

(stateDict, wordCount, wordSet) = buildData(wordFile)

#Play the game.
def playGhost():
    gameState = ''

    playerFirst = raw_input("Do you want to go first (y/n)? ")
    userTurn = (playerFirst == 'y')
    gameOver = False
    userWin = False

    while not gameOver:
        if userTurn:
            nextChar = upper(raw_input("Type in a letter or HELP  "))
            while nextChar =="HELP":
                goodMoves = []
                badMoves = []
                for state in stateDict[len(gameState)+1].values():
                    word = state[0]
                    if word.startswith(gameState):
                        if state[1]:
                            badMoves.append(word[-1])
                        else:
                            goodMoves.append(word[-1])
                if len(goodMoves) > 0:
                    goodMoves = list(set(goodMoves))
                    print("Maybe one of these is good ")
                    print(goodMoves)
                else:
                    badMoves = list(set(badMoves))
                    print("Your funeral ")
                    print(badMoves)
                nextChar = upper(raw_input("Type in a letter  "))
            gameState = gameState + nextChar
            print("Current string is " + gameState)
            if gameState in wordSet:
                gameOver = True
                print(gameState + " is a word.")
                print("I WIN")
            elif gameState not in stateDict[len(gameState)]:
                gameOver = True
                print("Challenge. You can't make a word in the dictionary with " + gameState)
                print("I WIN")
            userTurn = False
        else:
            if stateDict[len(gameState)][gameState][1]:
                possibleSteps = stateDict[len(gameState)+1].values()
                found = False
                for nextState in possibleSteps:
                    if (nextState[0].startswith(gameState)) and (not nextState[1]):
                        print("My next move is " + nextState[0][-1])
                        gameState = nextState[0]
                        print("Current string is " + gameState)
                        break
            else:
                possibleSteps = stateDict[len(gameState)+1].values()
                random.shuffle(possibleSteps)
                found = False
                for nextState in possibleSteps:
                    if (nextState[0].startswith(gameState)):
                        print("My next move is " + nextState[0][-1])
                        gameState = nextState[0]
                        print("Current string is " + gameState)
                        break
                if gameState in wordSet:
                    print("ILOSEIGUESS")
                    gameOver = True
            userTurn = True




