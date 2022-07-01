import sys                                    
code = sys.stdin.read().splitlines()


with open('test_case1.txt') as f:  # here test_case1.txt is an input file with assembly code
    code = f.read().splitlines()

listof_error = {
    "a": "Typos in instruction name or register name",
    "b": "Use of undefined variables",
    "c": "Use of undefined labels",
    "d": "Illegal use of FLAGS register",
    "e": "Illegal Immediate values",
    "f": "Misuse of labels as variables or vice-versa",
    "g": "Variables not declared at the beginning",
    "h": "Missing hlt instruction",
    "i": "hlt not being used as the last instruction",
    "j": "General Syntax Error"
}

register = {
    "R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"
}

registers = {
    "R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110"
}

operations = {
    "add": ['A', "10000"], 
    "sub": ['A', "10001"], 
    "mov1": ['B', "10010"],
    "mov2": ['C', "10011"], 
    "ld": ['D', "10100"], 
    "st": ['D', "10101"],
    "mul": ['A', "10110"], 
    "div": ['C', "10111"], 
    "rs": ['B', "11000"],
    "ls": ['B', "11001"], 
    "xor": ['A', "11010"], 
    "or": ['A', "11011"], 
    "and": ['A', "11100"],
    "not": ['C', "11101"], 
    "cmp": ['C', "11110"], 
    "jmp": ['E', "11111"], 
    "jlt": ['E', "01100"],
    "jgt": ['E', "01101"], 
    "je": ['E', "01111"], 
    "hlt": ['F', "01010"]
}


def decimaltobinary(n):
    n = int(n)
    binarycode=""
    while n>0:
        binarycode += str(n%2)
        n = int(n/2)
    binarycode[::-1]
    x="0"*(8-len(binarycode))
    finalcode=x+binarycode
    return finalcode


def typeA(value, r1, r2, r3):
    machinecode = operations[value][1] + "00" + register[r1] + register[r2] + register[r3]
    return machinecode


def typeB(value,r1,num):
    # y = bin(int(num))[2:]
    # x = "0"*(8-len(y)) + y
    x = decimaltobinary(num)
    machinecode=operations[value][1]+register[r1]+x

    return machinecode


def typeC(value, r1, r2):
    machinecode = operations[value][1]+"00000"+register[r1]+register[r2]

    return machinecode


def typeD(value, r1, var):
    # b = bin(variables[var])[2:]
    # mem_address = "0"*(8-len(b)) + b
    mem_address = decimaltobinary(variables[var])
    machinecode = operations[value][1]+register[r1]+mem_address

    return machinecode


def typeE(value, lbl):
    # b=bin(labels[lbl+":"])[2:]
    # mem_address = "0"*(8-len(b)) + b
    mem_address = decimaltobinary(labels[lbl + ":"])
    machinecode = operations[value][1] + "000" + mem_address

    return machinecode


def typeF(value):
    machinecode = operations[value][1] + "00000000000"

    return machinecode



# -------------------------------------------ALL ERRORS----------------------------------------------------------------------------

#typo in instruction, a
def typos(address, nameof_parameter, n):
    if(nameof_parameter not in operations.keys() and n == 1):
        print("Line number "+ str(address) +" has an error of type: " + listof_error["a"])
        exit()
    elif(nameof_parameter not in register.keys() and n==0):
        print("Line number "+ str(address) +" has an error of type: " + listof_error["a"])
        exit()

#undefined use of variables, b
def undef_variable(nameof_var):
    print("Line number "+str(address) +" has an error of type: " + listof_error["b"] + " " + nameof_var)
    exit()

#undefined use of labels, c
def undef_label(address, nameof_var):
    print("Line number "+str(address) +" has an error of type: " + listof_error["c"] + " " + nameof_var)
    exit()

# illegal use of flags, d
def illegal_flags(address):
    print("Line number "+str(address) +" has an error of type: " + listof_error.error["d"])
    exit()

#illegal value (greater than 8 bits), e
def illegal_immvalue(address, immval):
    if(immval>255 or immval<0):
        print("Line number "+str(address) +" has an error of type: " + listof_error.error["e"])
        exit()

#label def as var ; var def as label, f
def label_var(address, name, n):
    if(name not in label) and n==1:
        if(name in variable):
            print("Line number "+str(address) +" has an error of type: " + listof_error["f"])
            exit()
    
    if(name not in variable) and n==0:
        if(name in label):
            print("Line number "+str(address) +" has an error of type: " + listof_error["f"])
            exit()

#variable not defined in the beginning, g
def notdefvariable_beg(address):
    print("Line number "+str(address) +" has an error of type: " + listof_error["g"])
    exit()

#halt missing, h
def miss_halt(address):
    print("Line number "+str(address) +" has an error of type " + listof_error["h"])
    exit()

