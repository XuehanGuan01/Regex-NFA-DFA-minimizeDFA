import RegExp_conversion as rec
import hopcroft
'''
DFA示例输入
states = {0, 1, 2, 3, 4, 5}
alphabet = {'a', 'b'}
initial_state = {0}
accepting_states = {1, 3, 5}
transitions = {
    0:{'a': 1, 'b': 2},
    1:{'a':0, 'b':3},
    2:{'a':4, 'b':5},
    3:{'a':4, 'b':5},
    4:{'a':4, 'b':5},
    5:{'a':5, 'b':5},
}
'''
exp = rec.expressions
for expr in exp:
    tokens = rec.lexer(expr)
    parser = rec.Parser(tokens)
    ast = parser.parse()
    nfa = rec.compile_nfa(ast)
    print(f"Regular Expression: {expr}")
    rec.print_nfa_table(nfa)
    print()
    dfa_start, dfa_end, dfa_transitions, dfa_states = rec.nfa_to_dfa(nfa)
    my_states, my_symbols, my_start, my_final, my_delta = rec.print_dfa(dfa_start, dfa_end, dfa_transitions)
    my_start = set(my_start)

# print("my_states", my_states)
# print("my_symbols:", my_symbols_set)
# print("my_start:", my_start)
# print("my_final", my_final)
# print("my_delta:", my_delta)
my_symbols_set = set(my_symbols)
# print('Initial state:')
# print(my_states)
# print('Final states:')
# result = hopcroft.my_hopcroft(my_states, my_symbols_set, my_final, my_delta)
# print(result,'\n')
# 生成最小化DFA
minimized_states = hopcroft.my_hopcroft(my_states, my_symbols_set, my_final, my_delta)

new_states, new_initial_state, new_accepting_states, new_transitions = hopcroft.generate_minimized_dfa(minimized_states, my_symbols_set, my_start, my_final, my_delta)
# print('Minimized DFA States:', new_states)
# print('Minimized DFA Initial State:', new_initial_state)
# print('Minimized DFA Accepting States:', new_accepting_states)
# print('Minimized DFA Transitions:', new_transitions,'\n')
print('***  Minimized DFA TABLE  ***')
hopcroft.print_minimized_dfa_table(new_states, new_transitions, my_symbols_set)