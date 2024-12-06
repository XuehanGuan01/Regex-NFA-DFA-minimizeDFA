# Regex-NFA-DFA-minimizedDFA
Compiler principle design, a regular expression into NFA, NFA into DFA, DFA and then simplified to minimize the DFA project

## SCNU 编译原理实验 DFA生成器

## 一、实验内容：
(1) 设计一个应用软件，以实现将正则表达式-->NFA--->DFA-->DFA最小化
正则表达式应该支持单个字符作为基本正则表达式，运算符号有： 连接（|）、选择、闭包（*）、正闭包（+）、括号（）、可选（? ）

 输入：一行（一个）或多行（多个）正则表达式
 输出：NFA状态转换表
      DFA状态转换表
      最小化DFA状态转换表
 
（2）应该书写完善的软件文档

## 二、注意事项：
1.正则表达式中只需要支持单个字符来作为基本正则表达式，不需要支持命名。
2.用@表示空符号

## 三、环境说明：

python3.9

## 四、文件说明：
|----RegExp_conversion.py

|

|----main.py

|

|----hopcroft.py

|

|----实验2 DFA生成器.txt

## 五、数据说明：
测试案例位于RegExp_conversion.py开头的【expression】
已通过测试案例：
1、课件L03最后一题
2、midterm第一问

## 六、使用说明：
1、运行RegExp_conversion.py可以从正则表达式生成NFA，同时展示生成过程以及状态表。

2、hopcroft.py中运用hopcroft算法将NFA通过维护状态的
分割并使用快速查找机制来优化最小化过程。在这个文件中实现了将DFA状态最小化分割。函数generate_minimized_dfa传入DFA最小化状态的参数可以生成最小化DFA，print_minimized_dfa_table将最小化DFA状态表打印出来。

3、main.py主要接入前两个文件，可以将NFA，DFA，DFA最小化三个状态表打印出来。

4、需要tabulate、enum、pandas库

## 七、测试案例
Regular Expression: ab(((ba)*|bbb)*|a)*b
***        NFA TABLE        ***   
+-------+-----+-----+---------+
| state |  a  |  b  | epsilon |
+-------+-----+-----+---------+
|   0   |  1  | non |   non   |
|   1   | non | non |    2    |
|   2   | non |  3  |   non   |
|   3   | non | non |   24    |
|  24   | non | non |  25,22  |
|  23   | non | non |  25,22  |
|  22   | non | non |  18,20  |
|  19   | non | non |   23    |
|  21   | non | non |   23    |
|  18   | non | non |  19,16  |
|  17   | non | non |  19,16  |
|  16   | non | non |  8,10   |
|   9   | non | non |   17    |
|  15   | non | non |   17    |
|   8   | non | non |   9,4   |
|   7   | non | non |   9,4   |
|   4   | non |  5  |   non   |
|   5   | non | non |    6    |
|   6   |  7  | non |   non   |
|  10   | non | 11  |   non   |
|  11   | non | non |   12    |
|  12   | non | 13  |   non   |
|  13   | non | non |   14    |
|  14   | non | 15  |   non   |
|  20   | 21  | non |   non   |
|  25   | non | non |   26    |
|  26   | non | 27  |   non   |
+-------+-----+-----+---------+
Start state: 0
End state: 27

***   DFA TABLE   ***   
+-------+-----+-----+
| state |  a  |  b  |
+-------+-----+-----+
|   0   |  2  |  6  |
|   1   |  2  |  6  |
|   2   |  2  |  6  |
|   3   | non |  1  |
|   4   | non |  5  |
|   5   |  2  |  6  |
|   6   |  0  |  4  |
|   7   |  3  | non |
+-------+-----+-----+

***  Minimized DFA TABLE  ***
+---------+-----+-----+
| state   | b   | a   |
+=========+=====+=====+
| S0      | S4  | non |
+---------+-----+-----+
| S1      | S0  | S4  |
+---------+-----+-----+
| S2      | non | S3  |
+---------+-----+-----+
| S3      | S4  | non |
+---------+-----+-----+
| S4      | S1  | S4  |
+---------+-----+-----+
