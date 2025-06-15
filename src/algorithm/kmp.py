# Knuth-Morris-Pratt (KMP) Algorithm for Pattern Matching

# Longest Prefix Suffix or LPS untuk mengidentifikasi pola yang dicari
def compute_lps(pattern):
    m = len(pattern)
    lps = [0]*m
    j=0
    i=1

    while i<m:
        if pattern[i] == pattern[lps[i-1]]:
            lps[i] = j
            i += 1
        else:
            if j != 0:
                j = lps[j-1]
            else:
                lps[i] = 0
                i += 1
    return lps

# KMP Algorithm untuk mencari pola dalam string text
def KMP(text, pattern):
    n = len(text)
    m = len(pattern)
    lps = compute_lps(pattern)
    i = j = 0

    while i<n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == m:
            return True
        elif i<n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j-1]
            else:
                i += 1
    return False