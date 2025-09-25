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
echo = True
variables = {}

for line in lines:
    # default changes
    command = line
    if line == '\n': continue
    if command.startswith('#'): continue
    command = command.replace('\n', '')

    # echo
    if command == 'echo: true': echo = True; continue
    elif command == 'echo: false': echo = False; continue

    # printing value
    if command.startswith('print('):
        printing = True
        command = command.replace('print(', '').replace(')', '')
        try:
            if command.split('|')[1] not in variables.keys():
                print(f"Variable {command.split('|')[1]} is not defined")
                continue
            variable_value = variables[command.split('|')[1]]

            # variable in command
            if len(command.split('|')) == 3:
                command = command.split('|')[0] + str(variable_value) + command.split('|')[2]

        except IndexError: pass

        # printing fstring
        if command.startswith('f"'):
            printing, fstring = True, True
            command = command.replace('f"', '').replace('"', '')
            whole_command = command
            try:
                split = whole_command.split('{')
                text_before = split[0]
                command = split[1].split('}')[0]
                text_after = split[1].split('}')[1]
            except IndexError:
                text_before, text_after = '', ''

            try:
                if whole_command.split('|')[1] not in variables.keys():
                    print(f"Variable {whole_command.split('|')[1]} is not defined")
                    continue
                variable_value = variables[whole_command.split('|')[1]]
                
                # variable in text before
                if len(text_before.split('|')) == 3:
                    text_before = text_before.split('|')[0] + str(variable_value) + text_before.split('|')[2]

                # variable in text after
                elif len(text_after.split('|')) == 3:
                    text_after = text_after.split('|')[0] + str(variable_value) + text_after.split('|')[2]

            except IndexError: pass

            if not memoryLib.is_command(command.split(' ')[0]):
                print(f"{text_before}{command}{text_after}")
                text_before, text_after = '', ''
                continue

    
    # variable assignment
    elif len(command.split('=')) == 2:
        # processing
        var_name = command.split('=')[0].replace(' ', '')
        var_value = command.split('=')[1]
        if var_value[0] == ' ': var_value = var_value[1:]
        var_value_command = var_value.split(' ')[0]

        # a literal variable
        if not memoryLib.is_command(var_value_command):
            variables[var_name] = eval(var_value)
            continue

        # variable as a return of command
        value = memoryLib.command_handler(var_value, memory, True, echo)
        variables[var_name] = value

        continue

    # replace variable in normal command
    if not printing and command.count('|') > 0: 
        # variable not defined
        if command.split('|')[1] not in variables.keys():
            print(f"Variable {command.split('|')[1]} is not defined")
            continue

        # replace variable into expression
        variable_value = variables[command.split('|')[1]]
        command = command.replace(f"|{command.split('|')[1]}|", str(variable_value))

    # run command
    output = memoryLib.command_handler(command, memory, True, echo)
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