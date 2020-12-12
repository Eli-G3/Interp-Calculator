import parser
import math

class Interpreter:

    def __init__(self, program):
        self.parser = parser.Parser(program)
        self.ast = None

    def interpret(self):
        self.ast = self.parser.parse()
        val = self.visit_ast(self.ast)
        return val

    def visit_ast(self, ast_node:parser.ASTNode):
        """
          :return The Calculated Value by traversing the ast in dfs
        """
        if ast_node is None:
            return None

        elif ast_node.token.type == "NUMBER":
            return ast_node.token.value
        elif ast_node.token.type == "SUB":
            return self.visit_ast(ast_node.left) - self.visit_ast(ast_node.right)
        elif ast_node.token.type == "ADD":
            return self.visit_ast(ast_node.left) + self.visit_ast(ast_node.right)
        elif ast_node.token.type == "MUL":
            return self.visit_ast(ast_node.left) * self.visit_ast(ast_node.right)
        elif ast_node.token.type == "DIV":
            return self.visit_ast(ast_node.left) * self.visit_ast(ast_node.right)
        elif ast_node.token.type == "POW":
            return self.visit_ast(ast_node.left) ^ self.visit_ast(ast_node.right)
        elif ast_node.token.type == "NOT":
            return (-1)*self.visit_ast(ast_node.right)
        elif ast_node.token.type == "MOD":
            return self.visit_ast(ast_node.left) % self.visit_ast(ast_node.right)
        elif ast_node.token.type == "FCT":
            return math.factorial(self.visit_ast(ast_node.left))
        elif ast_node.token.type == "AVG":
            return (self.visit_ast(ast_node.left) + self.visit_ast(ast_node.right))/2.0
        elif ast_node.token.type == "MAX":
            return max(self.visit_ast(ast_node.left), self.visit_ast(ast_node.right))
        elif ast_node.token.type == "MIN":
            return min(self.visit_ast(ast_node.left), self.visit_ast(ast_node.right))

        else:
            raise SyntaxError("Unrecognized Token with type: {}.".format(ast_node.token.type))





