''''
Invariants:
- The number of letters 'a' remains constant
- The total string length remains unchanged
- Monotonic decrease of the letter 'c'
- Monotonic increase of the letter 'b'
- Decrease in the number of pairs (a, c) where a appears to the left of c
'''

from random import randint
from random import choice

T_stroke = {
    "abbc": "bbab",
    "abcc": "babb",
    "baac": "abab",
    "cb": "bc",
    "ca": "ab",
    "abbbc": "bbabb",
    "bbaba": "abbab",
    "abbcc": "babbb",
    "babba": "ababb",
    "baabc": "ababb",
    "baaab": "ababa",
    "babac": "abbab",
    "abbbbc": "bbabbb"
}

def count_a_c(w):
    count_a = 0
    res = 0

    for i in w:
        if i == 'a':
            count_a += 1
        if i == 'c':
            res += count_a

    return res

def check_invariants(w, w_stroke):
    if w.count('a') != w_stroke.count('a'):
        return False

    if len(w) != len(w_stroke):
        return False

    if w.count('c') < w_stroke.count('c'):
        return False

    if w.count('b') > w_stroke.count('b'):
        return False

    if count_a_c(w) < count_a_c(w_stroke):
        return False

    return True

def generate_random_word(min_len=3, max_len=12):
    alphabet = ['a', 'b', 'c']
    length = randint(min_len, max_len)

    return ''.join([choice(alphabet) for _ in range(length)])

def apply_random_chain_with_check_invariants(w, max_steps=10):
    for _ in range(max_steps):
        variants = []
        for left, right in T_stroke.items():
            pos = w.find(left)

            while pos != -1:
                variants.append((left, right, pos))
                pos = w.find(left, pos + 1)

        if variants:
            left, right, pos = choice(variants)
            w_stroke = w[:pos] + right + w[pos + len(left):]

            if check_invariants(w, w_stroke) == False:
                return False

            w = w_stroke
        else:
            return True

    return True

def run_metamorphic_test(num_tests):
    num_accept_tests = 0
    for i in range(num_tests):
        word = generate_random_word()
        res = apply_random_chain_with_check_invariants(word)

        if res:
            num_accept_tests += 1

        print(f"Test {i}:{' Accept' if res else 'Wrong'}")

    print(f"Total accept tests {num_accept_tests}")

if __name__ == '__main__':
    run_metamorphic_test(50)