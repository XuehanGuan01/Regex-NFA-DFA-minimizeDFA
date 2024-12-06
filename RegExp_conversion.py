import enum
import pandas as pd
from tabulate import tabulate
'''
定义正则表达式中可能出现的token类型
'''
expressions = [
    # 'b(a|b)*a'#课件原题
    'ab(((ba)*|bbb)*|a)*b'#作业原题
    ]
class TokenType(enum.Enum):
    LEFT_PAREN = 1  # 左括号
    RIGHT_PAREN = 2  # 右括号
    CHAR = 3  # 单个字符
    CHOICE = 4  # 选择符（|）
    STAR = 5  # 闭包（*）
    PLUS = 6  # 正闭包（+）
    QUESTION = 7  # 可选（?）
    EPSILON = 8  # 空字符串
    END = 9  # 结束标志
'''
将正则表达式字符串分解为token列表，忽略空格
'''
def lexer(expression):
    tokens = []
    i = 0
    while i < len(expression):
        char = expression[i]
        if char == '(':
            tokens.append({'type': TokenType.LEFT_PAREN, 'value': '('})
            i += 1
        elif char == ')':
            tokens.append({'type': TokenType.RIGHT_PAREN, 'value': ')'})
            i += 1
        elif char == '|':
            tokens.append({'type': TokenType.CHOICE, 'value': '|'})
            i += 1
        elif char == '*':
            tokens.append({'type': TokenType.STAR, 'value': '*'})
            i += 1
        elif char == '+':
            tokens.append({'type': TokenType.PLUS, 'value': '+'})
            i += 1
        elif char == '?':
            tokens.append({'type': TokenType.QUESTION, 'value': '?'})
            i += 1
        elif char == ' ':
            i += 1
        else:
            tokens.append({'type': TokenType.CHAR, 'value': char})
            i += 1
    tokens.append({'type': TokenType.END, 'value': 'END'})
    return tokens
'''
实现递归下降解析器，解析token列表生成抽象语法树（AST）
'''
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.next_token()

    def next_token(self):
        if self.tokens:
            self.current_token = self.tokens.pop(0)
        else:
            self.current_token = {'type': TokenType.END, 'value': 'END'}

    def parse(self):
        expr = self.parse_expression()
        self.expect_token(TokenType.END)
        return expr

    def parse_expression(self):
        # 解析表达式，处理选择运算（|）
        left = self.parse_concat()
        while self.current_token['type'] == TokenType.CHOICE:
            self.consume_token(TokenType.CHOICE)
            right = self.parse_concat()
            left = ChoiceNode(left, right)
        return left

    def parse_concat(self):
        # 解析连接运算
        left = self.parse_closure()
        while self.current_token['type'] not in [TokenType.CHOICE, TokenType.RIGHT_PAREN, TokenType.END]:
            right = self.parse_closure()
            left = ConcatNode(left, right)
        return left

    def parse_closure(self):
        # 解析闭包运算（*、+、?）
        child = self.parse_primary()
        while self.current_token['type'] in [TokenType.STAR, TokenType.PLUS, TokenType.QUESTION]:
            if self.current_token['type'] == TokenType.STAR:
                self.consume_token(TokenType.STAR)
                child = ClosureNode(child, 'star')
            elif self.current_token['type'] == TokenType.PLUS:
                self.consume_token(TokenType.PLUS)
                child = ClosureNode(child, 'plus')
            elif self.current_token['type'] == TokenType.QUESTION:
                self.consume_token(TokenType.QUESTION)
                child = ClosureNode(child, 'question')
        return child

    def parse_primary(self):
        # 解析基本单元，如字符、括号
        if self.current_token['type'] == TokenType.LEFT_PAREN:
            self.consume_token(TokenType.LEFT_PAREN)
            expr = self.parse_expression()
            self.expect_token(TokenType.RIGHT_PAREN)
            return expr
        elif self.current_token['type'] == TokenType.CHAR:
            char = self.current_token['value']
            self.consume_token(TokenType.CHAR)
            return CharNode(char)
        else:
            raise Exception(f"Unexpected token: {self.current_token}")

    def expect_token(self, token_type):
        # 检查并消费预期的token类型
        if self.current_token['type'] == token_type:
            self.consume_token(token_type)
        else:
            raise Exception(f"Expected token {token_type}, got {self.current_token['type']}")

    def consume_token(self, token_type):
        # 消费指定类型的token
        if self.current_token['type'] == token_type:
            self.next_token()
        else:
            raise Exception(f"Unexpected token: {self.current_token['type']}")

class Node:#node是一个基类，表示所有节点的通用结构，空类，仅用于继承
    pass

class CharNode(Node):#接受一个字符char
    def __init__(self, char):
        self.char = char  # 字符


class ChoiceNode(Node):#选择节点，对应正则表达式（|）
    def __init__(self, left, right):
        self.left = left  # 左子节点
        self.right = right  # 右子节点


class ConcatNode(Node):#连接节点，类似正则表达式中的连接操作
    def __init__(self, left, right):
        self.left = left  # 左子节点
        self.right = right  # 右子节点


