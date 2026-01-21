import re
from random import randint, choice


def generate_random_word(min_len=1, max_len=8):
    alphabet = ['a', 'b', 'c']
    length = randint(min_len, max_len)
    return ''.join([choice(alphabet) for _ in range(length)])


regex_pattern = r"^(aa*bb*ab|c)*(ba(b|(c|ac)ac|cc(bb|aba))*)*$"


def check_regex(word):
    return bool(re.match(regex_pattern, word))


DFA_STRUCTURE = {
    "1": {"a": "2", "b": "5", "c": "1"},
    "2": {"a": "2", "b": "3"},
    "3": {"a": "4", "b": "3"},
    "4": {"b": "1"},
    "5": {"a": "6"},
    "6": {"a": "7", "b": "9", "c": "10"},
    "7": {"c": "8"},
    "8": {"a": "11"},
    "9": {"a": "6", "b": "9", "c": "10"},
    "10": {"a": "11", "c": "12"},
    "11": {"c": "6"},
    "12": {"a": "14", "b": "13"},
    "13": {"b": "6"},
    "14": {"b": "5"}
}
DFA_START = "1"
DFA_FINALS = {"1", "6", "9"}


def check_dfa(word, structure, start, finals):
    current_state = start
    for char in word:
        if char in structure[current_state]:
            current_state = structure[current_state][char]
        else:
            return False
    return current_state in finals


NFA_STRUCTURE = {
    "S": {"a": ["a1"], "b": ["b8"], "c": ["c7"]},
    "a1": {"a": ["a2"], "b": ["b3"]},
    "a2": {"a": ["a2"], "b": ["b3"]},
    "b3": {"b": ["b4"]},
    "b4": {"b": ["b4"], "a": ["a5"]},
    "a5": {"b": ["b6"]},
    "b6": {"a": ["a1"], "c": ["c7"]},
    "c7": {"b": ["b8"], "c": ["c7"]},
    "b8": {"a": ["a9"]},
    "a9": {"a": ["a12"], "b": ["b8"], "c": ["c11", "c16"]},
    "b10": {"a": ["a12"], "b": ["b8", "b10"], "c": ["c11", "c16"]},
    "c11": {"a": ["a14"]},
    "a12": {"c": ["c13"]},
    "c13": {"a": ["a14"]},
    "a14": {"c": ["c15"]},
    "c15": {"a": ["a12"], "b": ["b8", "b10"], "c": ["c11", "c16"]},
    "c16": {"c": ["c17"]},
    "c17": {"a": ["a20"], "b": ["b18"]},
    "b18": {"b": ["b19"]},
    "b19": {"a": ["a12"], "b": ["b8", "b10"], "c": ["c11", "c16"]},
    "a20": {"b": ["b21"]},
    "b21": {"a": ["a22"]},
    "a22": {"b": ["b8", "b10"], "c": ["c11", "c16"]}
}
NFA_START = "S"
NFA_FINALS = {"S", "b6", "c7", "a9", "b10", "b19", "a22", "c15"}

SFA_STRUCTURE = {
    "S": {"a": ["a1"], "b": ["b8"], "c": ["c7"]},
    "a1": {"a": ["a2"], "b": ["b3"]},
    "a2": {"a": ["a2"], "b": ["b3"]},

    "b3": {"b": ["b3", "&"]},

    "&": {"a": ["a4", "a5"]},

    "a4": {"a": ["a4"], "b": ["b"]},
    "b": {"c": ["c7"], "a": ["a1"]},

    "a5": {"b": ["b6"]},
    "b6": {"b": ["b6"], "a": ["a1"], "c": ["c7"]},

    "c7": {"b": ["b8"], "c": ["c7"]},
    "b8": {"a": ["a9"]},

    "a9": {"a": ["a12"], "b": ["b8"], "c": ["c11", "c16"]},

    "b10": {"a": ["a12"], "b": ["b8", "b10"], "c": ["c11", "c16"]},

    "c11": {"a": ["a14"]},
    "a12": {"c": ["c13"]},
    "c13": {"a": ["a14"]},
    "a14": {"c": ["c15"]},

    "c15": {"a": ["a12"], "b": ["b8", "b10"], "c": ["c11", "c16"]},
    "c16": {"c": ["c17"]},
    "c17": {"a": ["a20"], "b": ["b18"]},
    "b18": {"b": ["b19"]},

    "b19": {"a": ["a12"], "b": ["b8", "b10"], "c": ["c11", "c16"]},
    "a20": {"b": ["b21"]},
    "b21": {"a": ["a22"]},

    "a22": {"b": ["b8", "b10"], "c": ["c11", "c16"]}
}

SFA_START = "S"
SFA_FINALS = {"S", "b6", "c7", "a9", "b10", "b19", "a22", "c15", "b"}

AND_NODES = {"&"}


def check_nfa(word, structure, start, finals):
    current_states = {start}
    for char in word:
        next_states = set()
        for state in current_states:
            if state in structure and char in structure[state]:
                transitions = structure[state][char]
                next_states.update(transitions)
        current_states = next_states
        if not current_states:
            return False
    return bool(current_states & finals)


def check_sfa(word, structure, start_state, finals, and_nodes):
    def dfs(current_state, idx):
        if idx == len(word):
            return current_state in finals

        char = word[idx]

        if current_state not in structure or char not in structure[current_state]:
            return False

        next_states = structure[current_state][char]

        if current_state in and_nodes:
            return all(dfs(nxt, idx + 1) for nxt in next_states)
        else:
            return any(dfs(nxt, idx + 1) for nxt in next_states)

    return dfs(start_state, 0)


print(f"{'WORD':<10} | {'REGEX':<7} | {'DFA':<7} | {'NFA':<7} | {'SWA':<7}")
print("-" * 65)

for i in range(20):
    w = generate_random_word()

    res_regex = check_regex(w)
    res_dfa = check_dfa(w, DFA_STRUCTURE, DFA_START, DFA_FINALS)
    res_nfa = check_nfa(w, NFA_STRUCTURE, NFA_START, NFA_FINALS)
    res_sfa = check_sfa(w, SFA_STRUCTURE, SFA_START, SFA_FINALS, AND_NODES)

    print(
        f"{w:<10} | {str(int(res_regex)):<7} | {str(int(res_dfa)):<7} | {str(int(res_nfa)):<7} | {str(int(res_sfa)):<7}")
    