def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    j = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j
            i += 1
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

# Modified KMP Algorithm to count all occurrences of pattern in text
def KMP(text, pattern):
    n = len(text)
    m = len(pattern)
    
    if m == 0:
        return 0
    
    lps = compute_lps(pattern)
    i = j = 0
    count = 0

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1

        if j == m:
            # Pattern found, increment count
            count += 1
            # Continue searching from the next possible position
            j = lps[j - 1]
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return count

if __name__ == "__main__":
    text = "ABABCABABA"
    pattern = "ABA"
    
    result = KMP(text, pattern)
    print(f"Pattern '{pattern}' found {result} times in text '{text}'")
    
    # Test with overlapping patterns
    text2 = "AAAAAAA"
    pattern2 = "AAA"
    result2 = KMP(text2, pattern2)
    print(f"Pattern '{pattern2}' found {result2} times in text '{text2}'")
    
    # Test with no matches
    text3 = "ABCDEF"
    pattern3 = "XYZ"
    result3 = KMP(text3, pattern3)
    print(f"Pattern '{pattern3}' found {result3} times in text '{text3}'")