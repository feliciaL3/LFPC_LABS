from parser import Parser


def main():
    code = """
    {
    m = 5*3
    m = n
    if (m<50){
        print(m / 0)
     }
    else{
        print(n * m)
    }
}
"""
    parser = Parser("text.txt")
    parser.parse()
    parser.show_ast()


if __name__ == '__main__':
    main()
