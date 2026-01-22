import io
import os

class Preprocessor():

    INCLUDE  = "#include"
    CONFIG   = "#config"
    DEFINE   = "#define"
    UNDEFINE = "#undefine"
    IFDEF    = "#ifdef"
    IFNDEF   = "#ifndef"
    ELSE     = "#else"
    ENDIF    = "#endif"
    
    def __init__(self, outputFolder, libFolders = [] ):
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
            Preprocessor.ENDIF:    self.handleEndif
        }
        self.indentation = ""
        self.writeLine = True
        self.symbolTable = {}
        
    def process(self, fileName):
        outputFileName = os.path.join( self.outputFolder,os.path.basename(fileName) )
        with io.open(fileName, "r", encoding="utf-8") as inputfile:
            with io.open(outputFileName, "w", encoding="utf-8") as outputfile:
                self._process(outputfile,inputfile)

    def getHandler(self, line):
    
        line = line.strip()
        if len(line) == 0: return None
        if line[0] != "#": return None
           
        command = line.split(" ")[0]
        if command not in self.commandHandlers: return None

        return self.commandHandlers[command]

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
        
        print(result)
        
        return result

    def getIndentation(self, line):
        if not self.keepindentation:
            return ""
        
        pos = line.find("#")
        return line[:pos]
        
    def _replaceSymbol(self,line):
        
        for s in self.symbolTable:
            line = line.replace(s,self.symbolTable[s] )
            
        return line
        
    def _process(self, outputStream, inputStream, indentation = ""):
    
        line = inputStream.readline()
        while line:
            handler = self.getHandler(line)
            if handler:
                handler(outputStream, line)
            else:
                if self.writeLine:
                    outputStream.write(indentation+self._replaceSymbol(line) )
            
            line = inputStream.readline()

    ##
    #
    #
    def handleInclude(self, outputStream, line  ):
    
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
            raise ValueError("Command {} not recognized!".format(cmd) )
            
    ##
    #
    #
    def handleDefine(self, outputStream, line  ):
        parameters = self.getParameters(line)

        assignee = parameters[0]
        if assignee not in self.symbolTable:
            self.symbolTable[assignee] = ""

        if len(parameters)==1: return
            
        value = parameters[1]
        self.symbolTable[assignee] = value
        
        #TODO: sort symbolTable by key length desc!
        
    ##
    #
    #
    def handleUndefine(self, outputStream, line  ):
        parameters = self.getParameters(line)

        assignee = parameters[0]
        if assignee in self.symbolTable:
            del self.symbolTable[assignee]
            
    ##
    #
    #
    def handleIfdef(self, outputStream, line  ):
        parameters = self.getParameters(line)

        assignee = parameters[0]
        if assignee in self.symbolTable:
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