#last line not halt, i
def lastnot_hlt():
    # print("Code has an error of type" + listof_error["i"])
    print("Line number "+str(line_number) +" has an error of type " + listof_error["i"])
    exit()

#General error, j
def generalError(address):
    print("Line number "+str(address) +" has an error of type " + listof_error["j"])
    exit()

# Variable check 
def errorVariables(flag, line):
    if flag:
        if len(line) == 2:
            if line[1] not in variable:
                variable.append(line[1])
            else:
                generalError(line_number)
        else:
            generalError(line_number)
    else:
        notdefvariable_beg(line_number)



variable = []
label = {}

var_flag = True
hlt_flag = True
assembly = {} 
line_number = 0


# This 'for' loop mainly checks for all the error
for line in code:

    line_list = list(line.split())

    if len(line_list) == 0:
        continue

    line_number += 1

    if line_list[0] == "var" :
        errorVariables(var_flag, line_list)
        continue
    else:
        var_flag = False


    if hlt_flag == False:
        lastnot_hlt()


    if "FLAGS" in line_list:
        if line_list[0] == "mov" and line_list[1] == "FLAGS" and line_list[2] in registers:
            pass
        else:
            illegal_flags(line_number)

    if line_list[0]=="mov":
        if line_list[2][0]=="$":
            line_list[0]="mov1"
        else:
            line_list[0]="mov2"


    assembly[line_number] = line_list


    if line_list[0][-1] == ":" :
        if line_list[0:-1] not in label:
            label[line_list[0][0:-1]] = [True, line_number]
            line_list.pop(0)
        else:
            generalError(line_number)


    if line_list[0] in operations.keys():

        if operations[line_list[0]][0] == "A":
            for i in range(1, len(line_list)):
                typos(line_number, line_list[i], 0)


        elif operations[line_list[0]][0]=="B":
            typos(line_number, line_list[1], 0)
            if line_list[2][0] != "$":
                generalError(line_number)
            illegal_immvalue(line_number, int(line_list[2][1:]))


        elif operations[line_list[0]][0]=="C":
            for i in range(1, len(line_list)):
                typos(line_number, line_list[i], 0)


        elif operations[line_list[0]][0]=="D":
            typos(line_number, line_list[1], 0)
            label_var(line_number, line_list[2], 0)

            if line_list[2] not in variable:
                undef_variable(line_list[2])


        elif operations[line_list[0]][0]=="E":
            label_var(line_number, line_list[1], 1)

            if line_list[1] not in label:
                label[line_list[1]] = [False, line_number]


        elif operations[line_list[0]][0]=="F":
            if hlt_flag == False:
                lastnot_hlt()
            hlt_flag = False
    

    else:
        typos(line_number, line_list[0], 1)


# Check is there was hlt instruction at last
if hlt_flag ==True:
    miss_halt(line_number)


# Check for undefined variables
for i in label:
    if label[i][0] == False:
        undef_label(i)




# -------------------------------------------PRINTING STARTS----------------------------------------------------------------------------

labels = {}
variables = {}


t=0
address=0


for line in code:
    if len(line) == 0:
        continue
    line_list = list(line.split())
    
    if (line_list[0] in operations):
        address += 1

    if (line_list[0] == "hlt"):
        labels[line_list[0]+":"] = address
        address += 1

    if (line_list[0][-1] == ":"):
        address += 1
        labels[line_list[0]] = address
        

for line in code:
    if (len(line) == 0):
        continue
    line_list = list(line.split())
    if line_list[0] == "var" and len(line_list) == 2:
        t+=1
        variables[line_list[1]]=t+address




for line in code:
    if(len(line)==0):
        continue

    line_list = list(line.split())

    if( len(line_list)>1 and line_list[0] in labels and line_list[1] in operations):
        line_list.pop(0)
    
    if line_list[0]=="mov":
        if line_list[2][0]=="$":
            line_list[0]="mov1"
        else:
            line_list[0]="mov2"

    if line_list[0] in operations.keys():

        if operations[line_list[0]][0]=="A":
            
            print(typeA(line_list[0],line_list[1],line_list[2],line_list[3]))

        elif operations[line_list[0]][0]=="B":
            
            print(typeB(line_list[0],line_list[1],line_list[2][1:]))
        
        elif operations[line_list[0]][0]=="C":
            
            print(typeC(line_list[0],line_list[1],line_list[2]))

        elif operations[line_list[0]][0]=="D":
            
            print(typeD(line_list[0],line_list[1], line_list[2]))

        elif operations[line_list[0]][0]=="E":
            
            print(typeE(line_list[0], line_list[1]))

        elif operations[line_list[0]][0]=="F":
            
            print(typeF(line_list[0]))