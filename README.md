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

![屏幕截图 2024-12-06 141715](https://github.com/user-attachments/assets/9225f3d1-e566-4955-8c55-b7807f003c4d)

![image](https://github.com/user-attachments/assets/334c26d1-ffe7-4579-9274-401e7341b928)

