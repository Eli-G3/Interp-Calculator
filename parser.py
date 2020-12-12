import tokenizer
from collections import deque

SPACE_DIFF = 3

class Parser:


    def __init__(self, program):
        self.program = program
        self.tokenizer = tokenizer.Tokenizer(program)
        self.current_token = self.tokenizer.get_next_token()

    def set_program(self, program):
        self.program = program
        self.tokenizer.set_program(program)
        self.current_token = self.tokenizer.get_next_token()

    def parse(self):
        """Returns an ast"""
        return self.expr()

    def eat(self, tok_type:str):
        if self.current_token.type == tok_type:
            self.current_token = self.tokenizer.get_next_token()
        else:
            raise SyntaxError("Expected token of type '{}', but instead got '{}'".format(tok_type, self.current_token.value))

    def expr(self):
        """
        expr -> pres2(+|- pres2)*
        :return:
        """
        node = self.precedence_2()

        while self.current_token is not None and self.current_token.type in ("ADD", "SUB"):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(node, self.precedence_2(), token)
        return node

    def precedence_2(self):
        """
        pres2 -> pres3( * | / pres3)*
        :return:
        """
        node = self.precedence_3()

        while self.current_token is not None and self.current_token.type in ("MUL", "DIV"):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(node, self.precedence_3(), token)
            node.spaces += SPACE_DIFF
        return node

    def precedence_3(self):
        """
        pres3 -> pres4( ^ pres4)*
        :return:
        """
        node = self.precedence_4()

        while self.current_token is not None and self.current_token.type == "POW":
            token = self.current_token
            self.eat("POW")
            node = BinOp(node, self.precedence_4(), token)
            node.spaces += SPACE_DIFF*2

        return node

    def precedence_4(self):
        """
        pres4 -> pres5( % | ! pres5)*
        :return:
        """
        node = self.precedence_5()

        while self.current_token is not None and self.current_token.type in ("MOD", "FCT"):
            token = self.current_token
            self.eat(token.type)
            if token.type == "MOD":
                node = BinOp(node, self.precedence_5(), token)
            else:
                node = BinOp(node, None, token)
            node.spaces += SPACE_DIFF*3

        return node


    def precedence_5(self):
        """
        pres5 -> pres6( & | $ | @ pres6)*
        :return:
        """
        node = self.precedence_6()

        while self.current_token is not None and self.current_token.type in ("MIN", "MAX", "AVG"):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(node, self.precedence_6(), token)
            node.spaces += SPACE_DIFF*4
        return node

    def precedence_6(self):
        """
        pres6 -> (~ pres7)*
        :return:
        """
        node = self.literal()

        while self.current_token is not None and self.current_token.type == "NOT":
            token = self.current_token
            self.eat("NOT")
            node = UnOp(self.literal(), token)
            node.spaces += SPACE_DIFF*5

        return node



    def literal(self):
        """
        literal -> LITERAL | LPAREN pres1 RPAREN
        :return:
        """
        token = self.current_token
        if token.type == "NUMBER":
            self.eat("NUMBER")
            node = Num(token)
            node.spaces += SPACE_DIFF*6
            return node

        elif token.type == "LPAREN":
            self.eat("LPAREN")
            node = self.expr()
            self.eat("RPAREN")
            return node


class ASTNode:
    def __init__(self, left, right, token:tokenizer.Token):
        self.left = left
        self.right = right
        self.token = token
        self.spaces = 0

    def bfs_pretty_print(self):
        q1 = deque()
        q2 = deque()
        #add root to q1
        q1.appendleft(self)
        while len(q1) != 0 or len(q2) != 0:
            print("\n")
            while len(q1) != 0:
                if q1[-1].left is not None:
                    q2.appendleft(q1[-1].left)
                if q1[-1].right is not None:
                    q2.appendleft(q1[-1].right)
                print(q1.pop().token.value, end=" ")
            print("\n")
            while len(q2) != 0:
                if q2[-1].left is not None:
                    q1.appendleft(q2[-1].left)
                if q2[-1].right is not None:
                    q1.appendleft(q2[-1].right)
                print(q2.pop().token.value, end=" ")

    def __str__(self):
        # return " "*self.spaces + "  {}\n".format(self.right) + " "*self.spaces + " /\n" + " "*self.spaces + "{}\n".format(self.token.value) + " "*self.spaces + " \\\n" + " "*self.spaces + "  {}".format(self.left)
        return "{}".format(self.token)

class UnOp(ASTNode):
    def __init__(self, right, token:tokenizer.Token):
        super().__init__(None, right, token)

class BinOp(ASTNode):
    def __init__(self, left, right, token:tokenizer.Token):
        super().__init__(left, right, token)

class Num(ASTNode):
    def __init__(self, token: tokenizer.Token):
        super().__init__(None, None, token)


