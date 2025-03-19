import ast

class memory():
    def __init__(self, name, x, y):
        self.name = name
        self.x, self.y = x, y
        self.change = False
        self.memory = {}
        self.free_memory = [f"0x{hex(i)[2:].zfill(8)}" for i in range(x * y)]
        self.print_memory = self.initMemory(x, y)

    def initMemory(self, x, y): return [['' for j in range(x)] for i in range(y)]
    
    def getName(self): return self.name

    def getValue(self, key):
        """
        Returns the value stored in the memory at the given key.

        Accepts different types of keys:

        - empty key: returns None
        - hexadecimal key: '0x' followed by a hexadecimal number
        - decimal key: a string or int representing a decimal number

        Returns None if the key is invalid or out of range of the memory.
        """

        if key == '' or key == '0x' or key == None:
            print("Invalid key: empty key!")
            return

        # hexadecimal key
        if key[0:2] == '0x': pass

        # decimal key
        elif type(key) == str:
            try:
                key = hex(key)
            except ValueError:
                print("Invalid key: invalid decimal key!")
                return

        # invalid key type
        else:
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
            return

        # hexadecimal key
        if key[0:2] == '0x': pass

        # decimal key
        elif type(key) == str:
            try:
                key = hex(key)
            except ValueError:
                print("Invalid key: invalid decimal key!")
                return

        # invalid key type
        else:
            print("Invalid key type!")
            return

        try:
            self.memory[key] = value
            self.change = True
        except IndexError:
            print("Memory index is out of range of the memory!")
            return

    def printMemory(self):
        if self.change: # change has been made, must convert memory to print_memory
            self.memoryConvert('MTP')

        for i in range(len(self.print_memory)):
            print(self.print_memory[i])
        return
    
    def saveMemory(self):
        global new

        if self.change: # change has been made, must convert memory to print_memory
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
                for i in range(len(self.print_memory)):
                    f.write(str(self.print_memory[i]) + "\n")
                f.write("\n")
                f.close()
                
        # replace the memory in the log
        else:
            if input("Are you sure you want to replace the memory in the log? (y/n): ") != 'y': return
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
            
            for memLine in self.print_memory[::-1]:
                lines.insert(targetLine + 1, str(memLine) + "\n")

            with open("memoryLog.txt", 'w') as f:
                f.writelines(lines)
                f.close()

        return

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

        self.print_memory = fetch
        self.memoryConvert('PTM')
        return

    def memoryConvert(self, mode):
        if mode == 'MTP': # memory to print memory
            self.print_memory = self.initMemory(self.x, self.y)
            for i in range(self.x * self.y):
                try:
                    self.print_memory[i // self.x][i % self.x] = self.memory[f"0x{hex(i)[2:].zfill(8)}"]
                except KeyError:
                    self.print_memory[i // self.x][i % self.x] = ''
            self.change = False

        elif mode == 'PTM': # print memory to memory
            self.memory = {}
            for y in range(len(self.print_memory)):
                for x in range(len(self.print_memory[y])):
                    if self.print_memory[y][x] != '': self.memory[f"0x{hex(y * self.x + x)[2:].zfill(8)}"] = self.print_memory[y][x]
            self.change = False

        else:
            print("Invalid mode!")

        return

    def malloc(self, size):
        pass

    def free(self, address):
        pass
