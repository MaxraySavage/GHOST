import re

"""
The goal of this script is to take a line separated list of words in a text file
and trim out all the words that are not reachable in a game of ghost.
You could do this trimming as you set up the game.
However, I've found that, as I'm testing the game build,
I very much appreciate removing 80% of the words in advance. 

Reachability here means that the word in question could actually be an end game state in a game of ghost.

Example of an unreachable word is the word SUPERB.
SUPERB is a word and would be included in most dictionaries.
However, in a game of GHOST, the game would end when you got to SUPER.
So you can never actually use the fact that SUPERB is a word.
So we can safely remove it from the word list.

To my surprise, this condition cuts the wordlist down by a huge amount.
"""

file1 = open('Collins Scrabble Words (2019).txt', 'r')
file2 = open('GhostWordlist.txt', 'w')

minWordLength = 4


# Lets pull the list of words into a set
# This will get rid of any duplicates for us 
# AND make the next step of determining which words are actually reachable somewhat faster


words = set()

while True:
    nextWord = file1.readline()
    # Stop if we're at the end of the file
    if not nextWord:
        break
    nextWord = nextWord.upper()
    # SUB out any non letters
    nextWord = re.sub("[^A-Z]+", "", nextWord)
    if len(nextWord) >= minWordLength:
        words.add(nextWord)

   
# If there any words that have substrings that are over the minimum length, 
# Those words are never actually reachable in game so let's get rid of them
# To my surprise this actually cuts down the size of the wordlist by about a factor of 5
# A reminder that english words are incredibly sparse in the space of all possible combinations of letters
# If the word is reachable, add it to a new list of reachable words
# Also I'm doing this because apparently you can't change the elements of a set while iterating over it.
# At least not without weird stuff happening.


wordList = list()

for word in words:
    # Minimum length words are by definition reachable
    if len(word) == minWordLength:
        wordList.append(word)
        continue
    # word is still reachable unless proven otherwise
    reachableWord = True
    # Iterate over all substrings that are longer than min word length
    for i in range(minWordLength, len(word)):
        wordSubstring = word[0:i]
        if wordSubstring in words:
            reachableWord = False
            break
    if reachableWord:
        wordList.append(word)


# Now we can write out our sorted list to a file
for word in wordList:
    word = word + "\n"
    file2.write(word)
