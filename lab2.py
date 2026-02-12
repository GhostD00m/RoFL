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
    "1": {"c": ["1"], "a": ["2"], "b": ["5"]},
    "2": {"a": ["2"], "b": ["3"]},
    "3": {"b": ["3"], "a": ["4"]},
    "4": {"b": ["1"]},

    "5": {"a": ["6"]},

    "6": {"b": ["5", "6"], "a": ["7"], "": ["7"], "c": ["10"]},

    "7": {"c": ["8"]},
    "8": {"a": ["9"]},
    "9": {"c": ["6"]},

    "10": {"c": ["11"]},
    "11": {"b": ["12"], "a": ["13"]},
    "12": {"b": ["6"]},
    "13": {"b": ["5"]}
}

NFA_START = "1"
NFA_FINALS = {"1", "6"}


def get_epsilon_closure(states, structure):
    stack = list(states)
    closure = set(states)

    while stack:
        state = stack.pop()
        if state in structure and "" in structure[state]:
            for next_state in structure[state][""]:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
    return closure


def check_nfa(word, structure, start, finals):
    current_states = get_epsilon_closure({start}, structure)

    for char in word:
        next_states = set()
        for state in current_states:
            if state in structure and char in structure[state]:
                transitions = structure[state][char]
                next_states.update(transitions)

        if not next_states:
            return False

        current_states = get_epsilon_closure(next_states, structure)

    return bool(current_states & finals)


SFA_STRUCTURE = {
    "1": {"c": ["1"], "a": ["2"], "b": ["5"]},
    "2": {"a": ["2"], "b": ["3"]},
    "3": {"b": ["3"], "a": ["4"]},
    "4": {"b": ["1"]},

    "5": {"a": ["6", "14"]},

    "6": {"b": ["5", "6"], "a": ["7"], "": ["7"], "c": ["10"]},
    "7": {"c": ["8"]},
    "8": {"a": ["9"]},
    "9": {"c": ["6"]},

    "10": {"c": ["11"]},
    "11": {"b": ["12"], "a": ["13"]},
    "12": {"b": ["6"]},
    "13": {"b": ["5"]},

    "14": {"c": ["15"], "a": ["14"], "b": ["14"]},
    "15": {"c": ["14"], "a": ["15"], "b": ["15"]}
}

SFA_START = "1"
SFA_FINALS = {"1", "6", "14"}
AND_NODES = {"5"}


def check_sfa(word, structure, start_state, finals, and_nodes):
    memo = {}

    def dfs(current_state, idx, path):
        state_key = (current_state, idx)

        if state_key in memo:
            return memo[state_key]

        if idx == len(word):
            result = current_state in finals
            if not result and current_state in structure and "" in structure[current_state]:
                if (current_state, idx) not in path:
                    new_path = path | {(current_state, idx)}
                    if current_state in and_nodes:
                        result = all(dfs(nxt, idx, new_path) for nxt in structure[current_state][""])
                    else:
                        result = any(dfs(nxt, idx, new_path) for nxt in structure[current_state][""])

            memo[state_key] = result
            return result

        char = word[idx]

        results_to_combine = []
        is_and = current_state in and_nodes

        if current_state in structure and "" in structure[current_state]:
            if (current_state, idx) not in path:
                new_path = path | {(current_state, idx)}
                for nxt in structure[current_state][""]:
                    results_to_combine.append(dfs(nxt, idx, new_path))

        if current_state in structure and char in structure[current_state]:
            for nxt in structure[current_state][char]:
                results_to_combine.append(dfs(nxt, idx + 1, set()))

        if not results_to_combine:
            return False

        if is_and:
            return all(results_to_combine)
        else:
            return any(results_to_combine)

    return dfs(start_state, 0, set())


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
