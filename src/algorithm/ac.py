# Aho-Corasick (AC) Algorithm for Pattern Matching

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
        
    def search(self, text):
        count = 0
        state = self.root
        i = 0
        
        while i < len(text):
            c = text[i]
            
            while not state.hasChildren(c) and state is not self.root:
                state = state.failureLink
            
            if state.hasChildren(c):
                state = state.getChildren(c)
                i += 1
            else:
                i += 1
            
            if len(state.outputs) > 0:
                count += len(state.outputs)
        
        return count
    
    def search_detailed(self, text):
        found = []
        state = self.root
        i = 0
        
        while i < len(text):
            c = text[i]
            
            # Try to move to next state
            while not state.hasChildren(c) and state is not self.root:
                state = state.failureLink
            
            if state.hasChildren(c):
                state = state.getChildren(c)
                i += 1
            else:
                i += 1
            
            # Record all patterns that end at current position
            if len(state.outputs) > 0:
                for val in state.outputs:
                    found.append({
                        "pos": i - len(val),
                        "val": val,
                    })
        
        return found

# Example usage
# if __name__ == "__main__":
#     patterns = ["banking"]
    
    
#     # Test with multiple patterns
#     patterns = ["he", "she", "his", "hers"]
#     text = "ushers"
    
#     ac = AhoCorasick(patterns)
#     count = ac.search(text)
#     print(f"Total occurrences of patterns {patterns} in text '{text}': {count}")
    
#     # Show detailed results for comparison
#     detailed = ac.search_detailed(text)
#     print(f"Detailed matches: {detailed}")
    
#     # Test with overlapping patterns
#     patterns2 = ["AA", "AAA"]
#     text2 = "AAAA"
    
#     ac2 = AhoCorasick(patterns2)
#     count2 = ac2.search(text2)
#     print(f"Total occurrences of patterns {patterns2} in text '{text2}': {count2}")
    
#     detailed2 = ac2.search_detailed(text2)
#     print(f"Detailed matches: {detailed2}")