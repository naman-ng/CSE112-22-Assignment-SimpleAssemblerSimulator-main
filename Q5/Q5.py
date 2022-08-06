import math

cellsize={1:1,2:4,3:8,4:16}

def choices():
    print('''1. Bit Addressable Memory 
2. Nibble Addressable Memory 
3. Byte Addressable Memory 
4. Word Addressable Memory ''')

def space_in():
    mem=input("Enter space in memory: ")
    space_mem=mem.split()
    if space_mem[1]=="Mb":
        x=float(space_mem[0])*1024*1024
        space_mem[0]=x
    if space_mem[1]=="MB":
        x=float(space_mem[0])*1024*1024*8
        space_mem[0]=x
    if space_mem[1]=="Kb":
        x=float(space_mem[0])*1024
        space_mem[0]=x
    if space_mem[1]=="KB":
        x=float(space_mem[0])*1024*8
        space_mem[0]=x
    if space_mem[1]=="Gb":
        x=float(space_mem[0])*1024*1024*1024*8
        space_mem[0]=x
    if space_mem[1]=="GB":
        x=float(space_mem[0])*1024*1024*1024*8
        space_mem[0]=x
    return space_mem

#main

while(True):
    print("Queries:")
    print('''1. ISA and Instructions related.
2. System enhancement related.
3. Exit.''')
    query=int(input("Enter query: "))
    if query==1:
        space_mem=space_in()
        choices()
        n=int(input("Enter choice: "))
        lengthofinst=int(input("Length of one instruction: "))
        lengthofreg=int(input("Length of register: "))
        l=math.log2(float(space_mem[0])/cellsize[n])
        P=math.ceil(l)
        Q=lengthofinst-P-lengthofreg
        R=lengthofinst-Q-(2*lengthofreg)
        no_of_inst=2**Q
        no_of_reg=2**lengthofreg
        print(f'{P} bits are needed to represent an address in this architecture ')
        print(f'{Q} bits needed by opcode')
        print(f'{R} filler bits required in instruction tyoe 2')
        print(f'Maximum numbers of instructions this ISA can support is {no_of_inst}')
        print(f'Maximum number of registers this ISA can support is {no_of_reg}')

    elif query==2:
        print("Type 1 or Type 2: ")
        type=int(input("Enter type: "))
        if type==1:
            space_mem=space_in()
            choices()
            n=int(input("Enter choice: "))
            l=math.log2(float(space_mem[0])/cellsize[n])
            P=math.ceil(l)
            cpubits=int(input("Enter CPU bits: "))
            choices()
            n2=int(input("Enter the memory type you want to enhance (from rest 3): "))
            cellsize[4]=cpubits
            l2=math.log2(float(space_mem[0])/cellsize[n2])
            P2=math.ceil(l2)
            print()
            print(f"{P2-P} address pins are required or saved.")
        if type==2:
            cpubits=int(input("Enter the bit that CPU support :"))
            adrresspins=int(input("Enter no. of address pins: "))
            choices()
            n=int(input("Enter Type of addressable memory: "))
            cellsize[4]=cpubits
            main_mem=((2**(adrresspins))*cellsize[n])/(2**33)
            print(f"The main memory is {main_mem} GB or {main_mem*1024*1024*1024} Bytes")
    
    elif query==3:
        break

    else:
        print("Wrong input.")
        break