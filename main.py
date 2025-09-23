import memoryLib

def main():
    memory = None
    while True:
        input_ = input(f"{memory.getName() + ' ' if memory != None else ''}>>> ")
        if input_ == 'exit': memory.exit(); break
        elif input_.startswith('init'):
            try:
                memory = memoryLib.memory(input_.split(' ')[1], int(input_.split(' ')[2]), int(input_.split(' ')[3]))
                print(f"Memory '{input_.split(' ')[1]}' initiated with size {input_.split(' ')[2]}x{input_.split(' ')[3]}")
            except IndexError: print("The amount of arguments for this command is 4")
        elif input_.startswith('select'): 
            try:
                memory = memoryLib.memory(input_.split(' ')[1], 2, 2)  # ambiguous x and y used, set true size during fetch
                if memory.fetchMemory() == 0: memory = None; print("Memory not found in the log")
                else: print(f"Memory '{input_.split(' ')[1]}' selected")
            except IndexError: print("The amount of arguments for this command is 2")
        elif input_.startswith('getval'): 
            try:
                print(f"Value at {input_.split(' ')[1]}: {memory.getValue(input_.split(' ')[1])}")
            except IndexError: print("The amount of arguments for this command is 2")
        elif input_.startswith('setval'): 
            try:
                memory.setValue(input_.split(' ')[1], input_.split(' ')[2])
                print(f"Value at {input_.split(' ')[1]} set to {memory.getValue(input_.split(' ')[1])}")
            except IndexError: print("The amount of arguments for this command is 3")
        elif input_.startswith('freeval'): 
            try:
                memory.freeValue(input_.split(' ')[1])
                print(f"Value at {input_.split(' ')[1]} freed")
            except IndexError: print("The amount of arguments for this command is 2")
        elif input_ == 'print': memory.printMemory()
        elif input_ == 'save': memory.saveMemory()
        elif input_ == 'fetch': memory.fetchMemory()
        elif input_.startswith('malloc'): 
            try:
                print(f'Memory pointer: {memory.malloc(int(input_.split(" ")[1]))}')
            except IndexError: print("The amount of arguments for this command is 2")
        elif input_.startswith('get'):
            try:
                print(f"Malloc variable at {input_.split(' ')[1]}: {memory.get(input_.split(' ')[1])}")
            except IndexError: print("The amount of arguments for this command is 2")
        elif input_.startswith('set'):
            try:
                if memory.set(input_.split(' ')[1], input_.split(' ')[2]) == 0: continue
                print(f"Malloc variable at {input_.split(' ')[1]} set to {memory.get(input_.split(' ')[1])}")
            except IndexError: print("The amount of arguments for this command is 3")
        elif input_.startswith('free'):
            try:
                memory.free(input_.split(' ')[1])
                print(f"Malloc memory at {input_.split(' ')[1]} freed")
            except IndexError: print("The amount of arguments for this command is 2")
        elif input_ == 'clear': memory.clear()
        elif input_ == 'help':
            print('Available commands:')
            print('init (name) (x size) (y size) - initiate an empty memory of name and size')
            print('select (name) - select a memory from the log')
            print('getval (key) - get value of the current working memory at hexadecimal key')
            print('setval (key) (value) - set value of the current working memory at hexadecimal key')
            print('freeval (key) - free the memory at the position of the key')
            print('print - print the current working memory')
            print('save - save the current working memory')
            print('fetch - fetch the memory from the log')
            print('exit - exit the program')
            print('malloc (size) - allocate memory in the current working memory, returning a pointer to the first character of the variable')
            print('get (malloc key) - get value of entire variable at the malloc key location')
            print('set (malloc key) - set value of entire "variable" at the malloc key location')
            print('free (malloc key) - free a whole variable from the memory')
        else: print("Invalid command, for help type 'help'")

if __name__ == '__main__': main()