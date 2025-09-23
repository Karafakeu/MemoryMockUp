import memoryLib
import time
import sys

if len(sys.argv) != 2:
    sys.exit("Usage: python scriptRunner.py [script directory]")
script_dir = sys.argv[1]

with open(script_dir, 'r') as f:
    lines = f.readlines()
    f.close()

memory = None
printing = False

for line in lines:
    command = line
    if command.startswith('print('):
        printing = True
        command = line.replace('print(', '').replace(')', '')
    command = command.replace('\n', '')
    output = memoryLib.command_handler(command, memory, True)
    if output == 0: break
    elif output == 1: continue
    elif type(output) == memoryLib.memory: memory = output
    elif output != None and printing: 
        print(f"Output of command ({command}): {output}") # print() like python
        printing = False

    time.sleep(0.5)