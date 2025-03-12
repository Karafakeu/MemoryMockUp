import math
import ast

class memory():
    def __init__(self, name, x, y, foreign = None):
        self.name = name
        self.memory = self.initMemory(x, y)
        self.foreign = foreign

    def initMemory(self, x, y): return [['' for j in range(x)] for i in range(y)]
    
    def getName(self): return self.name

    def getForeignName(self): return self.foreign.getName()
    
    def getValue(self, key):
        """
        Returns the value stored in the memory at the given key.

        Accepts different types of keys:

        - empty key: returns None
        - hexadecimal key: '0x' followed by a hexadecimal number
        - decimal key: a string or int representing a decimal number
        - coordinate key: a tuple of two ints representing the coordinates

        Returns None if the key is invalid or out of range of the memory.
        """

        if key == '' or key == '0x' or key == None:
            print("Invalid key: empty key!")
            return

        # hexadecimal key
        if key[0:2] == '0x':
            try:
                key = int(key[2:], 16)
                x = math.floor(key / len(self.memory[0]))
                y = key % len(self.memory[0])
            except ValueError:
                print("Invalid key: invalid hexadecimal key!")
                return

        # decimal key
        elif type(key) == str:
            try:
                key = int(key)
                x = math.floor(key / len(self.memory[0]))
                y = key % len(self.memory[0])
            except ValueError:
                print("Invalid key: invalid decimal key!")
                return
    
        # coordinate key
        elif type(key) == tuple:
            try:
                x, y = key[0], key[1]
            except (ValueError, TypeError):
                print("Invalid key: invalid coordinate key!")
                return

        # invalid key type
        else:
            print("Invalid key type!")
            return
        
        try:
            return self.memory[x][y]
        except IndexError:
            print("Memory index is out of range of the memory!")
            return

    def setValue(self, key, value):
        if key == '' or key == '0x' or key == None:
            print("Invalid key: empty key!")
            return

        # hexadecimal key
        if key[0:2] == '0x':
            try:
                key = int(key[2:], 16)
                x = math.floor(key / len(self.memory[0]))
                y = key % len(self.memory[0])
            except ValueError:
                print("Invalid key: invalid hexadecimal key!")
                return

        # decimal key
        elif type(key) == str:
            try:
                key = int(key)
                x = math.floor(key / len(self.memory[0]))
                y = key % len(self.memory[0])
            except ValueError:
                print("Invalid key: invalid decimal key!")
                return
    
        # coordinate key
        elif type(key) == tuple:
            try:
                x, y = key[0], key[1]
            except (ValueError, TypeError):
                print("Invalid key: invalid coordinate key!")
                return

        # invalid key type
        else:
            print("Invalid key type!")
            return

        try:
            self.memory[x][y] = value
        except IndexError:
            print("Memory index is out of range of the memory!")
            return

    def printMemory(self):
        for i in range(len(self.memory)):
            print(self.memory[i])
        return
    
    def saveMemory(self):
        global new
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
                for i in range(len(self.memory)):
                    f.write(str(self.memory[i]) + "\n")
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
            
            for memLine in self.memory[::-1]:
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

        self.memory = fetch
        return
