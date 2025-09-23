import ast

class memory():
    def __init__(self, name, x, y):
        self.name = name
        self.x, self.y = x, y
        self.change = False
        self.memory = {}
        self.free_memory = [f"0x{hex(i)[2:].zfill(8)}" for i in range(x * y)]
        self.p_memory = self.initMemory(x, y)
        self.next_malloc = f"0x{hex((x * y))[2:].zfill(8)}"
        self.current_malloc = {}

    def initMemory(self, x, y): return [['' for j in range(x)] for i in range(y)]
    
    def getName(self): return self.name

    def getValue(self, key):
        """
        Returns the value stored in the memory at the given key.

        - empty key: returns None
        - hexadecimal key: '0x' followed by a hexadecimal number

        Returns None if the key is invalid or out of range of the memory.
        """

        if key == '' or key == '0x' or key == None:
            print("Invalid key: empty key!")
            return

        # invalid key type
        if key[0:2] != '0x':
            print("Invalid key type!")
            return 
        
        try:
            return self.memory[key]
        except KeyError:
            print("Memory place does not contain any value.")
            return

    def setValue(self, key, value):
        if key == '' or key == '0x' or key == None:
            print("Invalid key: empty key!")
            return 0
        
        # invalid key type
        if key[0:2] != '0x':
            print("Invalid key type!")
            return 0
        
        if key not in self.free_memory:
            print("Memory address is not free, free it first")
            return 0

        try:
            self.memory[key] = value
            self.change = True
            self.free_memory.remove(key)
            return 1
        except IndexError:
            print("Memory index is out of range of the memory!")
            return 0

    def get(self, key):
        if key == '' or key == '0x' or key == None:
            print("Invalid key: empty key!")
            return 0
        
        # invalid key type
        if key[0:2] != '0x':
            print("Invalid key type!")
            return 0
        
        # key not in malloc memory
        if key not in self.current_malloc.keys():
            print("Memory address is not allocated, allocate it first")
            return 0
        
        # get the value
        result = ''
        for mem_key in self.current_malloc[key][1]:
            try:
                result += self.memory[mem_key]
            except KeyError:
                result += ''

        return result

    def set(self, key, value):
        if key == '' or key == '0x' or key == None:
            print("Invalid key: empty key!")
            return 0
        
        # invalid key type
        if key[0:2] != '0x':
            print("Invalid key type!")
            return 0
        
        # key not in malloc memory
        if key not in self.current_malloc.keys():
            print("Memory address is not allocated, allocate it first")
            return 0
        
        if len(value) != self.current_malloc[key][0]:
            print("Invalid value length, must be of length " + str(self.current_malloc[key][0]))
            return 0
        
        # set the value
        for i in range(len(self.current_malloc[key][1])):
            mem_key = self.current_malloc[key][1][i]
            try:
                self.memory[mem_key] = value[i]
                self.change = True
            except KeyError:
                print("Memory index is out of range of the memory!")
                return 0

        return 1

    def printMemory(self):
        if self.change: # change has been made, must convert memory to p_memory
            self.memoryConvert('MTP')

        for i in range(len(self.p_memory)):
            print(self.p_memory[i])

        for key in self.current_malloc.keys():
            print(f"malloc( {key} ): {self.current_malloc[key][1]}")

        return 1
    
    def saveMemory(self, force = False):
        global new

        if self.change: # change has been made, must convert memory to p_memory
            self.memoryConvert('MTP')

        with open("memoryLog.txt", 'r') as f:
            # check if the memory log exists
            if f.readlines().count(f"{self.name}:\n") == 0: new = True
            else: new = False
            f.close()

        # save current memory into the log
        # simply add the memory to the log
        if new:
            with open("memoryLog.txt", 'a') as f:
                f.write(f"{self.name}:\n")
                for i in range(len(self.p_memory)):
                    f.write(str(self.p_memory[i]) + "\n")
                f.write("\n")
                f.close()
                
        # replace the memory in the log
        else:
            if not force:
                if input("Are you sure you want to replace the memory in the log? (y/n): ") != 'y': return 0
            writing, count, targetLine, futureLines = True, True, 0, []
            with open("memoryLog.txt", 'r') as f:
                lines = f.readlines()
                f.close()
            
            for line in lines:
                if writing:
                    if line == f"{self.name}:\n":
                        futureLines.append(line)
                        writing = False
                    else:
                        futureLines.append(line)
                        if count: targetLine += 1
                else:
                    if line == '\n':
                        futureLines.append(line)
                        writing, count = True, False
            
            with open("memoryLog.txt", 'w') as f:
                f.writelines(futureLines)
                f.close()

            with open("memoryLog.txt", 'r') as f:
                lines = f.readlines()
                f.close()

            lines.insert(targetLine + 1, str(self.current_malloc) + "\n")
            
            for memLine in self.p_memory[::-1]:
                lines.insert(targetLine + 1, str(memLine) + "\n")

            with open("memoryLog.txt", 'w') as f:
                f.writelines(lines)
                f.close()

        print(f"Memory {self.name} saved successfully!")

        return 1

    def fetchMemory(self):
        fetch, fetching = [], False

        with open("memoryLog.txt", 'r') as f:
            lines = f.readlines()
            f.close()
        
        for line in lines:
            if fetching:
                if line == '\n':
                    fetching = False
                else:
                    fetch.append(ast.literal_eval(line))
            if line == f"{self.name}:\n":
                fetching = True

        if fetch == []: return 0

        if type(fetch[-1]) == dict:
            self.current_malloc = fetch[-1]
            fetch = fetch[:-1]
        
        self.p_memory = fetch
        x, y = len(self.p_memory), len(self.p_memory[0])
        self.x, self.y = x, y
        self.free_memory = [f"0x{hex(i)[2:].zfill(8)}" for i in range(self.x * self.y)]
        self.next_malloc = f"0x{hex((self.x * self.y))[2:].zfill(8)}"
        self.memoryConvert('PTM')

        print(f"Memory {self.name} fetched successfully!")

        return 1

    def memoryConvert(self, mode):
        if mode == 'MTP': # memory to print memory
            self.p_memory = self.initMemory(self.x, self.y)
            for i in range(self.x * self.y):
                try:
                    self.p_memory[i // self.x][i % self.x] = self.memory[f"0x{hex(i)[2:].zfill(8)}"]
                except KeyError:
                    self.p_memory[i // self.x][i % self.x] = ''

        elif mode == 'PTM': # print memory to memory
            self.memory = {}
            for y in range(len(self.p_memory)):
                for x in range(len(self.p_memory[y])):
                    if self.p_memory[y][x] != '': self.memory[f"0x{hex(y * self.x + x)[2:].zfill(8)}"] = self.p_memory[y][x]; self.free_memory.remove(f"0x{hex(y * self.x + x)[2:].zfill(8)}")

        else:
            print("Invalid mode!")
            return 0

        return 1

    def malloc(self, size):
        self.change = True
        size = int(size)

        if size <= 0:
            print("Cannot allocate memory, size must be greater than 0")
            return 0

        if size > len(self.free_memory):
            print("Cannot allocate memory, not enough space")
            return 0 
        
        current_pointer = self.next_malloc

        # assign the memory
        self.current_malloc[current_pointer] = (size, [self.free_memory[i] for i in range(size)])
        self.free_memory = self.free_memory[size:]

        # find the next free malloc
        counter = 1
        while True:
            self.next_malloc = f"0x{hex(int(self.next_malloc[2:], 16) + counter)[2:].zfill(8)}"
            counter += 1
            if self.next_malloc not in self.current_malloc.keys(): break
            
        return current_pointer

    def freeValue(self, address):
        if address in self.memory.keys():
            del self.memory[address]

        self.change = True
        for i in range(len(self.free_memory)):
            if i == len(self.free_memory) - 1: self.free_memory.insert(i + 1, address); break
            if int(self.free_memory[i][2:], 16) > int(address[2:], 16):
                self.free_memory.insert(i, address); break
            
        return 1
    
    def free(self, address):
        self.change = True

        # remove values from memory
        for addr in self.current_malloc[address][1]: self.freeValue(addr)

        # remove from malloc
        if address in self.current_malloc.keys():
            del self.current_malloc[address]
        else:
            print("Memory place does not contain any value.")
            return 0

        # assign the next malloc
        if int(self.next_malloc[2:], 16) > int(address[2:], 16):
            self.next_malloc = address

        return 1
    
    def clear(self):
        self.memory = {}
        self.free_memory = [f"0x{hex(i)[2:].zfill(8)}" for i in range(self.x * self.y)]
        self.p_memory = self.initMemory(self.x, self.y)
        self.next_malloc = f"0x{hex((self.x * self.y))[2:].zfill(8)}"
        self.current_malloc = {}
        self.change = True

        print(f"Memory {self.name} cleared successfully!")

        return 1
    
    def exit(self, force = False):
        if self.change and not force:
            if input("Memory has unsaved changed, save before exit? (y/n): ") == 'y': self.saveMemory()
            else: print("Memory not saved, exiting...")
        
        return 1
    
    def switch(self, force = False):
        if self.change and not force:
            if input("Memory has unsaved changed, save before switch? (y/n): ") == 'y': self.saveMemory()
            else: print("Memory not saved, switching...")

        return 1

def command_handler(command, current_memory = None, force = False):
    if command == 'exit': 
        try:
            current_memory.exit(force)
        except AttributeError: pass
        return 0
    elif command.startswith('init'):
        try:
            try:
                current_memory.switch(force)
            except AttributeError: pass
            current_memory = memory(command.split(' ')[1], int(command.split(' ')[2]), int(command.split(' ')[3]))
            print(f"Memory '{command.split(' ')[1]}' initiated with size {command.split(' ')[2]}x{command.split(' ')[3]}")
            return current_memory
        except IndexError: print("The amount of arguments for this command is 4")
    elif command.startswith('select'): 
        try:
            try:
                current_memory.switch(force)
            except AttributeError: pass
            current_memory = memory(command.split(' ')[1], 2, 2)  # ambiguous x and y used, set true size during fetch
            if current_memory.fetchMemory() == 0: current_memory = None; print("Memory not found in the log")
            else: print(f"Memory '{command.split(' ')[1]}' selected")
            return current_memory
        except IndexError: print("The amount of arguments for this command is 2")
    elif command.startswith('getval'): 
        try:
            value = current_memory.getValue(command.split(' ')[1])
            print(f"Value at {command.split(' ')[1]}: {value}")
            return value
        except IndexError: print("The amount of arguments for this command is 2")
        except AttributeError: print("No memory selected")
    elif command.startswith('setval'): 
        try:
            current_memory.setValue(command.split(' ')[1], command.split(' ')[2])
            print(f"Value at {command.split(' ')[1]} set to {current_memory.getValue(command.split(' ')[1])}")
        except IndexError: print("The amount of arguments for this command is 3")
        except AttributeError: print("No memory selected")
    elif command.startswith('freeval'): 
        try:
            current_memory.freeValue(command.split(' ')[1])
            print(f"Value at {command.split(' ')[1]} freed")
        except IndexError: print("The amount of arguments for this command is 2")
        except AttributeError: print("No memory selected")
    elif command == 'print': 
        try:
            current_memory.printMemory()
        except AttributeError: print("No memory selected")
    elif command == 'save': 
        try:
            current_memory.saveMemory(force)
        except AttributeError: print("No memory selected")
    elif command == 'fetch': 
        try:
            current_memory.fetchMemory()
        except AttributeError: print("No memory selected")
    elif command.startswith('malloc'): 
        try:
            print(f'Memory pointer: {current_memory.malloc(int(command.split(" ")[1]))}')
        except IndexError: print("The amount of arguments for this command is 2")
        except AttributeError: print("No memory selected")
    elif command.startswith('get'):
        try:
            value = current_memory.get(command.split(' ')[1])
            print(f"Malloc variable at {command.split(' ')[1]}: {value}")
            return value
        except IndexError: print("The amount of arguments for this command is 2")
        except AttributeError: print("No memory selected")
    elif command.startswith('set'):
        try:
            if current_memory.set(command.split(' ')[1], command.split(' ')[2]) == 0: return 1
            print(f"Malloc variable at {command.split(' ')[1]} set to {current_memory.get(command.split(' ')[1])}")
        except IndexError: print("The amount of arguments for this command is 3")
        except AttributeError: print("No memory selected")
    elif command.startswith('free'):
        try:
            current_memory.free(command.split(' ')[1])
            print(f"Malloc memory at {command.split(' ')[1]} freed")
        except IndexError: print("The amount of arguments for this command is 2")
        except AttributeError: print("No memory selected")
    elif command == 'clear': 
        try:
            current_memory.clear()
        except AttributeError: print("No memory selected")
    elif command == 'help':
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
