class Words():
    def __init__(self):
        self.word = ""      #记录每一行的单词
        # 关键字表， 符号表， 变量表， 函数表， 数组表, 宏展开表
        self.keywords = {'auto': 1, 'short': 2, 'int': 3, 'long': 4, 'float': 5, 'double': 6, 'char': 7,
                         'struct': 8, 'unio': 9, 'enum': 10, 'typdef': 11, 'const': 12, 'unsigned': 13,
                         'signed': 14, 'extern': 15, 'register': 16, 'static': 17, 'volatile': 18,
                         'void': 19, 'if': 20, 'else': 21, 'switch': 22, 'case': 23, 'for': 24, 'd0': 25,
                         'while': 26, 'goto': 27, 'continue': 28, 'break': 29, 'default': 30, 'sizeof': 31,
                         'return': 32}
        self.symbols ={'+':1, '-':2, '*':3, '/':4, '%':5, '++':6, '--':7, '=':8, '+=': 9, '-=':10,
                        '*=':11, '/=':12, '%=':13, '==':14, '!=':15, '<':16, '>':17, '<=':18, '>=':19,
                        '&&':20, '||':21, '!':22, '&':23, '|':24, '~':24, '^':25, '<<':26, '>>':27, '//':28, '#':29,
                        '(':30, ')':31, '{':32, '}':33, ';':34, ',':35, '[':37, ']':38, '\\':39,"'":40, '"':41}
        self.myWords={}
        self.myFunctions={}
        self.myArrays={}
        self.myDefines={}
        # 变量编号wSyn, 函数编号fsyn, 数组编号asyn
        self.wSyn = 0
        self.fSyn = 0
        self.aSyn = 0
        self.i = 0  #记录字符下标
        self.line = 0   #记录行数


    def splitLine(self):                                            # 分行
        with open('test.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                self.line += 1
                self.word = line.strip()                            # 去掉回车和句首空格，预处理字符串
                self.analyzingWords()

    def Print(self, syn, s):                                        # 输出格式控制
        syn = str(syn)
        print("Line：{:3s} <<  {:20s},    {:20s}  >>".format(str(self.line), syn, s))

    def PrintD(self, s1, s2):                                       # 宏展开输出格式控制
        print("Line：{:3s} <<  {:18s}<---   {:20s}  >>".format(str(self.line), s1, s2))

    def isVariable(self, syn):                                      # 判断标志符，标志符处理函数
        s = ''
        while True:  # 循环内进行分词
            # 标志符的组成字母\数字\下划线
            if self.i >= len(self.word):
                break
            # 标志符的组成字母、数字、下划线
            if self.word[self.i].isalpha() or self.word[self.i].isdigit() or self.word[self.i] == '_':
                s += self.word[self.i]
                self.i += 1
            else:
                break

            # 区分标志符是保留字还是用户自定义
            # 保留字
            # -------------------------------------------------------------------------------------------------------
        if s in self.keywords:
            syn = self.keywords[s]
            self.Print('keyword' + str(syn), s)

            # 用户自定义标志符
            # -------------------------------------------------------------------------------------------------------
        else:
            if s in self.myDefines:
                self.PrintD(s, self.myDefines[s])
            # 函数名*************************************************************************************************
            # 判断标志符后继，并确保该标志符还未存储在变量中，防止出现将已存储在变量中的指针作为函数再一次存储
            elif self.word[self.i] == '(' and s not in self.myWords:  # i是不满足标志符而退出循环的下标，相当于超前扫描的字符
                if s not in self.myFunctions:  # s还未存储在函数表中
                    self.fSyn += 1
                    self.myFunctions[s] = self.fSyn  # 添加键值对，即存储该函数及其编号
                    self.Print('Function' + str(self.fSyn), s)
                else:
                    self.Print('Function' + str(self.myFunctions[s]), s)
            # 数组名*************************************************************************************************
            # 判断标志符后继，并确保该标志符还未存储在变量中，防止出现将已存储在变量中的指针作为数组再一次存储
            elif self.word[self.i] == '[' and s not in self.myWords:
                if s not in self.myArrays:
                    self.aSyn += 1
                    self.myArrays[s] = self.aSyn
                    self.Print('Array' + str(self.aSyn), s)
                else:
                    self.Print('Array' + str(self.myArrays[s]), s)
            # 变量名*************************************************************************************************
            else:
                if s not in self.myWords:  # 如果该标志符还未存储过
                    self.wSyn += 1  # 计数
                    self.myWords[s] = self.wSyn  # 向字典中添加键值对
                    self.Print('Variable' + str(self.wSyn), s)
                else:
                    self.Print('Variable' + str(self.myWords[s]), s)  # 如果已存储，直接输出它的信息
            # 存在不足：1、不能区分指针变量类型 2、不能区分全局变量或局部变量 3、不能单纯的以变量的后继是[、(就粗略认为是数组或函数

    def analyzingWords(self):                               # 对每一行进行分词
        syn = 0  # 编号
        self.i = 0
        s = ''  # 暂存标志符
        while True:
            s = ''
            if self.i >= len(self.word):  # 单词遍历完毕
                break

            # 该部分对字符串进行预处理，跳空格，过滤注释和预编译
            # **********************************************************************************************************
            elif self.word[self.i] == ' ':  # 遇到空格字符，跳到下一个字符
                self.i += 1
                continue
            elif self.word[self.i] == '/' and self.word[self.i + 1] == '/':
                break  # 判断是否出现'//'注释符，
            elif self.word[self.i:self.i + 7] == '#define':                         #判断是否出现宏定义
                self.myDefines[self.word.split(" ")[1]] = self.word.split(" ")[2]   #将改行以空格分割为各个单词，向宏表中添加宏
                self.PrintD(self.word.split(" ")[1], self.word.split(" ")[2])
                break;
            elif self.word[self.i] == '#':
                break

            # 该分支主要进行分词产生标志符，并区分是保留字还是用户自定义标志符
            # **********************************************************************************************************
            elif self.word[self.i].isalpha():  # 确保是以字母开头
                self.isVariable(syn)           # 调用标志符处理函数

            # 该部分分离常数
            # **********************************************************************************************************
            elif self.word[self.i].isdigit():
                while True:
                    if self.i >= len(self.word):
                        break
                    if self.word[self.i].isdigit() or self.word[self.i] == '.':
                        s += self.word[self.i]
                        self.i += 1
                    else:
                        break
                self.Print('Constant', s)
            # 该部分分离字符
            # **********************************************************************************************************************
            elif self.word[self.i] in self.symbols:
                if self.i < len(self.word) - 1:
                    s = self.word[self.i:self.i + 2]            #超前读入下一个字符
                if s in self.symbols:                           #先贪心判断是否是一个双目符号
                    syn = self.symbols[s]
                    self.Print('Symbols' + str(syn), s)
                    self.i += 2
                else:
                    syn = self.symbols[self.word[self.i]]
                    self.Print('Symbols' + str(syn), self.word[self.i])
                    self.i += 1
            else:          # 过滤无效字符
                print("line: " + str(self.line) +"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   出现非法字符:     " + self.word[self.i] + "   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                self.i += 1


if __name__ == '__main__':
    w = Words()
    w.splitLine()