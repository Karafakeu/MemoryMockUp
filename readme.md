# Memory MockUp
A small project to simulate how a memory works in python, using 2d lists and heap dictionaries. It has things like printing the memory, saving the memory into a log and fetching it back or malloc itself. It consists of 2 parts:
* main.py - responsible for the user "interface" through the console, handles commands
* memoryLib.py - contains the memory class and all its functionality

# main.py
Contains the main loop with the implemented commands for the memoryLib.py. These commands are:
* exit - exit the application 
* init (name) (x size) (y size) - initiate an empty memory of name and size
* select (name) - select a memory of name from the memoryLog.txt
* get (key) - get value of the current working memory at key, decimal or hexadecimal
* set (key) (value) - set value to the current working memory at key, decimal or hexadecimal
* print - print the current working memory
* save - save the current working memory
* fetch - fetch teh current working memory from the memoryLog.txt

# memoryLib.py
Contains all the main functionality of the memory class and its classes. This class contains properties **name**, **x**, **y**, **change**, **memory (dict)**, **free_memory (list)**, **print_memory (2d list)**.
It also contains the functions:
* initMemory(x, y): initiates and returns the print memory of size **x**, **y**
* getName(): returns the name of the current working memory
* getValue(key): returns the value on the address **key** of the current working memory
* setValue(key, value): sets the **value** to the memory on the address **key**
* printMemory(): prints the print_memory (sometimes converts first, as per memoryConvert())
* saveMemory(): saves current memory into the memoryLog.txt
* fetchMemory(): fetches the memory under the same name from memoryLog.txt
* memoryConvert(mode): converts memory into print_memory (mode = MTP) or vice versa (mode = PTM)
* malloc(size): allocates an address from the memory using free_memory and returns its address
* free(address): frees the memory and adds the **address** into free_memory