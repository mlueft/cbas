import re

import cbas.Compiler.Compiler

Compiler = cbas.Compiler.Compiler.Compiler

def main():
    configFile  = "/home/work/cbas/config/config.json"
    inputFile   = "/home/work/cbas/examples/main.bas"
    inputFile   = "/home/work/cbas/examples/arithmetic.bas"

    compiler = Compiler()
 
    #compiler.compileFile( inputFile, 0 )
    compiler.compileLine("4+8+3/2",0)

main()