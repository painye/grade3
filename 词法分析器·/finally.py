
#全局变量////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#保留字字典
keywords={'auto':1, 'short': 2,  'int':3, 'long':4, 'float':5, 'double': 6, 'char':7,
          'struct':8, 'unio':9, 'enum':10, 'typdef':11, 'const':12, 'unsigned':13,
          'signed':14, 'extern': 15, 'register':16, 'static':17, 'volatile':18,
          'void': 19, 'if':20, 'else':21, 'switch':22, 'case':23, 'for':24, 'd0':25,
          'while':26, 'goto':27, 'continue':28, 'break':29, 'default':30, 'sizeof':31,
          'return':32}

#符号字典
symbols ={'+':1, '-':2, '*':3, '/':4, '%':5, '++':6, '--':7, '=':8, '+=': 9, '-=':10,
          '*=':11, '/=':12, '%=':13, '==':14, '!=':15, '<':16, '>':17, '<=':18, '>=':19,
          '&&':20, '||':21, '!':22, '&':23, '|':24, '~':24, '^':25, '<<':26, '>>':27, '//':28, '#':29,
          '(':30, ')':31, '{':32, '}':33, ';':34, ',':35, '[':37, ']':38, '\\':39,"'":40, '"':41}

#用户自定义变量名字典
mywords={}

# 函数名字典
myFunctions={}

# 数组名字典
myArrays={}

myDefines={}

#记录变量个数
fSyn = 0
wSyn = 0
aSyn = 0


######### 词法分析函数////////////////////////////////////////////////////////////////////////////////////////////////////
def lexicalAnalyze(word):
    syn = 0                                     # 编号
    i = 0                                       # 遍历字符串索引
    s = ''                                      # 暂存标志符
    while True:
        s = ''
        if i>=len(word):                    # 单词遍历完毕
            break

        # 该部分对字符串进行预处理，跳空格，过滤注释和预编译
        #***********************************************************************************************************************
        elif word[i] == ' ':                # 遇到空格字符，跳到下一个字符
            i += 1
            continue
        elif i<=len(word)-1 and word[i]=='/' and word[i+1] == '/':
            break                               # 判断是否出现'//'注释符，第一个条件保证超前读取不会越界
        elif word[i:i+7] == '#define':
            myDefines[word.split(" ")[1]] = word.split(" ")[2]
            PrintD(word.split(" ")[1], word.split(" ")[2])
            break;

        elif word[i] == '#':                # 判断是否出现'#'注释符，若是则直接结束本行的分词
            break

        # 该分支主要进行分词产生标志符，并区分是保留字还是用户自定义标志符
        # **********************************************************************************************************************
        elif word[i].isalpha():             # 确保是以字母开头
            while True:                         # 循环内进行分词
                # 标志符的组成字母\数字\下划线
                if i >= len(word):
                    break
                # 标志符的组成字母、数字、下划线
                if word[i].isalpha() or word[i].isdigit() or word[i] == '_':
                    s += word[i]
                    i += 1
                else:
                    break

                # 区分标志符是保留字还是用户自定义
                # 保留字
                #-------------------------------------------------------------------------------------------------------
            if s in keywords:
                syn = keywords[s]
                Print('keyword'+str(syn), s)

                # 用户自定义标志符
                #-------------------------------------------------------------------------------------------------------
            else:
                if i >= len(word):
                    break
                if s in myDefines:
                    PrintD(s, myDefines[s])
                # 函数名*************************************************************************************************
                elif word[i] == '(' and s not in mywords:                 # i是不满足标志符而退出循环的下标，相当于超前扫描的字符
                    if s not in myFunctions:                            # s还未存储在函数表中
                        global fSyn                                     # 全局变量为函数编号
                        fSyn += 1
                        myFunctions[s] = fSyn                           # 添加键值对，即存储该函数及其编号
                        Print('Function' + str(fSyn), s)
                    else :
                        Print('Function' + str(myFunctions[s]), s)
                # 数组名*************************************************************************************************
                elif word[i] == '['  and s not in mywords:
                    if s not in myArrays:
                        global  aSyn
                        aSyn +=1
                        myArrays[s] = aSyn
                        Print('Array' + str(aSyn), s)
                    else:
                        Print('Array' + str(myArrays[s]), s)
                # 变量名*************************************************************************************************
                else:
                    if s not in mywords:                                    # 如果该标志符还未存储过
                        global wSyn                                         # 需要使用一个全局变量来排序
                        wSyn += 1                                           # 计数
                        mywords[s] = wSyn                                   # 向字典中添加键值对
                        Print('Variable' + str(wSyn), s)
                    else:
                        Print('Variable' + str(mywords[s]), s)              # 如果已存储，直接输出它的信息
                # 存在不足：1、不能区分指针变量类型 2、不能区分全局变量或局部变量 3、不能单纯的以变量的后继是[、(就粗略认为是数组或函数

        # 该部分分离常数
        # **************************************************************************************************************
        elif word[i].isdigit():
            while True:
                if i >= len(word):
                    break
                if word[i].isdigit() or word[i] == '.':
                    s += word[i]
                    i += 1
                else:
                    break
            Print('Constant', s)
        # 该部分分离字符
        # **********************************************************************************************************************
        elif word[i] in symbols:
            if i<len(word)-1 :
                s = word[i:i+2]
            if s in symbols:
                syn = symbols[s]
                Print('Symbols'+str(syn), s)
                i += 2
            else:
                syn = symbols[word[i]]
                Print('Symbols'+str(syn), word[i] )
                i += 1
        else:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   出现非法字符:     " + word[i]+"   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            i += 1


#控制输出格式
def Print(syn, s):
    syn = str(syn)
    print(" <<  {:20s},    {:20s}  >>" .format(syn,s))

def PrintD(s1, s2):
    print(" <<  {:18s}<---   {:20s}  >>".format(s1,s2))

#将测试文件按行读取
if __name__ == '__main__':
    with open('test.txt', 'r',encoding='utf-8') as f:
        for line in f.readlines():
            wordlist = line.strip()         #去掉回车和句首空格，预处理字符串
            lexicalAnalyze(wordlist)        #每一行都作分词处理
