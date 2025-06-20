import sys
from tokenizer import tokenize
from belasova_parser import Parser
from interpreter import Interpreter

def main():
    if len(sys.argv) < 2:
        print("Usage: python sovarun.py <source-file.sova>")
        sys.exit(1)

    source_path = sys.argv[1]

    with open(source_path, 'r') as f:
        code = f.read()

    tokens = tokenize(code)
    print("Tokens:")
    for t in tokens:
        print(t)

    parser = Parser(tokens)
    ast = parser.parse()

    print("\nAST:")
    for node in ast:
        print(node)

    interpreter = Interpreter(ast)
    interpreter.interpret()

if __name__ == '__main__':
    main()
