
class NodeConfig:
    def __init__(self):
        pass




class Trie:
 
    def __init__(self):
        """
            Initialize
        """
        self.root = {}
        self.end = ()
        self.node_config = ()
 
    def insert(self, rule):
        curNode = self.root
        for c in word:
            if not c in curNode:
                curNode[c] = {}
            curNode = curNode[c]
          
        curNode[self.word_end] = True
 
    def search(self, word):
        curNode = self.root
        for c in word:
            if not c in curNode:
                return False
            curNode = curNode[c]
            
        if self.word_end not in curNode:
            return False
        
        return True
 
    def startsWith(self, prefix):
        curNode = self.root
        for c in prefix:
            if not c in curNode:
                return False
            curNode = curNode[c]
        
        return True
