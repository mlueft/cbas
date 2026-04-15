

def main():
    inputFile   = "/home/work/cbas/examples/Subsonic.prg"

    pos = 0
    with open(inputFile,"r") as file:
        content = file.read()
        print(content[pos])
        pos += 1

    file.close()

main()