
#===============================
# bibiti bobiti bu
#===============================


def tokenize(code: str) -> list:
    tokens = []
    i = 0
    while i < len(code):
        c = code[i]

        if c == "\n":
            tokens.append(("NEWLINE", "\n"))
            i += 1
            continue

        if c == " ":
            i += 1
            continue

        if c.isdigit():
            start = i
            while i < len(code) and (code[i].isdigit()) or code[i] == ".":
                i += 1
            tokens.append(("NUMBER", float(code[start:i])))
            continue

        if c.isalpha():
            start = i
            i += 1
            while i < len(code) and code[i].isalnum() or code[i] == "_":
                i += 1
            tokens.append(("IDENT", code[start:i]))
            continue

        if c in "+-*/=()":
            tokens.append(("OP", c))
            i += 1
            continue

        raise ValueError(f"Unexpected character: {c}")
    return tokens



def evaluate(node, environment):


    i = 0
    while i <len(node):
 
        kind = node[0]
 
        if kind ==  "NEWLINE":
            continue
 
        if kind == "NUMBER":
            ...
            continue     
 
        if kind == "IDENT":
            ident = node[i][1]
            if ident == "print":
                result = ""
                if node[i+1] == "NUMBER":
                    print(node[i+1][1])

                elif node[i+1][0] == "IDENT":
                    print(environment[node[i+1][1]])
                i += 4
            else:
                environment[node[i][1]] = node[i+2][1]
                i += 4
            continue

        if kind == "OP":
            ...
            continue
        




def execute(code):
    tokens = tokenize(code)
    print("Tokens:", tokens)
    ...
    ...

example = """
x = 5
y = 3
z = x + y * 2
print(z)
"""



execute(example)

# Neue funktionierende Implementierung ohne Änderung des alten Codes

def tokenize2(code: str) -> list:
    tokens = []
    i = 0
    while i < len(code):
        c = code[i]

        if c in " \t":
            i += 1
            continue

        if c == "\n":
            tokens.append(("NEWLINE", c))
            i += 1
            continue

        if c.isdigit() or (c == "." and i + 1 < len(code) and code[i + 1].isdigit()):
            start = i
            has_dot = False
            while i < len(code) and (code[i].isdigit() or (code[i] == "." and not has_dot)):
                if code[i] == ".":
                    has_dot = True
                i += 1
            tokens.append(("NUMBER", float(code[start:i])))
            continue

        if c.isalpha() or c == "_":
            start = i
            i += 1
            while i < len(code) and (code[i].isalnum() or code[i] == "_"):
                i += 1
            tokens.append(("IDENT", code[start:i]))
            continue

        if c in "+-*/=()":
            tokens.append(("OP", c))
            i += 1
            continue

        raise ValueError(f"Unexpected character: {c}")

    tokens.append(("EOF", None))
    return tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def advance(self):
        self.pos += 1
        return self.tokens[self.pos - 1]

    def consume_newline(self):
        if self.peek()[0] == "NEWLINE":
            self.advance()

    def parse(self):
        statements = []
        while self.peek()[0] != "EOF":
            if self.peek()[0] == "NEWLINE":
                self.advance()
                continue
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        if self.peek()[0] == "IDENT":
            if self.peek()[1] == "print":
                self.advance()
                expression = self.parse_expression()
                self.consume_newline()
                return ("PRINT", expression)

            if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1] == ("OP", "="):
                name = self.advance()[1]
                self.advance()
                expression = self.parse_expression()
                self.consume_newline()
                return ("ASSIGN", name, expression)

        expression = self.parse_expression()
        self.consume_newline()
        return ("EXPR", expression)

    def parse_expression(self):
        node = self.parse_term()
        while self.peek()[0] == "OP" and self.peek()[1] in "+-":
            op = self.advance()[1]
            right = self.parse_term()
            node = ("BINOP", op, node, right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.peek()[0] == "OP" and self.peek()[1] in "*/":
            op = self.advance()[1]
            right = self.parse_factor()
            node = ("BINOP", op, node, right)
        return node

    def parse_factor(self):
        token = self.peek()
        if token[0] == "OP" and token[1] == "-":
            self.advance()
            return ("UNARY", "-", self.parse_factor())

        if token[0] == "NUMBER":
            self.advance()
            return ("NUMBER", token[1])

        if token[0] == "IDENT":
            self.advance()
            return ("IDENT", token[1])

        if token[0] == "OP" and token[1] == "(":
            self.advance()
            node = self.parse_expression()
            if self.peek() != ("OP", ")"):
                raise SyntaxError("Missing closing parenthesis")
            self.advance()
            return node

        raise SyntaxError(f"Unexpected token in expression: {token}")


def evaluate_ast(node, environment):
    kind = node[0]
    if kind == "NUMBER":
        return node[1]
    if kind == "IDENT":
        name = node[1]
        if name in environment:
            return environment[name]
        raise NameError(f"Undefined variable: {name}")
    if kind == "BINOP":
        left = evaluate_ast(node[2], environment)
        right = evaluate_ast(node[3], environment)
        op = node[1]
        if op == "+":
            return left + right
        if op == "-":
            return left - right
        if op == "*":
            return left * right
        if op == "/":
            return left / right
    if kind == "UNARY":
        value = evaluate_ast(node[2], environment)
        if node[1] == "-":
            return -value
    if kind == "ASSIGN":
        value = evaluate_ast(node[2], environment)
        environment[node[1]] = value
        return value
    if kind == "PRINT":
        value = evaluate_ast(node[1], environment)
        print(value)
        return value
    if kind == "EXPR":
        return evaluate_ast(node[1], environment)

    raise SyntaxError(f"Unsupported AST node: {node}")


def execute_fixed(code):
    tokens = tokenize2(code)
    print("Tokens:", tokens)
    parser = Parser(tokens)
    statements = parser.parse()
    environment = {}
    for statement in statements:
        evaluate_ast(statement, environment)
    return environment

execute_fixed(example)