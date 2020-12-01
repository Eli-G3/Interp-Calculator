

class Tokenizer:

    def __init__(self, program:str):
        self.__program = program
        self.__cursor = 0

    def has_more_tokens(self):
        return (self.__cursor < len(self.__program))

    def get_next_token(self):
        if (not self.has_more_tokens()):
            return None

        tok_type = ''
        value = None

        #Literals (In this case just a number)
        if (self.__program[self.__cursor].isdigit()):
            value = ''
            while (self.__cursor < len( self.__program) and self.__program[self.__cursor].isalnum()):
                value += self.__program[self.__cursor]
                self.__cursor += 1 
            return (Token("NUMBER", int(value)))

        #Operators
        elif (self.__program[self.__cursor] == "&"\
            or self.__program[self.__cursor] == "$"\
            or self.__program[self.__cursor] == "@"\
            or self.__program[self.__cursor] == "!"\
            or self.__program[self.__cursor] == "%"\
            or self.__program[self.__cursor] == "^"\
            or self.__program[self.__cursor] == "/"\
            or self.__program[self.__cursor] == "*"\
            or self.__program[self.__cursor] == "-"\
            or self.__program[self.__cursor] == "+"):
            tok_type = "BINARY_OPERATOR"
            value = self.__program[self.__cursor]
        
        elif (self.__program[self.__cursor] == "~"):
            tok_type = "UNARY_OPERATOR"
            value = self.__program[self.__cursor]
        
        elif (self.__program[self.__cursor].isspace()):
            self.__cursor += 1
            return self.get_next_token()

        else:
            raise SyntaxError("Unexpected Token \"{}\"".format(self.__program[self.__cursor]))
        
        self.__cursor += 1
        return Token(tok_type, value)

class Token():
    def __init__(self, tok_type:str, value:object):
        self.type = tok_type
        self.value = value
    
    def __str__(self):
        return "{} Token Type\nValue:{}".format(self.type, str(self.value))

        