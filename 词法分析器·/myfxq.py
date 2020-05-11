#保留字列表
key = ['program', 'var', 'int', 'const', 'begin', 'end', 'if', 'then', 'while', 'do', 'read', 'write']

#把每行字符串分词
def lexicalAnalyze(wordlist):
    s = ''      #单词
    syn = 0     #标号
    i = 0       #字符串索引
    for word in wordlist:
        if word == ' ':             #若为空格则判断下一个字符
            i += 1
            continue
        else:
            if i >= len(wordlist):  #防止i越界
                break
            elif i < len(wordlist)-1:
                if wordlist[i] + wordlist[i+1] == "//":
                    continue
            elif wordlist[i] >= 'a' and wordlist[i] <= 'z':     #判断该字符串首字母是否是字母(即判断该字符串是否是标志符）
                for word in wordlist:   # 遍历该字符串
                    if i >= len(wordlist):  # 防止i越界
                        break
                    # 分割出一个合法的标志符
                    elif (wordlist[i] >= 'a' and wordlist[i] <= 'z') or (wordlist[i] >= '0' and wordlist[i] <= '9'):
                        s += wordlist[i]        #将标志符记录在s
                        i += 1                  #索引滚动
                    else:
                        break
                for keyword in key:                 #检查该标志符是不是保留字，查取标志符列表
                    if s == keyword:
                        syn = key.index(s) + 1      #是保留字， 并返回该标志符的编号
                        break
                    else:                           #是标识符，编号13
                        syn = 13
                lexicalPrint(syn, s)
                s = ''                              #将串置空
            elif wordlist[i] >= '0' and wordlist[i] <= '9':         #判断是否为常数
                for word in wordlist:
                    if i >= len(wordlist):  # 防止i越界
                        break
                    elif wordlist[i] >= '0' and wordlist[i] <= '9' or wordlist[i] == '.':
                        s += wordlist[i]
                        i += 1
                    else:
                        break
                syn = 14
                lexicalPrint(syn, s)
                s = ''
            #判断是否为其他字符
            elif wordlist[i] == '+':
                s += wordlist[i]
                i += 1
                syn = 15
                lexicalPrint(syn, s)
                s = ''
            elif wordlist[i] == '-':
                s += wordlist[i]
                i += 1
                syn = 16
                lexicalPrint(syn, s)
                s = ''
            elif wordlist[i] == '*':
                s += wordlist[i]
                i += 1
                syn = 17
                lexicalPrint(syn, s)
                s = ''
            elif wordlist[i] == '/':
                s += wordlist[i]
                i += 1
                syn = 18
                lexicalPrint(syn, s)
                s = ''
            elif wordlist[i] == ':':
                s += wordlist[i]
                i += 1
                if wordlist[i] == '=':
                    s += wordlist[i]
                    i += 1
                    syn = 20
                else:
                    syn = 19
                lexicalPrint(syn, s)
                s = ''
            elif wordlist[i] == '=':
                s += wordlist[i]
                i += 1
                syn = 21
                lexicalPrint(syn, s)
                s = ''
            elif wordlist[i] == '>':
                s += wordlist[i]
                i += 1
                if wordlist[i] == '=':
                    s += wordlist[i]
                    i += 1
                    syn = 23
                else:
                    syn = 22
                lexicalPrint(syn, s)
                s = ''
            elif wordlist[i] == '<':
                s += wordlist[i]
                i += 1
                if wordlist[i] == '=':
                    s += wordlist[i]
                    i += 1
                    syn = 25
                elif wordlist[i] == '>':
                    s += wordlist[i]
                    i += 1
                    syn = 26
                else:
                    syn = 24
                lexicalPrint(syn, s)
                s = ''
            elif wordlist[i] == '(':
                s += wordlist[i]
                i += 1
                syn = 27
                lexicalPrint(syn, s)
                s = ''
            elif wordlist[i] == ')':
                s += wordlist[i]
                i += 1
                syn = 28
                lexicalPrint(syn, s)
                s = ''
            elif wordlist[i] == '{':
                s += wordlist[i]
                i += 1
                syn = 29
                lexicalPrint(syn, s)
                s = ''
            elif wordlist[i] == '}':
                s += wordlist[i]
                i += 1
                syn = 30
                lexicalPrint(syn, s)
                s = ''
            elif wordlist[i] == ',':
                s += wordlist[i]
                i += 1
                syn = 31
                lexicalPrint(syn, s)
                s = ''
            elif wordlist[i] == ';':
                s += wordlist[i]
                i += 1
                syn = 32
                lexicalPrint(syn, s)
                s = ''
            elif wordlist[i] == '#':
                s += wordlist[i]
                syn = 0
                lexicalPrint(syn, s)
                print('碰到#号，结束程序！')
                break

#控制输出格式
def lexicalPrint(syn, s):
    syn = str(syn)
    print('<' + syn + ',' + "              "+ s+"      " + '>')

#将测试文件按行读取
def lexicalInput():
    with open('test.txt', 'r') as f:
        for line in f.readlines():
            wordlist = line.strip()         #去掉回车和句首空格
            lexicalAnalyze(wordlist)        #每一行都作分词处理

lexicalInput()