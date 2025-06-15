# # Fuzzy Algorithm using Levenshtein Distance to find similar pattern

import re

def levDistance(s1, s2):
    n = len(s1)
    m = len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,        # Deletion
                dp[i][j - 1] + 1,        # Insertion
                dp[i - 1][j - 1] + cost  # Substitution
            )
    return dp[n][m]

def calculate_similarity(s1, s2):
    if not s1 and not s2:
        return 100.0
    
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 0.0 # Salah satu string kosong, yang lain tidak

    distance = levDistance(s1, s2)
    
    similarity = (1 - (distance / max_len)) * 100
    return similarity

def fuzzy_search(text, pattern, min_similarity_percent=80.0):
    count = 0
    words_in_text = re.findall(r'\b\w+\b', text)
    
    for word in words_in_text:
        similarity = calculate_similarity(word, pattern)
        
        if similarity >= min_similarity_percent:
            count += 1

    return count

# import re
# # Perhitungan Levenshtein Distance
# def levDistance(s1, s2):
#     n = len(s1)
#     m = len(s2)
#     dp = [[0] * (m + 1) for _ in range(n + 1)]

#     for i in range(n + 1):
#         dp[i][0] = i

#     for j in range(m + 1):
#         dp[0][j] = j

#     for i in range(1, n + 1):
#         for j in range(1, m + 1):
#             if s1[i - 1] == s2[j - 1]:
#                 dp[i][j] = dp[i - 1][j - 1]
#             else:
#                 dp[i][j] = min(
#                     dp[i - 1][j] + 1,     # deletion
#                     dp[i][j - 1] + 1,     # insertion
#                     dp[i - 1][j - 1] + 1  # substitution
#                 )

#     return dp[n][m]

# # Modified Fuzzy Algorithm to count similar patterns in text
# def fuzzySearch(text, pattern, maxDistance):
#     count = 0
#     words_in_text = re.findall(r'\b\w+\b', text.lower())

#     for word in words_in_text:
#         distance = levDistance(word, pattern)
#         if distance <= maxDistance:
#             count += 1
#     return count

# def fuzzySearchDetailed(text, pattern, maxDistance):
#     results = []
#     n = len(text)
#     m = len(pattern)
    
#     if m == 0:
#         return results
    
#     for i in range(n - m + 1):
#         substring = text[i:i + m]
#         distance = levDistance(substring, pattern)
#         if distance <= maxDistance:
#             results.append((i, substring, distance))

#     return results

# def fuzzySearchVariableLength(text, pattern, maxDistance):
#     count = 0
#     n = len(text)
#     m = len(pattern)
    
#     if m == 0:
#         return 0
    
#     min_len = max(1, m - maxDistance)
#     max_len = min(n, m + maxDistance)
    
#     for length in range(min_len, max_len + 1):
#         for i in range(n - length + 1):
#             substring = text[i:i + length]
#             distance = levDistance(substring, pattern)
#             if distance <= maxDistance:
#                 count += 1
    
#     return count

# # def fuzzy_search_word_by_word(text, pattern, maxDistance):
# #     count = 0
# #     words_in_text = re.findall(r'\b\w+\b', text.lower())

# #     for word in words_in_text:
# #         distance = levDistance(word, pattern)
# #         if distance <= maxDistance:
# #             count += 1
# #     return count

# # Example usage
# if __name__ == "__main__":
#     text = "The quick brown fox jumps over the lazy dog"
#     pattern = "quick"
#     maxDistance = 1
    
#     # Count matches with fixed length
#     count = fuzzySearch(text, pattern, maxDistance)
#     print(f"Pattern '{pattern}' found {count} similar matches (distance ≤ {maxDistance}) in text")
    
#     # Show detailed results for comparison
#     detailed = fuzzySearchDetailed(text, pattern, maxDistance)
#     print(f"Detailed matches: {detailed}")
    
#     # Test with variable length matching
#     count_var = fuzzySearchVariableLength(text, pattern, maxDistance)
#     print(f"Pattern '{pattern}' found {count_var} similar matches with variable length (distance ≤ {maxDistance})")
    
#     # Test with higher tolerance
#     pattern2 = "fox"
#     maxDistance2 = 2
#     count2 = fuzzySearch(text, pattern2, maxDistance2)
#     print(f"Pattern '{pattern2}' found {count2} similar matches (distance ≤ {maxDistance2}) in text")
    
#     detailed2 = fuzzySearchDetailed(text, pattern2, maxDistance2)
#     print(f"Detailed matches: {detailed2}")