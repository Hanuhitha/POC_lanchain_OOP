def wordBreak(s, wordDict):
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(len(s)):
        for j in range(i, -1, -1):
            if dp[j] and s[j:i + 1] in wordDict:
                dp[i + 1] = True
                break
    return dp[len(s)]

def generateSentences(s, wordDict):
    result = []
    def backtrack(start, current_sentence):
        if start == len(s):
            result.append(' '.join(current_sentence))
            return

        for i in range(start + 1, len(s) + 1):
            word = s[start:i]
            if word in wordDict:
                current_sentence.append(word)
                backtrack(i, current_sentence)
                current_sentence.pop()
    backtrack(0, [])
    return result