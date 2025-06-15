# Boyer-Moore (BM) Algorithm for Pattern Matching
def badCharacterRule(pattern):
    occurrenceMap = {}
    m = len(pattern)
    for i in range(m):
        occurrenceMap[pattern[i]] = i
    return occurrenceMap

def goodSuffixRule(pattern):
    m = len(pattern)
    borders = [0] * (m + 1)
    shift = [0] * (m + 1)
    i = m
    j = m + 1
    borders[i] = j

    while i > 0:
        while j <= m and pattern[i - 1] != pattern[j - 1]:
            if shift[j] == 0:
                shift[j] = j - i
            j = borders[j]
        i -= 1
        j -= 1
        borders[i] = j
    
    b = borders[0]
    for i in range(m + 1):
        if shift[i] == 0:
            shift[i] = b
        if i == b:
            b = borders[b]
    return shift

def BoyerMoore(text, pattern):
    n = len(text)
    m = len(pattern)
    
    if m == 0:
        return 0
    
    badCharShift = badCharacterRule(pattern)
    goodSuffixShift = goodSuffixRule(pattern)
    
    count = 0
    t = 0
    
    while t <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[t + j]:
            j -= 1
        
        if j < 0:
            # Pattern found, increment count
            count += 1
            # Move to next possible position
            t += goodSuffixShift[0]
        else:
            # Pattern not found, calculate shift
            char = text[t + j]
            lastOcc = badCharShift.get(char, -1)
            t += max(j - lastOcc, goodSuffixShift[j + 1])
    
    return count

# Example usage
if __name__ == "__main__":
    text = "ABAAABCDABABCABCABCDAB"
    pattern = "ABC"
    
    result = BoyerMoore(text, pattern)
    print(f"Pattern '{pattern}' found {result} times in text '{text}'")
    
    # Test with overlapping patterns
    text2 = "AAAAAAA"
    pattern2 = "AAA"
    result2 = BoyerMoore(text2, pattern2)
    print(f"Pattern '{pattern2}' found {result2} times in text '{text2}'")