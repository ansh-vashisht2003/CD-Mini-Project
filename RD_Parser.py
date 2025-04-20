import sys

class ParseTreeNode:
    def __init__(self, label, terminal=False):
        self.label = label
        self.terminal = terminal
        self.children = []

    def add_child(self, child):
        self.children.append(child)

class RD_Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.parse_tree = None

    def parse(self):
        self.parse_tree = self.parse_S()
        if self.pos < len(self.tokens):
            raise SyntaxError("Unexpected tokens at the end")
        print("Parsing successful!")
        return self.parse_tree

    def match(self, expected_token):
        if self.pos < len(self.tokens) and self.tokens[self.pos] == expected_token:
            self.pos += 1
        else:
            print(f"Expected '{expected_token}', found '{self.tokens[self.pos]}'")
            sys.exit(0)

    def parse_S(self):
        node = ParseTreeNode("S")
        node.add_child(ParseTreeNode(self.tokens[self.pos], True))
        self.match("TYPE")
        node.add_child(ParseTreeNode(self.tokens[self.pos], True))
        self.match("MAIN")
        self.match("LP")  # Expect LP for '('
        self.match("RP")  # Expect RP for ')'
        self.match("BEGIN")
        node.add_child(self.parse_CODE())
        self.match("END")
        return node

    def parse_CODE(self):
        node = ParseTreeNode("CODE")
        node.add_child(self.parse_DECLARE())
        node.add_child(self.parse_STATEMENTS())
        return node

    def parse_DECLARE(self):
        node = ParseTreeNode("DECLARE")
        node.add_child(ParseTreeNode(self.tokens[self.pos], True))
        self.match("TYPE")
        
        node.add_child(self.parse_ID_LIST())  # Parse variable list (including initializations)
        
        self.match("SC")  # Expect semicolon after declaration
        return node

    def parse_ID_LIST(self):
        node = ParseTreeNode("ID_LIST")
        
        while self.tokens[self.pos] == "ID":  # As long as we have an identifier
            var_node = ParseTreeNode(self.tokens[self.pos], True)
            node.add_child(var_node)
            self.match("ID")
            
            # Check for assignment operator '=' (e.g., "re = 0")
            if self.tokens[self.pos] == "EQ":
                node.add_child(self.parse_ASSIGNMENT())
            
            # Handle commas separating declarations
            if self.tokens[self.pos] == "CM":
                node.add_child(ParseTreeNode(self.tokens[self.pos], True))  # Add comma
                self.match("CM")
        
        return node

    def parse_ASSIGNMENT(self):
        node = ParseTreeNode("ASSIGNMENT")
        node.add_child(ParseTreeNode(self.tokens[self.pos], True))  # The '=' token
        self.match("EQ")
        
        # Allow either ID or NUM after assignment (handle initialization like 're = 0')
        if self.tokens[self.pos] == "ID":
            node.add_child(ParseTreeNode(self.tokens[self.pos], True))
            self.match("ID")
        elif self.tokens[self.pos] == "NUM":
            node.add_child(ParseTreeNode(self.tokens[self.pos], True))
            self.match("NUM")
        else:
            print(f"Expected 'ID' or 'NUM' after '=', found {self.tokens[self.pos]}")
            sys.exit(0)
        
        return node

    def parse_EXPR(self):
        node = ParseTreeNode("EXPR")
        node.add_child(ParseTreeNode(self.tokens[self.pos], True))

        # Handle ID and RELOP (relational operators)
        if self.tokens[self.pos] == "ID":
            node.add_child(ParseTreeNode(self.tokens[self.pos], True))
            self.match("ID")

        elif self.tokens[self.pos] in ["NUM", "ID"]:
            # If it's a number or identifier, we handle the token
            node.add_child(ParseTreeNode(self.tokens[self.pos], True))
            self.match(self.tokens[self.pos])

        # Handle relational operators (like ==, !=, <, >)
        if self.tokens[self.pos] in ["RELOP"]:
            node.add_child(ParseTreeNode(self.tokens[self.pos], True))
            self.match("RELOP")
            node.add_child(self.parse_EXPR())  # Recursive call for the right operand of the relation
        
        return node

    def parse_STATEMENTS(self):
        node = ParseTreeNode("STATEMENTS")
        while self.tokens[self.pos] in ["ID", "WHILE"]:
            if self.tokens[self.pos] == "ID":
                node.add_child(self.parse_ASSIGN_STMT())
            elif self.tokens[self.pos] == "WHILE":
                node.add_child(self.parse_WHILE_STMT())
        return node

    def parse_ASSIGN_STMT(self):
        node = ParseTreeNode("ASSIGN_STMT")
        node.add_child(ParseTreeNode(self.tokens[self.pos], True))
        self.match("ID")
        node.add_child(ParseTreeNode(self.tokens[self.pos], True))
        self.match("EQ")
        node.add_child(self.parse_EXPR())
        self.match("SC")  # Expect semicolon after assignment
        return node

    def parse_WHILE_STMT(self):
        node = ParseTreeNode("WHILE_STMT")
        node.add_child(ParseTreeNode(self.tokens[self.pos], True))
        self.match("WHILE")
        self.match("LP")  # Expect LP for '('
        node.add_child(self.parse_EXPR())  # Parse the expression inside while
        self.match("RP")  # Expect RP for ')'
        self.match("BEGIN")
        node.add_child(self.parse_STATEMENTS())  # Parse statements inside while
        self.match("END")
        return node

# Code to parse tokens
input_str = ""
tokens = []

try:
    try:
        with open("tokens.txt", "r", encoding="utf-8") as tf_handle:
            for line in tf_handle:
                line = line.strip()
                if line:
                    input_str += line + " "
    except FileNotFoundError:
        print("Error: File not found.")

    print("Based on tokens generated the input to be parsed : ")
    print(input_str)
    print()
    tokens = input_str.split()
    parser = RD_Parser(tokens)
    parse_tree = parser.parse()

    def print_parse_tree(node, indent=""):
        terminal_symbol = " (Terminal)" if node.terminal else ""
        print(indent + node.label + terminal_symbol)
        if node.children:
            for idx, child in enumerate(node.children):
                if idx == len(node.children) - 1:
                    print_parse_tree(child, indent + "    " + "└── ")
                else:
                    print_parse_tree(child, indent + "    " + "├── ")

    with open("parse_tree.txt", "w", encoding="utf-8") as tree_file:
        def write_parse_tree(node, indent=""):
            terminal_symbol = " (Terminal)" if node.terminal else ""
            tree_file.write(indent + node.label + terminal_symbol + "\n")
            if node.children:
                for idx, child in enumerate(node.children):
                    if idx == len(node.children) - 1:
                        write_parse_tree(child, indent + "    " + "└── ")
                    else:
                        write_parse_tree(child, indent + "    " + "├── ")

        write_parse_tree(parse_tree)

    # Writing Grammar Rules to parser_table.txt
    with open("parser_table.txt", "w", encoding="utf-8") as pt:
        pt.write("Grammar Rules Used:\n")
        pt.write("1. S, int -> main\n")
        pt.write("2. main, int -> int main\n")
        pt.write("3. statements, begin -> statement statements\n")
        pt.write("4. statement, while -> while_loop\n")
        pt.write("5. statement, int -> declaration\n")
        pt.write("6. declaration, int -> int IDENTIFIER ASSIGNMENT NUMBER\n")
        pt.write("7. while_loop, while -> while PARENTHESIS expression PARENTHESIS begin statements end\n")

except Exception as e:
    print(f"Error occurred: {e}")