class ClosureNode(Node):#闭包节点，类似正则表达式中的（*，+，?）
    def __init__(self, child, type):
        self.child = child  # 子节点
        self.type = type  # 闭包类型：'star', 'plus', 'question'


class NFA:
    def __init__(self, start, end, transitions):
        self.start = start  # 起始状态
        self.end = end  # 终止状态
        self.transitions = transitions  # 转移函数，字典形式表示

    def add_transition(self, state, symbol, next_state):
        # 添加转移
        if state not in self.transitions:
            self.transitions[state] = {}
        if symbol not in self.transitions[state]:
            self.transitions[state][symbol] = []
        self.transitions[state][symbol].append(next_state)


nfa_state_counter = 0


def get_new_state():
    # 获取新的状态编号
    global nfa_state_counter
    state = nfa_state_counter
    nfa_state_counter += 1
    return state

'''
根据AST生成NFA，处理不同类型的节点，生成相应的状态和转移
'''
def compile_nfa(node):
    # 根据AST生成NFA
    global nfa_state_counter
    if isinstance(node, CharNode):#字符节点
        start = get_new_state()
        end = get_new_state()
        nfa = NFA(start, end, {})
        nfa.add_transition(start, node.char, end)
        return nfa
    elif isinstance(node, ChoiceNode):#选择节点
        left_nfa = compile_nfa(node.left)
        right_nfa = compile_nfa(node.right)
        start = get_new_state()
        end = get_new_state()
        nfa = NFA(start, end, {})
        nfa.add_transition(start, 'epsilon', left_nfa.start)
        nfa.add_transition(start, 'epsilon', right_nfa.start)
        nfa.add_transition(left_nfa.end, 'epsilon', end)
        nfa.add_transition(right_nfa.end, 'epsilon', end)
        nfa.transitions.update(left_nfa.transitions)
        nfa.transitions.update(right_nfa.transitions)
        return nfa
    elif isinstance(node, ConcatNode):#连接节点
        left_nfa = compile_nfa(node.left)
        right_nfa = compile_nfa(node.right)
        left_nfa.add_transition(left_nfa.end, 'epsilon', right_nfa.start)
        nfa = NFA(left_nfa.start, right_nfa.end, {})
        nfa.transitions = left_nfa.transitions.copy()
        nfa.transitions.update(right_nfa.transitions)
        return nfa
    elif isinstance(node, ClosureNode):#闭包节点
        child_nfa = compile_nfa(node.child)
        start = get_new_state()
        end = get_new_state()
        nfa = NFA(start, end, {})
        nfa.add_transition(start, 'epsilon', end)
        nfa.add_transition(start, 'epsilon', child_nfa.start)
        nfa.add_transition(child_nfa.end, 'epsilon', end)
        if node.type == 'star':
            nfa.add_transition(child_nfa.end, 'epsilon', child_nfa.start)
        elif node.type == 'plus':
            pass  # a+ is a followed by a*
        elif node.type == 'question':
            pass  # a? is a or epsilon
        nfa.transitions.update(child_nfa.transitions)
        return nfa
    else:
        raise Exception(f"Unknown node type: {node}")

def print_nfa(nfa):
    # 打印NFA的状态转换表
    for state in nfa.transitions:
        print()
        for symbol in nfa.transitions[state]:
            for next_state in nfa.transitions[state][symbol]:
                print({state}, end="")
                print(" ->",{symbol} ,"->", {next_state})

    #print(f"Start state: {nfa.start}")
    #print(f"End state: {nfa.end}")

def print_nfa_table(nfa):
    # 打印NFA的状态转换表
    states = nfa.transitions.keys()
    symbols = set()
    for state in states:
        symbols.update(nfa.transitions[state].keys())
    symbols = sorted(symbols)

    data = []
    for state in states:
        row = {'state': state}
        for symbol in symbols:
            if symbol in nfa.transitions[state]:
                row[symbol] = ','.join(map(str, nfa.transitions[state][symbol]))
            else:
                row[symbol] = 'non'
        data.append(row)

    df = pd.DataFrame(data)
    df.set_index('state', inplace=True)
    print("***        NFA TABLE        ***   ")
    print(tabulate(df, headers='keys', tablefmt='pretty'))
    print(f"Start state: {nfa.start}")
    print(f"End state: {nfa.end}")

'''
求解NFA-DFA
'''
def epsilon_closure(nfa, states):
    # 求出ε-closure(s)
    closure = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        if 'epsilon' in nfa.transitions.get(state, {}):
            for next_state in nfa.transitions[state]['epsilon']:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
    return closure

def move(nfa, states, symbol):
    # 根据符号求出下一个状态集合
    next_states = set()
    for state in states:
        if symbol in nfa.transitions.get(state, {}):
            next_states.update(nfa.transitions[state][symbol])
    return next_states

