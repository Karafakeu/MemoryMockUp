import ast

class memory():
    def __init__(self, name, x, y):
        self.name = name
        self.x, self.y = x, y
        self.change = False
        self.memory = {}
        self.free_memory = [f"0x{hex(i)[2:].zfill(8)}" for i in range(x * y)]
        self.p_memory = self.initMemory(x, y)

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

        try:
            self.memory[key] = value
            self.change = True
            self.free_memory.remove(key)
            return 1
        except IndexError:
            print("Memory index is out of range of the memory!")
            return 0

    def printMemory(self):
        if self.change: # change has been made, must convert memory to p_memory
            self.memoryConvert('MTP')

        for i in range(len(self.p_memory)):
            print(self.p_memory[i])
        return 1
    
    def saveMemory(self):
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

        self.p_memory = fetch
        x, y = len(self.p_memory), len(self.p_memory[0])
        self.x, self.y = x, y
        self.free_memory = [f"0x{hex(i)[2:].zfill(8)}" for i in range(self.x * self.y)]
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
            self.change = False

        elif mode == 'PTM': # print memory to memory
            self.memory = {}
            for y in range(len(self.p_memory)):
                for x in range(len(self.p_memory[y])):
                    if self.p_memory[y][x] != '': self.memory[f"0x{hex(y * self.x + x)[2:].zfill(8)}"] = self.p_memory[y][x]; self.free_memory.remove(f"0x{hex(y * self.x + x)[2:].zfill(8)}")
            self.change = False

        else:
            print("Invalid mode!")
            return 0

        return 1

    def malloc(self, size):
        pass

    def free(self, address):
        del self.memory[address]
        self.change = True
        for i in range(len(self.free_memory)):
            if i == len(self.free_memory) - 1: self.free_memory.insert(i + 1, address); break
            if int(self.free_memory[i][2:], 16) < int(address[2:], 16) and int(self.free_memory[i + 1][2:], 16) > int(address[2:], 16):
                self.free_memory.insert(i + 1, address); break
        return 1