import sys

def valid_input(prompt):
    while True:
        user_input = input(prompt).strip().lower()

        if user_input == "exit":
            sys.exit()

        elif user_input == "y":
            return "y"

        elif user_input == "n":
            return "n"

        else:
            print("That is not a valid input. Please try again.")

# Input is Exit
def exit_input(user_input):
    if user_input.lower() == "exit":
       sys.exit()