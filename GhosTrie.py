# I originally solved this problem with an array of dictionaries.
# In that solution, array index i contained a dictionary of all words of length i.
# This worked really well and may even run a little faster than the trie data structure
# But the trie is a lot easier to deal with


class GhosTrieNode:
    def __init__(self, letter=""):
        self.letter = letter
        self.is_word = False
        self.is_win = False
        self.children = dict()

    def cascade_wins(self):
        self.is_win = True
        if self.is_word:
            self.is_win = False
            return self.is_win
        for child_node in self.children.values():
            if child_node.cascade_wins():
                self.is_win = False
        return self.is_win


class GhosTrie:
    def __init__(self):
        self.root = GhosTrieNode()

    def insert_word(self, word):
        current_node = self.root
        for char in word:
            if char not in current_node.children:
                current_node.children[char] = GhosTrieNode(char)
            current_node = current_node.children[char]
        current_node.is_word = True

    def find(self, word_fragment):
        current_node = self.root
        for char in word_fragment:
            if char not in current_node.children:
                return None
            current_node = current_node.children[char]
        return current_node

    def set_wins(self):
        current_node = self.root
        current_node.cascade_wins()
