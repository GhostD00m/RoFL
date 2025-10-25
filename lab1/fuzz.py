from random import randint
from random import choice
from collections import deque

T_stroke_1_priority = {
    "abbbc": "bbabb",
    "bbaba": "abbab",
    "abbcc": "babbb",
    "babba": "ababb",
    "baabc": "ababb",
    "baaab": "ababa",
    "babac": "abbab",
    "abbbbc": "bbabbb"
}

T_stroke_2_priority = {
    "abbc": "bbab",
    "abcc": "babb",
    "baac": "abab",
    "cb": "bc",
    "ca": "ab"
}

T = T_stroke_2_priority

def generate_random_word(min_len=3, max_len=12):
    alphabet = ['a', 'b', 'c']
    length = randint(min_len, max_len)
    return ''.join([choice(alphabet) for _ in range(length)])

def apply_random_chain(w, rools, max_steps=10):
    for _ in range(max_steps):
        variants = []
        for left, right in rools.items():
            pos = w.find(left)
            while pos != -1:
                variants.append((left, right, pos))
                pos = w.find(left, pos + 1)
        if variants:
            left, right, pos = choice(variants)
            w = w[:pos] + right + w[pos + len(left):]
        else:
            break
    return w

def run_fuzz_testing(w, w_stroke):
    if w == w_stroke:
        return True
    visited = set([w])
    queue = deque([w])
    while queue:
        current = queue.popleft()
        variants = []
        for left, right in T_stroke_1_priority.items():
            pos = current.find(left)
            while pos != -1:
                variants.append((left, right, pos))
                pos = current.find(left, pos + 1)
        for left, right in T_stroke_2_priority.items():
            pos = current.find(left)
            while pos != -1:
                variants.append((left, right, pos))
                pos = current.find(left, pos + 1)
        for left, right, pos in variants:
            w_s = current[:pos] + right + current[pos + len(left):]
            if w_s == w_stroke:
                return True
            if w_s not in visited:
                visited.add(w_s)
                queue.append(w_s)
    return False

num_accept_tests = 0
for i in range(50):
    w = generate_random_word()
    w_stroke = apply_random_chain(w, T)
    res = run_fuzz_testing(w, w_stroke)
    if res:
        num_accept_tests += 1
    print(f"Test {i}:{' Accept' if res else 'Wrong'}")
print(f"Total accept tests {num_accept_tests}")