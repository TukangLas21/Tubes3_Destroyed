# Aho-Corasick (AC) Algoritm for Pattern Matching

import collections
# Membuat Trie semua pola yang ingin dicari
class Node: 
    def __init__(self):
        self.children = {}
        self.failureLink = None
        self.outputs = set()
    def hasChildren(self, key):
        return key in self.children
    def getChildren(self, key):
        return self.children.get(key)
    def setChildren(self, key, nodeObj):
        self.children[key] = nodeObj
    def addOutput(self, output):
        self.outputs.add(output)
    def copyOutputs(self, otherNode):
        for outputItem in otherNode.outputs:
            self.outputs.add(outputItem)

# AC Algorithm untuk mencari pola dalam string text
class AhoCorasick:
    def __init__(self, patterns):

        # Membuat Trie
        self.root = Node()
        for pattern in patterns:
            currNode = self.root
            for char in range(len(pattern)):
                key = pattern[char]
                if not currNode.hasChildren(key):
                    currNode.setChildren(key, Node())
                currNode = currNode.getChildren(key)
            currNode.addOutput(pattern)
        
        # Membuat failure link
        self.root.failureLink = self.root
        queue = collections.deque()
        for key, childNode in self.root.children.items():
            childNode.failureLink = self.root
            queue.append(childNode)
        while queue:
            currNode = queue.popleft()    
            for key, childNode in currNode.children.items():
                queue.append(childNode)
                n = currNode.failureLink
                while not n.hasChildren(key) and n is not self.root:
                    n = n.failureLink
                    potentialFailureLink = n.getChildren(key)
                    if potentialFailureLink:
                        childNode.failureLink = potentialFailureLink
                    else:
                        childNode.failureLink = self.root
                    childNode.copyOutputs(childNode.failureLink)
        
    # Mencari pola
    def search(self, text):
        found = []
        state = self.root
        i = 0
        while i<len(text):
            c = text[i]
            if state.hasChildren(c):
                state = state.getChildren(c)
                i += 1
            if len(state.outputs) > 0:
                for val in state.outputs:
                    found.append({
                        "pos": i - len(val),
                        "val": val,
                    })
            elif state is self.root:
                i += 1
            else:
                state = state.failureLink
        return found