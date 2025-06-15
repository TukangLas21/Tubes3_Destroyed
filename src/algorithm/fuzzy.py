# Fuzzy Algorithm using Levenshtein Distance to find similar pattern


# Perhitungan Levenshtein Distance
def levDistance(s1, s2):
    n = len(s1)
    m = len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n+1):
        dp[i][0] = i

    for j in range(m+1):
        dp[0][j] = j

    for i in range(1, n+1):
        for j in range(1, m+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = min(
                    dp[i-1][j] + 1, # deletion
                    dp[i][j-1] + 1, # insertion
                    dp[i-1][j-1] + 1) # substitusion

    return dp[n][m]

# Algoritma Fuzzy untuk mencari pola yang mirip dalam String

def fuzzySearch(text, pattern, maxDistance):

    results = []
    n = len(text)
    m = len(pattern)
    
    for i in range(n - m + 1) :
        substring = text[i:i+m]
        distance = levDistance(substring, pattern)
        if distance <= maxDistance:
            results.append((i, substring, distance))

    return results