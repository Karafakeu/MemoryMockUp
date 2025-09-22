import memoryLib

def main():
    memory = None
    while True:
        input_ = input(f"{memory.getName() + ' ' if memory != None else ''}>>> ")
        if input_ == 'exit': break
        elif input_.startswith('init'):
            try:
                memory = memoryLib.memory(input_.split(' ')[1], int(input_.split(' ')[2]), int(input_.split(' ')[3]))
            except IndexError: print("The amount of arguments for this command is 4")
        elif input_.startswith('select'): 
            try:
                memory = memoryLib.memory(input_.split(' ')[1], 2, 2)  # ambiguous x and y used, set true size during fetch
                if memory.fetchMemory() == 0: memory = None
            except IndexError: print("The amount of arguments for this command is 2")
        elif input_.startswith('get'): 
            try:
                print(memory.getValue(input_.split(' ')[1]))
            except IndexError: print("The amount of arguments for this command is 2")
        elif input_.startswith('set'): 
            try:
                memory.setValue(input_.split(' ')[1], input_.split(' ')[2])
            except IndexError: print("The amount of arguments for this command is 3")
        elif input_ == 'print': memory.printMemory()
        elif input_ == 'save': memory.saveMemory()
        elif input_ == 'fetch': memory.fetchMemory()
        elif input_ == 'help':
            print('Available commands:')
            print('init (name) (x size) (y size) - initiate an empty memory of name and size')
            print('select (name) - select a memory from the log')
            print('get (key) - get value of the current working memory at hexadecimal key')
            print('set (key) (value) - set value of the current working memory at hexadecimal key')
            print('print - print the current working memory')
            print('save - save the current working memory')
            print('fetch - fetch the memory from the log')
        else: print("Invalid command, for help type 'help'")

if __name__ == '__main__': main()