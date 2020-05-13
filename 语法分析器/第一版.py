import os
class Words(str):
    def __init__(self, str):    # 构造函数
        self.word = ""  # 记录每一行的单词
        self.str = str
        self.i = 0  # 记录字符下标
        self.line = 0  # 记录行数


        self.Vt = []  # 记录文法中的终结符
        self.Vn = []  # 记录文法中的非终结符
        self.record = {}  # 记录文法中的具体情况，是一个字典的形式，键为左边的非终结符，值为右边的推导式内容。可以理解为这就是文法
        self.flag = True  # 该值反应某一推导式是否会出现两个连续的非终结符，即文法是否是算符优先文法
        self.pflag = True
        self.firstvt = {}  # 记录该文法的firstvt集，字典形式，键值对表示某非终结符的firstvt集
        self.lastvt = {}  # 记录文法的lastvt集， 字典形式， 键值对表示某非终结符的lastvt集
        self.precedenceMatrix = {}  # 算符优先矩阵

    def splitLine(self):  # 将文法的每个推导式分离出来
        with open('test3', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                self.line += 1
                self.word = line.strip()  # 去掉回车和句首空格，预处理字符串
                self.analyzingWords()

    def getFirstvt(self):
        stack = []  # 这是一个栈数据结构
        # 这是19页ppt的步骤（2）（3）----------------------------------------------------------------------
        print('\n\n\n'+'*' * 160)
        print('\t\t\tFIRSTVT集的栈出栈入栈情况')
        for key, value in self.record.items():  # 遍历文法
            firstvt = []  # firstvt中存储形如U->b…或U->Vb的产生式
            for str in value:
                if str:
                    if str[0] in self.Vt:
                        stack.append([key, str[0]])
                        firstvt.append(str[0])
                    elif len(str) > 1 and str[1] in self.Vt:
                        stack.append([key, str[1]])
                        firstvt.append(str[1])
            self.firstvt[key] = firstvt
        print(stack)
        # 步骤（4）---------------------------------------------------------------------------------------
        while stack:
            l = stack.pop()
            print('\t\t\t出栈：  <---' + l[0] + '   ' + l[1] + '---->')
            for key, value in self.record.items():
                for str in value:
                    if str and l[0] == str[0] and str[0] in self.Vn:
                        if l[1] not in self.firstvt[key]:  # 即判断出栈的非终结符V，是否存在推导式U->V，即v是否在U的value里
                            print('\t\t\t入栈：  ' + '--->' + key + '   ' + l[1] + '<----')
                            stack.append([key, l[1]])  # 如果存在根据步骤4，将key, l[1]入栈，并将F[U，b]置一，即存入self.firstvt
                            self.firstvt[key] += l[1]


    def getLastvt(self):
        stack = []  # 这是一个栈数据结构
        # 这是19页ppt的步骤（2）（3）----------------------------------------------------------------------
        print('*' * 160)
        print('\t\t\tLATSTVT集的栈出栈入栈情况')
        for key, value in self.record.items():  # 遍历文法
            lastvt = []  # firstvt中存储形如U->b…或U->Vb的产生式
            for str in value:
                if str:
                    length = len(str)
                    if str[-1] in self.Vt:
                        stack.append([key, str[-1]])
                        lastvt.append(str[-1])
                    elif length > 1 and str[length-2] in self.Vt:
                        stack.append([key, str[length-2]])
                        lastvt.append(str[length-2])
            self.lastvt[key] = lastvt
        print(stack)
        # 步骤（4）---------------------------------------------------------------------------------------
        while stack:
            l = stack.pop()
            print('\t\t\t出栈：  <---' + l[0] + '   ' + l[1] + '---->')
            for key, value in self.record.items():
                for str in value:
                    if str and l[0] == str[-1] and str[-1] in self.Vn:
                        if l[1] not in self.lastvt[key]:
                            print('\t\t\t入栈   --->' + key + '   ' + l[1] + '<----')
                            stack.append([key, l[1]])
                            self.lastvt[key] += l[1]

    def getprecedenceMatrix(self):  # 建立运算符优先关系字典
        for value in self.record.values():  # 遍历所有的产生式建立优先关系字典
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
                            if last + '  ' + str[i + 1] in self.precedenceMatrix.keys():
                                self.pflag = False
                                break
                            else:
                                self.precedenceMatrix[last + '  ' + str[i + 1]] = '>'
                    elif i + 1 < len(str) and str[i] in self.Vt:  # 该字符如果是终结符在前，即 FIRSTVT(str[i+1]) < str[i]
                        for first in self.firstvt[str[i + 1]]:
                            if str[i] + '  ' + first in self.precedenceMatrix.keys():
                                self.pflag = False
                                break
                            else:
                                self.precedenceMatrix[str[i] + '  ' + first] = '<'
                    i += 1
                for index1 in range(len(list)):
                    for index2 in range(index1 + 1, len(list)):
                        self.precedenceMatrix[list[index1] + ' ' + list[index2]] = '='
        for first in self.firstvt[self.Vn[0]]:
            self.precedenceMatrix['#  ' + first] = '<'
        for last in self.lastvt[self.Vn[0]]:
            self.precedenceMatrix[last + '  #'] = '>'
        self.precedenceMatrix['#  #'] = '='

    def IsOPG(self):
        if self.pflag and self.flag:
            print("\t\t\t\tYES!")
        else:
            print("\t\t\t\tNO!")

    def reduction(self, l):
        fmt = '{{:{}}}{{:{}}}'.format(50, 5)
        left = ''.join(l)
        flag = False
        for key, value in self.record.items():
            for n in value:
                n = list(n)
                if n == l:
                    print(fmt.format(left, key))
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
        for key, value in self.record.items():
            for n in value:
                n = list(n)
                if n == l:
                    print(fmt.format(left, key))
                    return key

    def isLeft(self):
        s = ['#']
        k = 0
        str = self.str[1:]
        str = str[::-1]
        str = list(str)
        while True:
            while True:
                a = str.pop()
                if a in self.Vn:
                    s.append(a)
                    k += 1
                else:
                    break
            if s[k] in self.Vt:  # 确保s[j]是一个非终结符
                j = k
            else:
                j = k - 1
            while self.precedenceMatrix[s[j] + '  ' + a] == '>':
                while True:
                    q = s[j]
                    if s[j - 1] in self.Vt:
                        j -= 1
                    else:
                        j -= 2
                    if self.precedenceMatrix[s[j] + '  ' + q] == '<':
                        break
                left = []
                for i in range(k - j):
                    left.append(s.pop())
                left = left[::-1]
                k = j + 1
                N = []
                N = self.reduction(left)
                s += N
            if self.precedenceMatrix[s[j] + '  ' + a] == '<' or self.precedenceMatrix[s[j] + '  ' + a] == '=':
                k += 1
                s.append(a)
            if a == '#':
                break

    def IsOP(self):
        if self.flag:
            print('\t\t\t\tYES')
        else:
            print('\t\t\t\tNO')

    def analyzingWords(self):
        self.i = 1
        record = ''
        flag = True
        while True:

            if self.i >= len(self.word):
                break
            if self.word[self.i: self.i + 2] == "->":
                self.i += 2
            else:
                if 'A' <= self.word[self.i] <= 'Z':
                    record += self.word[self.i]
                    if self.word[self.i] not in self.Vn:
                        self.Vn.append(self.word[self.i])
                    self.i += 1
                    # 判断是否是算符文法，即是否出现两个连续的非终结符
                    if self.i < len(self.word) and 'A' <= self.word[self.i] <= 'Z':
                        flag = False
                elif self.word[self.i] != ' ' and self.word[self.i] != '@':
                    record += self.word[self.i]
                    if self.word[self.i] != '|' and self.word[self.i] not in self.Vt:
                        self.Vt.append(self.word[self.i])
                    self.i += 1
                else:
                    self.i += 1
        self.record[self.word[0]] = record.split('|')
        self.flag = self.flag & flag

from tkinter import *


class Menue():
    def wOPG(self):
        print('*' * 160)
        print('*文法：', end='   ')
        print(self.word.record)
        print('*' * 160)

    def wFirst(self):
        self.word.getFirstvt()
        print('*'*160)
        print('*文法的FIRSTVT集：', end = '   ')
        print(self.word.firstvt)
        print('*'*160)

    def wLast(self):
        print('\n\n\n')
        self.word.getLastvt()
        print('*' * 160)
        print('*文法的LASTVT集：', end='   ')
        print(self.word.lastvt)
        print('*' * 160)

    def wVn(self):
        print('\n\n\n'+'*' * 160)
        print('*文法的Vn集：', end='   ')
        print(self.word.Vn)
        print('*' * 160)

    def wVt(self):
        print('\n\n\n'+'*' * 160)
        print('*文法的Vt集：', end='   ')
        print(self.word.Vt)
        print('*' * 160)

    def wPrecedence(self):
        print('\n\n\n' + '*' * 160)
        print('算符优先字典')
        self.word.getprecedenceMatrix()
        print(self.word.precedenceMatrix)
        print('*' * 160)

    def wIsleft(self):
        print('\n\n\n' + '*' * 160)
        print('\t\t\t\t\t\t归约处 理')
        fmt = '{{:{}}}{{:{}}}'.format(45, 5)
        print(fmt.format('最左素短语', '归约符号'))
        self.word.isLeft()
        print('*' * 160)

    def wIsOPG(self):
        print('\n\n\n' + '*' * 160)
        self.word.IsOPG()
        print('*' * 160)

    def wIsOP(self):
        print('\n\n\n' + '*' * 160)
        self.word.IsOP()
        print('*' * 160)

    def center_window(self, width, height):
        screenwidth = self.window.winfo_screenwidth()
        screenheight = self.window.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        print(size)
        self.window.geometry(size)

    def __init__(self,str):
        self.window = Tk()     # 主菜单界面
        self.center_window( 300, 240)
        Label(self.window, text='语法分析器', font = 'Helvetica -12 bold').pack(side=TOP)    # 创建一个标签并应用布局管理器
        form = Frame(self.window)
        form.pack()
        entries = {}
        Button(form, text='处理后的文法', font='Helvetica -12 bold', command=(lambda: self.wOPG())).pack(expand=YES, fill=X)
        Button (form, text='Vn集', font = 'Helvetica -12 bold', command=(lambda : self.wVn())).pack( expand=YES, fill=X)
        Button(form, text='Vt集', font='Helvetica -12 bold', command=(lambda: self.wVt())).pack( expand=YES,fill=X)
        Button(form, text='算符文法', font='Helvetica -12 bold', command=(lambda: self.wIsOP())).pack(expand=YES, fill=X)
        Button(form, text='FIRSTVT集', font = 'Helvetica -12 bold', command=(lambda: self.wFirst())).pack(expand=YES, fill=X)
        Button(form, text='LASTVT集', font = 'Helvetica -12 bold', command=(lambda: self.wLast())).pack( expand=YES, fill=X)
        Button(form, text='算符优先字典', font='Helvetica -12 bold', command=(lambda: self.wPrecedence())).pack(expand=YES, fill=X)
        Button(form, text='是否算符优先文法', font='Helvetica -12 bold', command=(lambda: self.wIsOPG())).pack(expand=YES, fill=X)
        Button(form, text='归约处理', font='Helvetica -12 bold', command=(lambda: self.wIsleft())).pack(expand=YES,fill=X)
        self.word = Words(str)
        self.word.splitLine()
        self.window.mainloop()     # 开始事件循环


if __name__ == '__main__':
    str = input()
    m = Menue(str)
