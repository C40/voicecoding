from instructions import instructions
from helpers.voice_conversion import voice_conversion
from code_class import Code


# evaluates the voice command
def eval_command(command):
    # checks for the instruction
    command = voice_conversion(command, "command")
    instruction = command.split()[0]
    # exits if instruction is "exit"
    if instruction.lower() == "exit":
        print("Exiting...")
        quit()
    if instruction.lower() == "end":
        if Code.multiline:
            Code.code[len(Code.code)] = "{0}end".format(Code.amount_nested)
            Code.amount_nested = Code.amount_nested[:-4]
        return
    elif instruction.lower() == "cancel":
        Code.multiline = False
        Code.if_else = False
        Code.for_loop = False
        Code.code = ""
        Code.amount_nested = ""

    # if there is nothing after the instruction, invalid command
    if len(command.split()) == 1:
        return False

    # gets and runs voice command that will be used with the instruction
    to_parse = " ".join(command.split()[1:])
    if instruction in instructions:
        if Code.if_else or Code.for_loop:
            to_parse = voice_conversion(to_parse, "if-else/loop")
            to_add = instructions[instruction](to_parse)
            if to_add not in [None, False]:
                Code.code[len(Code.code)] = "{0}    {1}".format(
                    Code.amount_nested, to_add
                )
                return
            elif to_add is False:
                print("Invalid command")
                return False
        else:
            return instructions[instruction](to_parse)
    else:
        return False
