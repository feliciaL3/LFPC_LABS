from lexer import Lexer

text = '''16+2+(3-2)*1/1mm
elif self.text_self = $
$.mdl
#the.input\012
#comment\012
def magic_function(arr):
    n = len(arr)
    for p in range(n):
            if arr[m] = arr[m+2]:
'''

lexer = Lexer(text)
tokens = lexer.lexer()

for token in tokens:
    print(token)

# def main():
#   source_code = ""
#    with open('text.txt', 'r') as file:
#       source_code = file.read()
#   lex = lexer.Lexer(text)
#   print(lex.tokenize())
# if "__name__" == main():
#   main()
