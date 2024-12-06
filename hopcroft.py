from tabulate import tabulate
def prepare_initial_state(states, accepting_states):
    new_states = set()
    non_accepting = []
    accepting = frozenset(accepting_states)
    for i in states:
        if i not in accepting:
            non_accepting.append(i)
    new_states.add(frozenset(accepting))
    new_states.add(frozenset(non_accepting))   
    return new_states

def split(current_set, alphabet, transitions):
    hash_table = {}
    result = set()
    for state in current_set:
        key = ''
        for action in alphabet:
            if action in transitions[state]:
                key += str(transitions[state][action])
        if key not in hash_table:
            hash_table[key] = []
        hash_table[key].append(state)
    values = hash_table.values()
    for current in values:
        result.add(frozenset(current))
    return result
def my_hopcroft(states, alphabet, accepting_states, transitions):
    new_states = prepare_initial_state(states, accepting_states)
    current_states = None

    while (current_states != new_states):
        current_states = new_states.copy()
        new_states = set()
        for current_set in current_states:
            new_states = new_states | split(current_set, alphabet, transitions)

    return new_states
def generate_minimized_dfa(minimized_states, alphabet, initial_state, accepting_states, transitions):
    # 创建新的状态映射
    state_mapping = {}
    new_states = []
    for i, state_set in enumerate(minimized_states):
        new_state = f'S{i}'
        state_mapping[state_set] = new_state
        new_states.append(new_state)

    # 创建新的初始状态
    new_initial_state = None
    for state_set in minimized_states:
        if initial_state.issubset(state_set):
            new_initial_state = state_mapping[state_set]
            break

    # 创建新的接受状态
    new_accepting_states = set()
    for state_set in minimized_states:
        if state_set.intersection(accepting_states):
            new_accepting_states.add(state_mapping[state_set])

    # 创建新的转移函数
    new_transitions = {}
    for state_set in minimized_states:
        new_state = state_mapping[state_set]
        new_transitions[new_state] = {}
        for action in alphabet:
            next_state = None
            for state in state_set:
                if action in transitions[state]:
                    next_state = transitions[state][action]
                    break
            for next_state_set in minimized_states:
                if next_state in next_state_set:
                    new_transitions[new_state][action] = state_mapping[next_state_set]
                    break

    return new_states, new_initial_state, new_accepting_states, new_transitions
def print_minimized_dfa_table(new_states, new_transitions, alphabet):
    table = []
    headers = ["state"] + list(alphabet)
    for state in new_states:
        row = [state]
        for action in alphabet:
            if action in new_transitions[state]:
                row.append(new_transitions[state][action])
            else:
                row.append("non")
        table.append(row)
    print(tabulate(table, headers, tablefmt="grid"))