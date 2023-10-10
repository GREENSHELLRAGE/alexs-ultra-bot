from fuzzywuzzy import fuzz


# Detects the word fortnite in text
def fortnite(text):
    # Hardcoded strings to also censor
    # NOT CASE SENSITIVE
    hardcoded_exceptions = ['🇫🇴🇷🇹🇳🇮🇹🇪', 'fortnut', 'ofrtnite', 'forfnife', 'ortnite', 'forknife', 'nitefort']

    # Returns true if hardcoded words are found in the message
    for word in hardcoded_exceptions:
        if text.lower().count(word) > 0:
            return True

    # Stores multiple possibilities for each letter in case people try to break the censor
    f = ['f', '🇫', '𝓯', '𝒻', '𝓕', '𝐹', '🄵', '𝔽', '🅵', '𝕗', '𝖋', '𝕱', 'ƒ']
    o = ['o', '🇴', '𝓸', '𝑜', '𝓞', '𝒪', '🄾', '𝕆', '🅾', '𝕠', '𝖔', '𝕺', '⭕', '🚫', '0']
    r = ['r', '🇷', '𝓻', '𝓇', '𝓡', '𝑅', '🅁', 'ℝ', '🆁', '𝕣', '𝖗', '𝕽', '®']
    t = ['t', '🇹', '𝓽', '𝓉', '𝓣', '𝒯', '🅃', '𝕋', '🆃', '𝕥', '𝖙', '𝕿', '+']
    n = ['n', '🇳', '𝓷', '𝓃', '𝓝', '𝒩', '🄽', 'ℕ', '🅽', '𝕟', '𝖓', '𝕹']
    i = ['i', '🇮', '𝓲', '𝒾', '𝓘', '𝐼', '🄸', '𝕀', '🅸', '𝕚', '𝖎', '𝕴', '1', '!']
    e = ['e', '🇪', '𝓮', '𝑒', '𝓔', '𝐸', '🄴', '𝔼', '🅴', '𝕖', '𝖊', '𝕰', '3']
    g = ['g']
    h = ['h']
    # Isolates the letters in fortnite and the letter g in case someone says fortnight
    letter_isolate = []
    for letter in text.lower():
        if letter in f:
            letter_isolate.append('f')
        elif letter in o:
            letter_isolate.append('o')
        elif letter in r:
            letter_isolate.append('r')
        elif letter in t:
            letter_isolate.append('t')
        elif letter in n:
            letter_isolate.append('n')
        elif letter in i:
            letter_isolate.append('i')
        elif letter in e:
            letter_isolate.append('e')
        elif letter in g:
            letter_isolate.append('g')
        elif letter in h:
            letter_isolate.append('h')

    # Removes letters if the previous letter is the same
    removed_duplicates = []
    for x in range(len(letter_isolate)):
        if letter_isolate[x] != letter_isolate[x-1] or x == 0:
            removed_duplicates.append(letter_isolate[x])

    # Fuzzywuzzy ratio
    fuzz_ratio = fuzz.token_sort_ratio(''.join(removed_duplicates), "fortnite")

    # Returns true if fortnite is found
    if ''.join(removed_duplicates).count('fortnite') > 0 or fuzz_ratio >= 88:
        return True
