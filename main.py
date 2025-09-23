import memoryLib

def main():
    memory = None
    while True:
        input_ = input(f"{memory.getName() + ' ' if memory != None else ''}>>> ")
        
        output = memoryLib.command_handler(input_, memory)
        if output == 0: break
        elif output == 1: continue
        elif output != None: memory = output

if __name__ == '__main__': main()