
class Words(str):
    def __init__(self, str):
        self.word = ""      #记录每一行的单词
        self.str = str
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
            print('['+key+']'+':'+value, end = ' ')
        print()
        self.isLeft()


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
                list = []
                while True:
                    if i >= len(str):  # 索引超限，退出循环
                        break
                    if str[i] in self.Vt:
                        list.append(str[i])
                    if i + 1 < len(str) and str[i] in self.Vn:  # 该字符如果非终结符在前，即 LASTVT(str[i]) >  str[i+1]
                        for last in self.lastvt[str[i]]:
                            self.precedenceMatrix[last +'  '+ str[i+1]] = '>'
                    elif i + 1 < len(str) and str[i] in self.Vt:  # 该字符如果是终结符在前，即 FIRSTVT(str[i+1]) < str[i]
                        for first in self.firstvt[str[i + 1]]:
                            self.precedenceMatrix[str[i] +'  '+ first] = '<'
                    i += 1
                for index1 in range(len(list)):
                    for index2 in range(index1+1,len(list)):
                        self.precedenceMatrix[list[index1] + ' ' + list[index2]] = '='
        for first in self.firstvt[self.Vn[0]]:
            self.precedenceMatrix['#  '+first] = '<'
        for last in self.lastvt[self.Vn[0]]:
            self.precedenceMatrix[last + '  #'] = '>'
        self.precedenceMatrix['#  #'] = '='


    def reduction(self, l):
        flag = False
        for key,value in self.record.items():
            for n in value:
                n = list(n)
                if n == l:
                    print(l)
                    return key
        for j in range(len(l)):
            for key, value in self.record.items():
                for n in value:
                    if n == l[j]:
                        l[j] = key
                        flag = True
                        break
                if flag:
                    break
            if flag:
                break
        for key,value in self.record.items():
            for n in value:
                n = list(n)
                if n == l:
                    print(l)
                    return key


    def isLeft(self):
        s = ['#']
        k = 0
        str = self.str[1:]
        str = str[::-1]
        str = list(str)
        while True :
            while True:
                a = str.pop()
                if a in self.Vn:
                    s.append(a)
                    k += 1
                else:
                    break
            if s[k] in self.Vt:         # 确保s[j]是一个非终结符
                j = k
            else:
                j = k-1
            while self.precedenceMatrix[s[j]+'  '+a] == '>':
                while True:
                    q = s[j]
                    if s[j-1] in self.Vt:
                        j -= 1
                    else:
                        j -= 2
                    if self.precedenceMatrix[s[j]+'  '+q]== '<':
                        break
                left = []
                for i in range(k-j):
                    left.append(s.pop())
                left = left[::-1]
                k = j+1
                N = []
                N=self.reduction(left)
                s += N
                print(s)
            if self.precedenceMatrix[s[j]+'  '+a] == '<' or self.precedenceMatrix[s[j]+'  '+a] == '=':
                k += 1
                s.append(a)
            if a == '#':
                break
        print(s)


    def analyzingWords(self):
        self.i = 1
        record = ''
        flag = True
        while True:

            if self.i >= len(self.word):
                break
            if self.word[self.i : self.i+2] == "->":
                self.i += 2
            else:
                if self.word[self.i] >= 'A' and self.word[self.i] <= 'Z':
                    record += self.word[self.i]
                    if self.word[self.i] not in self.Vn:
                        self.Vn.append(self.word[self.i])
                    self.i += 1
                    # 判断是否是算符文法，即是否出现两个连续的非终结符
                    if self.i <  len(self.word) and self.word[self.i] >= 'A' and self.word[self.i] <= 'Z':
                        flag = False
                elif self.word[self.i] != ' ':
                    record += self.word[self.i]
                    if self.word[self.i] != '|' and self.word[self.i] not in self.Vt:
                        self.Vt.append(self.word[self.i])
                    self.i += 1
                else:
                    self.i += 1
        self.record[self.word[0]] = record.split('|')
        self.flag = self.flag & flag


if __name__ == '__main__':
    str = '#T+T*F+i+F#'
    print(str)
    w = Words(str)
    w.splitLine()
    w.getFirstvt()
    w.getLastvt()
    w.Print()