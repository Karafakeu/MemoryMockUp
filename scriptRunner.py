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

for line in lines:
    output = memoryLib.command_handler(line.replace('\n', ''), memory, True)
    if output == 0: break
    elif output == 1: continue
    elif output != None: memory = output

    time.sleep(0.5)