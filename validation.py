
def valid_input(input):
    while True:
        if input.lower() == "exit":
            return # stop the program
        elif input.lower() not in ["y", "n"]:
            input("That is not a valid input. Please try again: ")
            continue
        else:
            break

def exit_input(input):
    if input.lower() == "exit":
        return # stop the program