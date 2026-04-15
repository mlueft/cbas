import io
import os

import cbas.Compiler.Compiler
import cbas.Preprocessor.SymbolTable
import cbas.Config.Config

Compiler = cbas.Compiler.Compiler.Compiler
SymbolTable = cbas.Preprocessor.SymbolTable.SymbolTable
Config = cbas.Config.Config.Config

class Preprocessor():

    CMD_INCLUDE  = "#include"
    CMD_CONFIG   = "#config"
    CMD_DEFINE   = "#define"
    CMD_UNDEFINE = "#undefine"
    CMD_IFDEF    = "#ifdef"
    CMD_IFNDEF   = "#ifndef"
    CMD_ELSE     = "#else"
    CMD_ENDIF    = "#endif"
    CMD_IF       = "#if"
    
    CK_KEEP_INDENTATION = "keepindentation"

    def __init__(self, outputFolder, libFolders = [] ):
        self.keepindentation = False
        self.outputFolder = outputFolder
        self.libFolders   = libFolders
        self.commandHandlers = {
            Preprocessor.CMD_INCLUDE:  self.handleInclude,
            Preprocessor.CMD_CONFIG:   self.handleConfig,
            Preprocessor.CMD_DEFINE:   self.handleDefine,
            Preprocessor.CMD_UNDEFINE: self.handleUndefine,
            Preprocessor.CMD_IFDEF:    self.handleIfdef,
            Preprocessor.CMD_IFNDEF:   self.handleIfNdef,
            Preprocessor.CMD_ELSE:     self.handleElse,
            Preprocessor.CMD_ENDIF:    self.handleEndif,
            Preprocessor.CMD_IF:       self.handleIf
        }
        self.indentation = ""
        self.writeLine = True
        self.symbolTable = SymbolTable()
        
    def process(self, fileName):
        outputFileName = os.path.join( self.outputFolder,os.path.basename(fileName) )
        with io.open(fileName, "r", encoding="utf-8") as inputfile:
            with io.open(outputFileName, "w", encoding="utf-8") as outputfile:
                self._process(outputfile,inputfile)

    ## Returns the handler to the pp directive in line.
    #
    #
    def getHandler(self, line):
    
        line = line.strip()
        if len(line) == 0: return None
        if line[0] != "#": return None
           
        command = line.split(" ")[0]
        if command not in self.commandHandlers: return None

        return self.commandHandlers[command]

    ## Returns a list of strings
    #  represensting all Parameters
    #  to a pp directive.
    #
    def getParameters(self,line):
        
        result = []
        
        line = line.strip()
        
        # TODO: Spaces in values will break this!
        parts = line.split(" ")
        
        for i,p in enumerate(parts):
            if i == 0:
                continue
                
            p = p.strip()
            p = p.strip("\"")
            result.append( p )
        
        return result

    ## Returns the indentation string
    #  of the line.
    #
    def getIndentation(self, line):
        if not self.keepindentation:
            return ""
        
        pos = line.find("#")
        return line[:pos]
        
    def _process(self, outputStream, inputStream, indentation = ""):
    
        line = inputStream.readline()
        while line:
            handler = self.getHandler(line)
            if handler:
                handler(outputStream, line)
            else:
                if self.writeLine:
                    print(indentation+self.symbolTable.replaceSymbols(line) )
                    outputStream.write(indentation+self.symbolTable.replaceSymbols(line) )
            
            line = inputStream.readline()

    ##
    #
    #
    def handleInclude(self, outputStream, line  ):
    
        #self.indentation = ""
        localIndentation = self.getIndentation(line)
        restoreki=self.keepindentation

        if restoreki:
            self.indentation += localIndentation

        parameters = self.getParameters(line)
        
        # looking for the include file.
        for f in self.libFolders:
            includeFile = os.path.join(f,parameters[0])
            if os.path.isfile( includeFile ):
            
                # we open the include file
                with io.open(includeFile, "r", encoding="utf-8") as includefile:
                    self._process(outputStream, includefile, self.indentation)
                
                #outputStream.write("\n")
                self.indentation = self.getIndentation(line)

        if restoreki:
            self.indentation = self.indentation[:-len(localIndentation)]

    ##
    #
    #
    def handleConfig(self, outputStream, line  ):
        parameters = self.getParameters(line)
        cmd = parameters[0]
        value = parameters[1]
        
        if cmd.lower() == Preprocessor.CK_KEEP_INDENTATION:
            self.keepindentation = value.lower() == "true"
            
        else:
            raise ValueError("Config command {} not recognized!".format(cmd) )
            
    ##
    #
    #
    def handleDefine(self, outputStream, line  ):

        line = line.lstrip()
        line = line.rstrip("\n")

        # We remove the '#define' string
        line = line[len(Preprocessor.CMD_DEFINE):].lstrip()

        # We extract the macro name
        # The macro name ends at space or '('
        macroName = ""
        hasParams = False
        params = []
        while True and len(line) > 0:
            c = line[0]
            
            if c == " ":
                # if the macro name ends with ' ' it's object like.
                break

            if c == "(":
                # If the macro name ends with '(' it's function like.
                hasParams = True
                break

            macroName += c

            line = line[1:]

        if hasParams:
            paramString = line[:line.find(")")+1].strip()
            line        = line[len(paramString):]

            paramString = paramString[1:-1].strip()

            params = paramString.split(",")
            for i,v in enumerate(list(params)):
                params[i] = v.strip()

        id = self.symbolTable.addSymbol( macroName, line.lstrip(), params )
        
    ##
    #
    #
    def handleUndefine(self, outputStream, line  ):
        parameters = self.getParameters(line)
        assignee = parameters[0]
        self.symbolTable.removeSymbol(assignee)

    ##
    #
    #
    def handleIfdef(self, outputStream, line  ):
        parameters = self.getParameters(line)

        assignee = parameters[0]
        if self.symbolTable.symbolExists(assignee):
            self.writeLine = True
        else:
            self.writeLine = False
            
    ##
    #
    #
    def handleIfNdef(self, outputStream, line  ):
        self.handleIfdef(outputStream,line)
        self.handleElse(outputStream,line)

    ##
    #
    #
    def handleElse(self, outputStream, line  ):
            self.writeLine = not self.writeLine

    ##
    #
    #       
    def handleEndif(self, outputStream, line  ):
            self.writeLine = True

    ##
    #
    #
    def handleIf(self, outputStream, line  ):
        expr = line[len(Preprocessor.CMD_IF):].strip()

        print(expr)
        expr = self.symbolTable.replaceSymbols(expr)
        print(expr)
        
        compiler = Compiler(Config.PREPROCESSOR)
        result = compiler.compileExpression(expr )

        if len(result.statements) != 1:
            raise ValueError("If-Condition couldn't be evaluated!: "+line)
        else:
            pass

        self.writeLine = result.statements[0].value