def nfa_to_dfa(nfa):
    # 将NFA转换为DFA
    dfa_start = epsilon_closure(nfa, {nfa.start})
    dfa_states = [dfa_start]
    dfa_transitions = {}
    unmarked_states = [dfa_start]
    symbols = set(symbol for transitions in nfa.transitions.values()
                  for symbol in transitions if symbol != 'epsilon')
    # 对不是epsilon转换的状态录入进symbols内
    # print(symbols)
    while unmarked_states:
        current_state = unmarked_states.pop()
        for symbol in symbols:
            next_state = epsilon_closure(nfa, move(nfa, current_state, symbol))
            if next_state and next_state not in dfa_states:
                dfa_states.append(next_state)
                unmarked_states.append(next_state)
            if next_state:
                dfa_transitions[(frozenset(current_state), symbol)] = frozenset(next_state)

    dfa_states = [frozenset(state) for state in dfa_states]
    # print(dfa_states)
    dfa_start = dfa_states[0]
    dfa_end = [state for state in dfa_states if nfa.end in state]

    return dfa_start, dfa_end, dfa_transitions,dfa_states

def print_dfa(dfa_start, dfa_end, dfa_transitions):
    # 打印DFA的状态转换表
    states = set(state for state, _ in dfa_transitions) | set(next_state for _, next_state in dfa_transitions)
    states = {state for state in states if isinstance(state, frozenset)}  # 只保留frozenset类型的状态
    # print("函数里的states:", states)
    symbols = sorted(set(symbol for _, symbol in dfa_transitions))
    # print("函数里的symbols:", symbols)

    # 创建状态映射表
    state_mapping = {state: i for i, state in enumerate(states)}

    data = []
    for state in states:
        row = {'state': state_mapping[state]}
        for symbol in symbols:
            if (state, symbol) in dfa_transitions:
                next_state = dfa_transitions[(state, symbol)]
                if next_state not in state_mapping:
                    state_mapping[next_state] = len(state_mapping)
                row[symbol] = state_mapping[next_state]
            else:
                row[symbol] = 'non'
        data.append(row)
    # print("函数内的state_mapping：",state_mapping)
    # 提取过滤后的状态
    filtered_states = [row['state'] for row in data]

    # 重新排序状态
    new_state_mapping = {state: j for j, state in enumerate(filtered_states)}
    # print("函数内的new_state_mapping：", new_state_mapping)
    # print("修改后的filtered_states：", filtered_states)
    # print("函数内的data：", data)

    # 更新状态编号
    for row in data:
        # print("data里的row:",row)
        row['state'] = new_state_mapping[row['state']]
        # for symbol in symbols:
        #     if row[symbol] != 'non':
        #         print("row[symbol]：",row[symbol])
        #         row[symbol] = new_state_mapping[row[symbol]]

    df = pd.DataFrame(data)
    # print("df：",df)
    df.set_index('state', inplace=True)
    # print('function_state_mapping：', state_mapping)
    print("***   DFA TABLE   ***   ")
    print(tabulate(df, headers='keys', tablefmt='pretty'))
    # print(f"Start state: {new_state_mapping[state_mapping[dfa_start]]}")
    # print("dfa_end：",dfa_end)
    # print(new_state_mapping)
    # print(state_mapping)
    # print(f"End states: {[new_state_mapping[state_mapping[state]] for state in dfa_end]}")
    # 处理 End states，如果DFA指向自身情况下可能报错
    end_states = []
    for state in dfa_end:
        try:
            end_states.append(new_state_mapping[state_mapping[state]])
        except KeyError:
            # 如果找不到状态，则这个DFA是由自身指向自身，end_states是start_states
            end_states = [new_state_mapping[state_mapping[dfa_start]]]
            break

    # print(f"End states: {end_states}")

    # 定义 States 并返回 function_state_mapping 内的 value()
    States = set(state_mapping.values())
    States_str = {str(state) for state in States}
    # 定义 my_start 并返回其字符串形式
    my_start = new_state_mapping[state_mapping[dfa_start]]
    my_start_str = str(my_start)
    # 将 end_states 改成字符型并放入一个集合中
    my_final = {str(state) for state in end_states}

    # 定义 my_delta
    my_delta = {}
    # 读取 data 里的所有 row，并构建 my_delta
    for row in data:
        state = str(row['state'])
        # transitions = {symbol: str(row[symbol]) for symbol in symbols if row[symbol] != 'non'}
        transitions = {symbol: str(row[symbol]) for symbol in symbols}
        my_delta[state] = transitions
    return States_str,symbols,my_start_str,my_final,my_delta

def main():
    # 处理正则表达式，并转换成NFA
    for expr in expressions:
        tokens = lexer(expr)
        parser = Parser(tokens)
        ast = parser.parse()
        nfa = compile_nfa(ast)
    print(f"Regular Expression: {expr}")
    print("NFA INFO:")
    print_nfa(nfa)
    print()
    print_nfa_table(nfa)
    print()
    # 获取DFA相关信息，进行DFA转化以及最小化操作
    dfa_start, dfa_end, dfa_transitions, dfa_states = nfa_to_dfa(nfa)
    print("DFA INFO:")
    print("dfa start：", dfa_start)
    print("dfa end：", dfa_end)
    print("dfa transitions：", dfa_transitions)
    print("dfa states：", dfa_states,'\n')
    print_dfa(dfa_start, dfa_end, dfa_transitions)

if __name__ == "__main__":
    main()