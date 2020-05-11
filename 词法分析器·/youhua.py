#保留字列表
keywords={'auto':1, 'short': 2,  'int':3, 'long':4, 'float':5, 'double': 6, 'char':7,
          'struct':8, 'unio':9, 'enum':10, 'typdef':11, 'const':12, 'unsigned':13,
          'signed':14, 'extern': 15, 'register':16, 'static':17, 'volatile':18,
          'void': 19, 'if':20, 'else':21, 'switch':22, 'case':23, 'for':24, 'd0':25,
          'while':26, 'goto':27, 'continue':28, 'break':29, 'default':30, 'sizeof':31,
          'return':32}

symbols ={'+':1, '-':2, '*':3, '/':4, '%':5, '++':6, '--':7, '=':8, '+=': 9, '-=':10,
          '*=':11, '/=':12, '%=':13, '==':14, '!=':15, '<':16, '>':17, '<=':18, '>=':19,
          '&&':20, '||':21, '!':22, '&':23, '|':24, '~':24, '^':25, '<<':26, '>>':27, '//':28, '#':29,
          '(':30, ')':31, '{':32, '}':33, ';':34}

mywords={}

#记录变量个数
syn_2 = -1


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
            elif i <= len(wordlist)-1: #判断该行是否是注释,如果是则结束本行
                if word == "//" or word == '#':
                    break
                elif wordlist[i] >= 'A' and wordlist[i] <= 'z':     #判断该字符串首字母是否是字母(即判断该字符串是否是标志符）
                    while True:   # 死循环内进行分词
                        if i >= len(wordlist):  # 防止i越界
                            break
                        # 分割出一个合法的标志符
                        elif (wordlist[i] >= 'A' and wordlist[i] <= 'z') or (wordlist[i] >= '0' and wordlist[i] <= '9'):
                            s += wordlist[i]        #将标志符记录在s
                            i += 1                  #
                        else:
                            break
                    for keyword in keywords:                 #检查该标志符是不是保留字，查取标志符列表
                        if s == keyword:
                            syn = keywords[s]     #是保留字， 并返回该标志符的编号
                            break
                        else:                           #是标识符，编号13
                            if s not in mywords:
                                global syn_2
                                syn_2 = syn_2+1
                                syn = '变量' + str(syn_2)
                                mywords[s] = syn = 'Variable'+ str(syn_2)
                            else:
                                syn=mywords[s]
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
                    lexicalPrint('Constant', s)
                    s = ''
                #判断是否为其他字符
                elif word in symbols:
                    i = i + word.__len__();
                    syn = symbols[word]
                    lexicalPrint('Symbol'+str(syn), word)
                    s = ''


#控制输出格式
def lexicalPrint(syn, s):
    syn = str(syn)
    print(" <<  {:10s},    {:20s}  >>" .format(syn,s))

#将测试文件按行读取
def lexicalInput():
    with open('test.txt', 'r',encoding='utf-8') as f:
        for line in f.readlines():
            wordlist = line.strip()         #去掉回车和句首空格
            lexicalAnalyze(wordlist)        #每一行都作分词处理

lexicalInput()