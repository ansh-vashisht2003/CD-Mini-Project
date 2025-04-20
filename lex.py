import re
import sys
import os

# Keywords, types, and operators
c_keywords = [
    "auto", "break", "case", "char", "const", "continue", "default", "do", "else", 
    "enum", "extern", "for", "goto", "if", "long", "register", "return", 
    "short", "signed", "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", 
    "void", "volatile", "while", "begin", "end", "main"
]

c_types = ["int", "float", "double"]

reloperators = {
    "+": "plus", 
    ">=": "greater than or equal to", 
    "<=": "less than or equal to", 
    "<": "less than", 
    ">": "greater than", 
    "-": "minus", 
    "*": "multiply", 
    "%": "modulo", 
    "/": "divide", 
    "==": "equal to", 
    "!=": "not equal to"
}

# Containers to store tokens
keywords = []
numbers = []
characters = []
operators = []
rel_operators = []
identifiers = []

def lex():
    filename = input("Enter the input file name: ")
    
    try:
        # Open the output file where tokens will be written
        with open("tokens.txt", "w") as token_file:
            with open(filename, "r") as fptr:
                tokens = []
                line_count = 0
                print("\nLexical Analysis:")
                print("{:<20} {:<20} {:<20}".format("Token", "Lexeme", "Type"))
                print("-" * 40)
                
                for line in fptr:
                    line_count += 1
                    identifier_pattern = r'[a-zA-Z_][a-zA-Z0-9_]*'
                    line_tokens = re.findall(r'[a-zA-Z_#$@!%^&*0-9]\w*|==|!=|[<>]=?|\+\+|--|[\+\-*/%=;,()\[\]]|\d+', line.strip())
                    tokens.extend(line_tokens)
                    
                    for token in line_tokens:
                        if token in c_keywords:
                            keywords.append(token)
                            token_file.write(f"{token.upper()}\n")
                            print("{:<20} {:<20} {:<20}".format(token.upper(), token, "Keyword"))
                        elif token in c_types:
                            keywords.append(token)
                            token_file.write("TYPE\n")
                            print("{:<20} {:<20} {:<20}".format("TYPE", token, "Keyword"))
                        elif token in reloperators:
                            rel_operators.append(token)
                            token_file.write("RELOP\n")
                            print("{:<20} {:<20} {:<20}".format("RELOP", token, reloperators[token]))
                        elif token == ",":
                            characters.append(token)
                            token_file.write("CM\n")
                            print("{:<20} {:<20} {:<20}".format("CM", token, "Comma"))
                        elif token == ";":
                            characters.append(token)
                            token_file.write("SC\n")
                            print("{:<20} {:<20} {:<20}".format("SC", token, "Semi-colon"))
                        elif token == "(":
                            characters.append(token)
                            token_file.write("LP\n")
                            print("{:<20} {:<20} {:<20}".format("LP", token, "Left Parenthesis"))
                        elif token == ")":
                            characters.append(token)
                            token_file.write("RP\n")
                            print("{:<20} {:<20} {:<20}".format("RP", token, "Right Parenthesis"))
                        elif token.isdigit():
                            numbers.append(token)
                            token_file.write("NUM\n")
                            print("{:<20} {:<20} {:<20}".format("NUM", token, "Number"))
                        elif token == "++":
                            operators.append(token)
                            token_file.write("INC\n")
                            print("{:<20} {:<20} {:<20}".format("INC", token, "Increment operator"))
                        elif token == "=":
                            operators.append(token)
                            token_file.write("EQ\n")
                            print("{:<20} {:<20} {:<20}".format("EQ", token, "Assignment operator"))
                        elif re.match(identifier_pattern, token):
                            identifiers.append(token)
                            token_file.write("ID\n")
                            print("{:<20} {:<20} {:<20}".format("ID", token, "Identifier"))
                        else:
                            print(f"Error at Line {line_count}: Unexpected character {token}")
                            token_file.close()
                            os.remove("tokens.txt")
                            sys.exit()

        # Summary of lexical analysis
        with open("lexical_summary.txt", "w") as summary_file:
            data = [
                ("Numbers", len(numbers), *numbers), 
                ("Symbols", len(characters), *characters),
                ("Keywords", len(keywords), *keywords),
                ("Operators", len(operators), *operators),
                ("Identifiers", len(identifiers), *identifiers),
                ("Relational Operators", len(rel_operators), *rel_operators)
            ]
            summary_file.write("Summary of Lexical Analysis:\n")
            summary_file.write("-" * 60 + "\n")
            for item in data:
                category, count, *elements = item
                summary_file.write(f"{category:<22} {count:<12} {' '.join(set(elements))}\n")

    except FileNotFoundError:
        print("Error: File not found")
        sys.exit()

if __name__ == "__main__":
    lex()
