#from cbas.Parser import *
#from cbas.Lexer import *
#from cbas.Ast import *
#from cbas.TokenChainOptimizer import *
#from cbas.Config import *
import cbas.Compiler.SymbolTable
import cbas.Compiler.LabelTable
import cbas.Logger

debug = False

def log(message,logLevel="info"):
    if logLevel == "debug" and not cbas.debug:
        return
    
    cbas.Logger.Logger.log(message, logLevel)

symbolTable = cbas.Compiler.SymbolTable.SymbolTable()
labelTable = cbas.Compiler.LabelTable.LabelTable()
