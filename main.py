import re
from GhosTrie import GhosTrie
import GhostGame

game_trie = GhosTrie()
file1 = open('GhostWordlist.txt', 'r')
while True:
  nextWord = file1.readline()
  if not nextWord:
    break
  nextWord = re.sub("[^A-Z]+", "", nextWord)
  game_trie.insert_word(nextWord)

game_trie.set_wins()

GhostGame.play_ghost(game_trie)