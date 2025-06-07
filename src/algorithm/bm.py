# Boyer-Moore (BM) Algorithm for Pattern Matching
def badCharacterRule(pattern):
    occurrenceMap ={}
    m = len(pattern)
    for i in range(m):
        occurrenceMap[pattern[i]] = i
    return occurrenceMap

def goodSuffixRule(pattern):
    m = len(pattern)
    borders = [0]*(m+1)
    shift = [0]*(m+1)
    i = m
    j = m+1
    borders[i] = j

    while i>0:
        while j<=m and pattern[i-1]!=pattern[j-1]:
            if shift[j]==0:
                shift[j] = j
            j = borders[j]
        i -= 1
        j -= 1
        borders[i] = j
    
    b = borders[0]
    for i in range(m+1):
        if shift[i] == 0:
            shift[i] = b
        if i == b:
            b = borders[b]
    return shift

# BM Algorithm untuk mencari pola dalam string text
def BoyerMoore(text, pattern):
    n = len(text)
    m = len(pattern)
    badCharShift = badCharacterRule(pattern)
    goodSuffixShift = goodSuffixRule(pattern)
    t = 0
    while t<= n-m:
        j = m-1
        while j>=0 and pattern[j] == text[t+j]:
            j -= 1
        if j<0:
            return t
        else:
            char = text[t+j]
            lastOcc = badCharShift.get(char, -1)
            t = t + max(j-lastOcc, goodSuffixShift[j])
    return -1
    