# Memory MockUp
A small project to simulate how a memory works in python, using 2d lists and heap dictionaries. It has things like printing the memory, saving the memory into a log and fetching it back or malloc itself. It consists of 2 parts:
* main.py - responsible for the user "interface" through the console, handles commands
* memoryLib.py - contains the memory class and all its functionality, with the command function calling other memory class functions based on the inputed command

# main.py
Contains the main loop with the implemented commands for the memoryLib.py. These are called through memoryLib.py command_handler. These commands are:
* exit - exit the application after a prompt
* init (name) (x size) (y size) - initiate an empty memory of name and size
* select (name) - select a memory of name from the memoryLog.txt
* getval (key) - get value of the current working memory at hexadecimal key
* setval (key) (value) - set value to the current working memory at hexadecimal key
* freeval (key) - free the memory at the position of the key
* print - print the current working memory
* save - save the current working memory
* fetch - fetch the current working memory from the memoryLog.txt
* malloc (size) - returns a position, not within the memory object, that points to the beginning of a linked list of characters (positions) within the memory, working like a variable assignment
* get (malloc key) - get value of entire variable at the malloc key location
* set (malloc key) - set value of entire "variable" at the malloc key location
* free (malloc key) - free a whole "variable" from the memory
* clear - resets the whole memory to its empty original state
* help - print all available commands

# memoryLib.py
Contains all the main functionality of the memory class and its classes. This class contains properties **name**, **x**, **y**, **change**, **memory (dict)**, **free_memory (list)**, **print_memory (2d list)**.
It also contains the functions:
* initMemory(x, y): initiates and returns the print memory of size **x**, **y**
* getName(): returns the name of the current working memory
* getValue(key): returns the value on the address **key** of the current working memory
* setValue(key, value): sets the **value** to the memory on the address **key**
* get(key): return the whole "variable" from malloc address
* set(key, value): set entire "variable" based on malloc address
* printMemory(): prints the print_memory (sometimes converts first, as per memoryConvert())
* saveMemory(): saves current memory into the memoryLog.txt
* fetchMemory(): fetches the memory under the same name from memoryLog.txt
* memoryConvert(mode): converts memory into print_memory (mode = MTP) or vice versa (mode = PTM)
* malloc(size): returns the malloc address of a "variable" of size in the malloc memory
* freeValue(address): frees the memory and adds the **address** into free_memory
* free(address): frees the malloc address and its joint addresses in memory
* clear(): resets and clears the whole memory
* exit(): prompts the user if changed have been made and returns 1 if exit is in order
* command_handler(command): calls functions based on the command, inputted as the literal string taken from the input

# TO-DO:
* scripting - basic commands
* scripting - variables
* scripting - print like python