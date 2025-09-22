import memoryLib

def main():
    memory = None
    while True:
        input_ = input(f"{memory.getName() + ' ' if memory != None else ''}>>> ")
        if input_ == 'exit': break
        if input_.startswith('init'):
            try:
                memory = memoryLib.memory(input_.split(' ')[1], int(input_.split(' ')[2]), int(input_.split(' ')[3]))
            except IndexError: print("The amount of arguments for this command is 4")
        if input_.startswith('select'): 
            try:
                memory = memoryLib.memory(input_.split(' ')[1], 2, 2); memory.fetchMemory() # ambiguous x and y used, set true size during fetch
            except IndexError: print("The amount of arguments for this command is 2")
        if input_.startswith('get'): 
            try:
                print(memory.getValue(input_.split(' ')[1]))
            except IndexError: print("The amount of arguments for this command is 2")
        if input_.startswith('set'): 
            try:
                memory.setValue(input_.split(' ')[1], input_.split(' ')[2])
            except IndexError: print("The amount of arguments for this command is 3")
        if input_ == 'print': memory.printMemory()
        if input_ == 'save': memory.saveMemory()
        if input_ == 'fetch': memory.fetchMemory()

if __name__ == '__main__': main()