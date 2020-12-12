from tokenizer import Tokenizer
from parser import Parser
from interpreter import Interpreter


class Calculator:
    def __init__(self):
        self.interpreter =  Interpreter("")

    def start(self):
        user_input = input("Hello! Welcome to The Calculator 4000!\nEnter Whatever you want to calculate, press 'h' for Help, or press 'q':\n")
        while user_input != 'q' and user_input != 'Q':
            if user_input == 'h' or user_input == 'H':
                print( "& : Minimum - (Usage: 6 & 2 = 2)\n$ : Maximum\n@ : Average - (Usage: 5 @ 7 = 6)\n"
                       "! : Factorial - (Usage: 3! = 6)\n% : Modulo\n~ : Sign Flip - (Usage: ~7 = -7)\n"
                       "^ : Exponentiation\n/ : Division\n* : Multiplication\n- : Subtraction\n+ : Addition\n"
                       "Parenthesis or done with SQUARE BRACKETS '[' and ']'\n")
            elif user_input == 'q' or user_input == 'Q':
                break
            else:
                self.interpreter.parser.set_program(user_input)
                calculated_val = self.interpreter.interpret()
                print("Value of {} = {}".format(user_input, calculated_val))

            user_input = input("Enter Whatever you want to calculate, press 'h' for Help, or press 'q':\n")
        print("Thank You for using The Calculator 4000!. Goodbye!")


if __name__ == "__main__":
    program = "[1! + 5 * 7 & [7!]] $ 8"

    #Test the tokenizer by printing all the tokens
    t = Tokenizer(program)
    while t.has_more_tokens():
        print(t.get_next_token())

    #Test the parser by generating and printing the whole ast tree
    p = Parser(program)
    # print("AST Tree:\n{}".format(p.parse()))
    root = p.parse()
    root.bfs_pretty_print()
    print("\n")

    #Test the interpreter program
    i = Interpreter(program)
    print("Value of {} = {}".format(program, i.interpret()))

    #Test the Calculator
    calc = Calculator()
    calc.start()

