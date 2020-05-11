
class Words():
    def __init__(self):
        self.word = ""      #记录每一行的单词
        # 运算符表，用来匹配问法中出现的合法的运算符
        self.symbols ={'+':1, '-':2, '*':3, '/':4, '%':5, '++':6, '|':7, '=':8, '+=': 9, '-=':10,
                        '*=':11, '/=':12, '%=':13, '==':14, '!=':15, '<':16, '>':17, '<=':18, '>=':19,
                        '&&':20, '||':21, '!':22, '&':23,  '~':24, '^':25, '<<':26, '>>':27, '//':28, '#':29,
                        '(':30, ')':31, '{':32, '}':33, ';':34, ',':35, '[':37, ']':38, '\\':39,"'":40, '"':41, "->": 42}

        self.i = 0                          # 记录字符下标
        self.line = 0                       # 记录行数
        self.Vt = []                        # 记录文法中的终结符
        self.Vn = []                        # 记录文法中的非终结符
        self.record = {}                    # 记录文法中的具体情况，是一个字典的形式，键为左边的非终结符，值为右边的推导式内容。可以理解为这就是文法
        self.mySymbol = []                  # 记录文法中出现的运算符
        self.flag = True                    # 该值反应某一推导式是否会出现两个连续的非终结符，即文法是否是算符优先文法
        self.firstvt = {}                   # 记录该文法的firstvt集，字典形式，键值对表示某非终结符的firstvt集
        self.lastvt = {}                    # 记录文法的lastvt集， 字典形式， 键值对表示某非终结符的lastvt集
        self.precedenceMatrix = {}          # 算符优先矩阵


    def splitLine(self):                                            # 将文法的每个推导式分离出来
        with open('test.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                self.line += 1
                self.word = line.strip()                            # 去掉回车和句首空格，预处理字符串
                self.analyzingWords()


    def Print(self):                        # 输出格式控制
        print(self.Vn)                      # 输出非终结符
        print(self.Vt)                      # 输出终结符
        print(self.mySymbol)                # 输出运算符
        print(self.record)                  # 输出文法记录
        print(self.flag)                    # 输出是否算符文法
        print(self.firstvt)
        print(self.lastvt)
        self.getprecedenceMatrix()
        for key, value in self.precedenceMatrix.items():
            print('['+key+']'+':'+value)




    '''def getFirstvt(self):                      # 获得p的FIRSTVT（）集
        l = list(self.record.keys())
        l.reverse()
        for key in l:
            firstvt = []
            value = self.record[key]
            for str in value:
                if str not in self.Vn:
                    for c in str:
                        if c not in self.Vn:
                            firstvt.append(c)
                            break
                elif str in self.firstvt.keys():
                    firstvt += self.firstvt[str]
            self.firstvt[key] = firstvt'''

    def getFirstvt(self):
        stack = []                                          # 这是一个栈数据结构
        # 这是19页ppt的步骤（2）（3）----------------------------------------------------------------------
        for key, value in self.record.items():              # 遍历文法
            firstvt = []                                    # firstvt中存储形如U->b…或U->Vb的产生式
            for str in value:
                for c in str:
                    if c not in self.Vn:                    # 判断c是不是非终结符，是的话入栈，结束循环
                        stack.append([key, c])
                        firstvt.append(c)
                        break
            self.firstvt[key] = firstvt
        print(stack)
        # 步骤（4）---------------------------------------------------------------------------------------
        while stack:
            l = stack.pop()
            print('出栈：  <---'+ l[0] + '   ' + l[1] + '---->')
            for key, value in self.record.items():
                if l[0] in value:
                    if l[1] not in self.firstvt[key]:       # 即判断出栈的非终结符V，是否存在推导式U->V，即v是否在U的value里
                        print('入栈：  '+'--->' + key + '   ' + l[1] + '<----')
                        stack.append([key, l[1]])           # 如果存在根据步骤4，将key, l[1]入栈，并将F[U，b]置一，即存入self.firstvt
                        self.firstvt[key] += l[1]


    def getLastvt(self):
        stack = []                                          # 这是一个栈数据结构
        # 这是19页ppt的步骤（2）（3）----------------------------------------------------------------------
        for key, value in self.record.items():              # 遍历文法
            lastvt = []                                    # firstvt中存储形如U->b…或U->Vb的产生式
            for str in value:
                for c in str[::-1]:
                    if c not in self.Vn:
                        stack.append([key, c])
                        lastvt.append(c)
                        break
            self.lastvt[key] = lastvt
        print(stack)
        # 步骤（4）---------------------------------------------------------------------------------------
        while stack:
            l = stack.pop()
            print('出栈：  <---'+ l[0] + '   ' + l[1] + '---->')
            for key, value in self.record.items():
                if l[0] in value:
                    if l[1] not in self.lastvt[key]:
                        print('入栈   --->' + key + '   ' + l[1] + '<----')
                        stack.append([key, l[1]])
                        self.lastvt[key] += l[1]


    def getprecedenceMatrix(self):                                      # 建立运算符优先关系字典
        for value in self.record.values():                                # 遍历所有的产生式建立优先关系字典
            for str in value:
                i = 0  # 产生式字符串下标
                while True:
                    if i >= len(str):  # 索引超限，退出循环
                        break
                    if i + 1 < len(str) and str[i] in self.Vn:  # 该字符如果非终结符在前，即 LASTVT(str[i]) >  str[i+1]
                        for last in self.lastvt[str[i]]:
                            self.precedenceMatrix[str[i] +'  '+ str[i + 1]] = '>'
                    elif i + 1 < len(str) and str[i] in self.Vt:  # 该字符如果是终结符在前，即 FIRSTVT(str[i+1]) < str[i]
                        for first in self.firstvt[str[i + 1]]:
                            self.precedenceMatrix[str[i] - str[i + 1]] = '<'
                    i += 1



    def analyzingWords(self):
        self.i = 1
        record = ''
        flag = True
        while True:

            if self.i >= len(self.word):
                break

            if self.word[self.i] in self.symbols:
                if self.word[self.i : self.i+2] == "->":
                    self.i += 2
                else:
                    record += self.word[self.i]
                    if self.word[self.i] not in self.mySymbol:
                         self.mySymbol.append(self.word[self.i])
                    self.i += 1
            else:
                if self.word[self.i] >= 'A' and self.word[self.i] <= 'Z':
                    record += self.word[self.i]
                    if self.word[self.i] not in self.Vn:
                        self.Vn.append(self.word[self.i])
                    self.i += 1
                    # 判断是否是算符文法，即是否出现两个连续的非终结符
                    if self.i <  len(self.word) and self.word[self.i] >= 'A' and self.word[self.i] <= 'Z':
                        flag = False
                elif self.word[self.i] >= 'a' and self.word[self.i] <= 'z':
                    record += self.word[self.i]
                    if self.word[self.i] not in self.Vt:
                        self.Vt.append(self.word[self.i])
                    self.i += 1
                else:
                    self.i += 1
        self.record[self.word[0]] = record.split('|')
        self.flag = self.flag & flag






if __name__ == '__main__':
    w = Words()
    w.splitLine()
    w.getFirstvt()
    w.getLastvt()
    w.Print()