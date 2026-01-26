import re

import cbas.Config.Config
import cbas.Compiler.Compiler

Compiler = cbas.Compiler.Compiler.Compiler

def debugLexerChainList(token):
    print("TOKENS:")
    while token:
        
        colWidth = 30
        _current = str(token)
        _prev = str(token.prev)
        _next = str(token.next)

        if len(_prev) > colWidth: _prev = _prev[:colWidth-3]+"..."
        if len(_current) > colWidth: _current = _current[:colWidth-3]+"..."
        if len(_next) > colWidth: _next = _next[:colWidth-3]+"..."
        formatstring = " * {:<"+str(colWidth)+"} <= {:<"+str(colWidth)+"} => {:<"+str(colWidth)+"}"
        print(
            formatstring.format(
                _prev,
                _current,
                _next
            )
        )

        token=token.next

def debugTokenlist(tokens):
    print("TOKENS List:")
    for t in tokens:
        print("{}".format(t))

def main():
    configFile  = "/home/work/cbas/config/config.json"
    inputFile   = "/home/work/cbas/examples/main.bas"
    #inputFile   = "/home/work/cbas/examples/arithmetic.bas"

    compiler = Compiler()
 
    compile( inputFile, configFile, 0 )

main()