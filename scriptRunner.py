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
printing, fstring = False, False
text_before, text_after = '', ''

for line in lines:
    # default changes
    command = line
    if command.startswith('#'): continue
    command = command.replace('\n', '')

    # printing value
    if command.startswith('print('):
        printing = True
        command = command.replace('print(', '').replace(')', '')

    # printing fstring
    if command.startswith('f"'):
        printing, fstring = True, True
        command = command.replace('f"', '').replace('"', '')
        split = command.split('{')
        text_before = split[0]
        command = split[1].split('}')[0]
        text_after = split[1].split('}')[1]

    # run command
    output = memoryLib.command_handler(command, memory, True)
    if output == 0: break
    elif output == 1: continue
    elif type(output) == memoryLib.memory: memory = output
    elif output != None and printing and not fstring: 
        print(f"Output of command ({command}): {output}") # print() like python
        printing = False
    elif output != None and printing and fstring: 
        print(f"{text_before}{output}{text_after}") # fstring like python
        printing, fstring = False, False
        text_before, text_after = '', ''

    time.sleep(0.5)