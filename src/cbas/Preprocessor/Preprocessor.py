import io
import os

import cbas.Compiler.Compiler
import cbas.Compiler.SymbolTable

Compiler = cbas.Compiler.Compiler.Compiler
SymbolTable = cbas.Compiler.SymbolTable.SymbolTable

class Preprocessor():

    INCLUDE  = "#include"
    CONFIG   = "#config"
    DEFINE   = "#define"
    UNDEFINE = "#undefine"
    IFDEF    = "#ifdef"
    IFNDEF   = "#ifndef"
    ELSE     = "#else"
    ENDIF    = "#endif"
    IF       = "#if"
    
    def __init__(self, outputFolder, libFolders = [] ):
        self.CONFIGID = 1
        self.keepindentation = False
        self.outputFolder = outputFolder
        self.libFolders   = libFolders
        self.commandHandlers = {
            Preprocessor.INCLUDE:  self.handleInclude,
            Preprocessor.CONFIG:   self.handleConfig,
            Preprocessor.DEFINE:   self.handleDefine,
            Preprocessor.UNDEFINE: self.handleUndefine,
            Preprocessor.IFDEF:    self.handleIfdef,
            Preprocessor.IFNDEF:   self.handleIfNdef,
            Preprocessor.ELSE:     self.handleElse,
            Preprocessor.ENDIF:    self.handleEndif,
            Preprocessor.IF:       self.handleIf
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
                    outputStream.write(indentation+self.symbolTable.replaceSymbols(line) )
            
            line = inputStream.readline()

    ##
    #
    #
    def handleInclude(self, outputStream, line  ):
    
        self.indentation = ""
        if self.keepindentation:
            self.indentation += self.getIndentation(line)

        parameters = self.getParameters(line)
        
        # looking for the include file.
        for f in self.libFolders:
            includeFile = os.path.join(f,parameters[0])
            if os.path.isfile( includeFile ):
            
                # we open the include file
                with io.open(includeFile, "r", encoding="utf-8") as includefile:
                    self._process(outputStream, includefile, self.indentation)
                
                outputStream.write("\n")
                self.indentation = self.getIndentation(line)

    ##
    #
    #
    def handleConfig(self, outputStream, line  ):
        parameters = self.getParameters(line)
        cmd = parameters[0]
        value = parameters[1]
        
        if cmd.lower() == "keepindentation":
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
        line = line[len(Preprocessor.DEFINE):].lstrip()

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

        self.symbolTable.addSymbol( macroName, line.lstrip(), params )
        
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
        expr = line[len(Preprocessor.IF):].strip()

        expr = self.symbolTable.replaceSymbols(expr)

        compiler = Compiler()
        result = compiler.compileExpression(expr, self.CONFIGID )

        if len(result.statements) != 1:
            raise ValueError("If-Condition couldn't be evaluated!: "+line)

        self.writeLine = result.statements[0].value

