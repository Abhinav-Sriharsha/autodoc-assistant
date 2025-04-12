from timeit import timeit

def ispalindrome_v1(s):
    return s == s[::-1]

def ispalindrome_v2(s):
    for i in range(len(s)//2):
        if s[i] != s[-(i+1)]:
            return False
    return True

def ispalindrome_v3(s):
    for c1, c2 in zip(s, reversed(s)):
        if c1 != c2:
            return False
    return True

S = 'aabbcdcbbaa'

for func in ispalindrome_v1, ispalindrome_v2, ispalindrome_v3:
    print(func.__name__, timeit(lambda: func(S)))