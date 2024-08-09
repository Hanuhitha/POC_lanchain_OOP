def is_interleaving(s1, s2, s3):
    if len(s1) + len(s2) != len(s3):
        return False
    i = j = 0
    for c in s3:
        if i < len(s1) and c == s1[i]:
            i += 1
        elif j < len(s2) and c == s2[j]:
            j += 1
        else:
            return False
    return True