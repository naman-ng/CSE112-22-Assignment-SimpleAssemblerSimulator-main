import sys                                    
code = sys.stdin.read().splitlines()

# with open('test_case1.txt') as f:  # here test_case1.txt is an input file with assembly code
#     code = f.read().splitlines()

variable = []
label = {}
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

#typo in instruction, a
def typos(address, nameof_parameter):
    if(nameof_parameter not in operations.keys() and nameof_parameter not in register.keys()):
        print("Line number "+ str(address) +" has an error of type: " + listof_error["a"])
        exit()

#undefined use of variables, b
def undef_variable(nameof_var):
    print(nameof_var + ": " + listof_error["b"])
    exit()

#undefined use of labels, c
def undef_label(nameof_var):
    print(nameof_var + ": " + listof_error["c"])
    exit()

#illegal value (greater than 8 bits), e
def illegal_immvalue(address, immval):
    if(immval>255 or immval<0):
        print("Line number"+str(address) +"has an error of type" + listof_error.error["e"])
        exit()

#label def as var ; var def as label, f
def label_var(address, nameof_label,nameof_var):
    if(nameof_label not in label):
        if(nameof_label in variable):
            print("Line number"+str(address) +"has an error of type" + listof_error["f"])
            exit()
    
    if(nameof_var not in variable):
        if(nameof_var in label):
            print("Line number"+str(address) +"has an error of type" + listof_error["f"])
            exit()

#variable not defined in the beginning, g
def notdefvariable_beg(address):
    print("Line number"+str(address) +"has an error of type" + listof_error["g"])
    exit()

#halt missing, h
def miss_halt(address, immval):
    if(immval>255 or immval<0):
        print("Line number"+str(address) +"has an error of type" + listof_error["h"])
        exit()

#last line not halt, i
def lastnot_hlt():
    print("Code has an error of type" + listof_error["i"])
    exit()

def generalError():
    print(listof_error["j"])

def errorVariables(flag, line):
    if flag:
        if len(line) == 2:
            if line[1] not in variable:
                variable.append(line[1])
        else:
            print(listof_error["j"])
    else:
        notdefvariable_beg(line_number)



var_flag = True
hlt_flag = True
assembly = {}
line_number = 0

for line in code:
    line_list = list(line.split())
    if len(line_list) == 0:
        continue

    line_number += 1
    assembly[line_number] = line_list


    if line_list[0] == "var" :
        errorVariables(var_flag, line_list)
        variable.append(line_list[1])
        continue


    if line_list[0] == "hlt" and hlt_flag == False:
        lastnot_hlt()


    if line_list[0]=="mov":
        if line_list[2][0]=="$":
            line_list[0]="mov1"
        else:
            line_list[0]="mov2"


    assembly[line_number] = line_list


    if line_list[0][-1]== ":" :
        label[line_list[0][0:-1]] = True
        line_list.remove(line_list[0])

    if line_list[0] in operations.keys():

        if operations[line_list[0]][0] == "A":
            for i in range(1, len(line_list)):
                typos(line_number, line_list[i])

        elif operations[line_list[0]][0]=="B":
            typos(line_number, line_list[1])
            if line_list[2][0] != "$":
                generalError()
            illegal_immvalue(line_number, int(line_list[2][1:]))

        elif operations[line_list[0]][0]=="C":
            for i in range(1, len(line_list)):
                typos(line_number, line_list[i])

        elif operations[line_list[0]][0]=="D":
            typos(line_number, line_list[1])
            if line_list[2] not in variable:
                undef_variable(line_list[2])

        elif operations[line_list[0]][0]=="E":
            if line_list[1] not in label:
                # undef_variable(line_number)
                label[line_list[1]] = False


        elif operations[line_list[0]][0]=="F":
            if hlt_flag == False:
                lastnot_hlt()
            hlt_flag = False
    
    else:
        typos(line_number, line_list[0])

# print(assembly)

for i in label:
    if label[i] == False:
        undef_label(i)


labels = {}
variables = {}


t=0
address=0


for line in code:
    if len(line)==0:
        continue
    value = list(line.split())
    
    if(value[0] in operations):
        address+=1

    if value[0]=="hlt":
        labels[value[0]+":"]=address
        address += 1

    if(value[0][-1]==":"):
        address+=1
        labels[value[0]]=address
        

for line in code:
    if(len(line)==0):
        continue
    value = list(line.split())
    if value[0]=="var" and len(value)==2:
        t+=1
        variables[value[1]]=t+address




for line in code:
    if(len(line)==0):
        continue

    value = list(line.split())
    if( len(value)>1 and value[0] in labels and value[1] in operations):
        value.pop(0)
    
    if value[0]=="mov":
        if value[2][0]=="$":
            value[0]="mov1"
        else:
            value[0]="mov2"

    if value[0] in operations.keys():

        if operations[value[0]][0]=="A":
            
            print(typeA(value[0],value[1],value[2],value[3]))

        elif operations[value[0]][0]=="B":
            
            print(typeB(value[0],value[1],value[2][1:]))
        
        elif operations[value[0]][0]=="C":
            
            print(typeC(value[0],value[1],value[2]))

        elif operations[value[0]][0]=="D":
            
            print(typeD(value[0],value[1], value[2]))

        elif operations[value[0]][0]=="E":
            
            print(typeE(value[0], value[1]))

        elif operations[value[0]][0]=="F":
            
            print(typeF(value[0]))