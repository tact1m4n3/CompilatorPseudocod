from lexer import Lexer
from parser_ import Parser
from compiler import Compiler
import sys, os

if __name__ == "__main__":
    filename = sys.argv[1]
    cpp_filename = filename.split(".")[0] + ".cpp"
    exec_filename = filename.split(".")[0]
    with open(filename, "r+") as f:
        _input = f.read()
    lexer = Lexer(_input, filename)
    tokens, errors = lexer.tokenize()
    if errors:
        for error in errors:
            print(error.as_string())
        exit()
    
    print("-> Tokens created successfully...")

    parser = Parser(tokens)
    ast = parser.parse_program()

    if parser.errors.errors:
        for error in parser.errors.errors:
            print(error.as_string())
        exit()
    
    print("-> Ast created successfully...")

    compiler = Compiler()
    code, error = compiler.visit(ast)

    if error:
        print(error.as_string())
        exit()
    
    print("-> C++ code generated successfully...")
    
    with open(cpp_filename, "w+") as f:
        f.write(code)
    
    os.system(f"g++ {cpp_filename} -o {exec_filename}")
    

