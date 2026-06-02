import io
import os

import cbas
import cbas.Compiler.Compiler
import cbas.Preprocessor.SymbolTable
import cbas.Config.Config

Compiler = cbas.Compiler.Compiler.Compiler
SymbolTable = cbas.Preprocessor.SymbolTable.SymbolTable
Config = cbas.Config.Config.Config

##
#
#
class RuntimeState():
    def __init__(self):
        self.__values=[]
        self.push()

    def push(self):
        self.__values.append({})

    def pop(self):
        if len(self.__values)==1:
            return
        
        self.__values.pop()

    def get(self, key):
        #
        # We search the Stack for the first value
        #
        i = len(self.__values)-1
        while i >=0:
            if key in self.__values[i]:
                return self.__values[i][key]
            i-=1

        return None

    def set(self, key, value):
        self.__values[len(self.__values)-1][key] = value

class Preprocessor():

    #
    # Preprocessor directives to be used in source file.
    #
    CMD_INCLUDE  = "#include"
    CMD_PRAGMA   = "#pragma"
    CMD_DEFINE   = "#define"
    CMD_UNDEFINE = "#undefine"
    CMD_IFDEF    = "#ifdef"
    CMD_IFNDEF   = "#ifndef"
    CMD_ELSE     = "#else"
    CMD_ENDIF    = "#endif"
    CMD_IF       = "#if"
    
    CK_KEEP_INDENTATION = "keepindentation"

    ST_KEEP_INDENTATION = 0
    ST_WRITE_LINE = 1
    ST_INDENTATION = 2

    def __init__(self):
        
        self.__symbolTable = self._createSymboltable()
        self.__runTimeState = self._createRuntimeState()
        self.__runTimeState.set(Preprocessor.ST_KEEP_INDENTATION, False )

        # Stores the current indentation
        self.__runTimeState.set(Preprocessor.ST_INDENTATION, "" )

        # Defines if the line of the input file
        # is written to the output file.
        self.__runTimeState.set(Preprocessor.ST_WRITE_LINE, True )

        self.__commandHandlers = {
            Preprocessor.CMD_INCLUDE:  self.__handleInclude,
            Preprocessor.CMD_PRAGMA:   self.__handlePragma,
            Preprocessor.CMD_DEFINE:   self.__handleDefine,
            Preprocessor.CMD_UNDEFINE: self.__handleUndefine,
            Preprocessor.CMD_IFDEF:    self.__handleIfdef,
            Preprocessor.CMD_IFNDEF:   self.__handleIfNdef,
            Preprocessor.CMD_ELSE:     self.__handleElse,
            Preprocessor.CMD_ENDIF:    self.__handleEndif,
            Preprocessor.CMD_IF:       self.__handleIf
        }
        
        self.outputFolder = None
        self.libFolders   = []

        
    ##
    #
    #     
    def _createRuntimeState(self):
        return RuntimeState()
    
    ##
    #
    #
    def _createSymboltable(self):
        return SymbolTable()
    
    ##
    #
    #
    def main(self, inputFileName, outputFileName):
        
        # absolute path for the input file.
        #outputFileName = os.path.join( self.outputFolder,os.path.basename(inputFileName)+".pass1" )
        
        # Creates a file object for the input file.
        with io.open(inputFileName, "r", encoding="utf-8") as inputfile:

            # Creates a file object for the output file.
            with io.open(outputFileName, "w", encoding="utf-8") as outputfile:

                # Runs the preprocessor for the input file.
                self.__main(outputfile,inputfile)
    
    ## Processes the input file.
    #
    # 
    def __main(self, outputStream, inputStream):
    
        # Read the first line
        line = self.__readLine(inputStream)

        while line:
            handler = self.__getHandler(line)
            if handler:

                if not self.__runTimeState.get(Preprocessor.ST_WRITE_LINE):
                    # if we are in a false if-block
                    # we are just waiting for else or endif
                    if handler in(self.__handleElse,self.__handleEndif):
                        handler(outputStream, line)
                else:
                    # We have a handler, so the line is a preprocessor directive.
                    handler(outputStream, line)

            else:

                # We don't have a handler, so the line is regular source code
                # we write it in the output file.
                if self.__runTimeState.get(Preprocessor.ST_WRITE_LINE):
                    outputStream.write(self.__runTimeState.get(Preprocessor.ST_INDENTATION)+self.__symbolTable.replaceSymbols(line) )
            
            # Read next line.
            line = self.__readLine(inputStream)

    ## Returns the handler to the pp directive in line.
    #
    #
    def __getHandler(self, line):
    
        line = line.strip()
        if len(line) == 0: return None
        if line[0] != "#": return None
           
        command = line.split(" ")[0]
        if command not in self.__commandHandlers: return None

        return self.__commandHandlers[command]

    ## Returns a list of strings
    #  represensting all Parameters
    #  to a pp directive.
    #
    def __getParameters(self,line):
        
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
    def __getIndentation(self, line):
        if not self.__runTimeState.get(Preprocessor.ST_KEEP_INDENTATION):
            return ""
        
        pos = line.find("#")
        return line[:pos]

    ##
    #
    #
    def __readLine(self, inputStream):
        
        result = ""

        line = inputStream.readline()
        line = line.strip("\n")

        # EOF?
        if line == "":
            return line
        
        if line[-1:] == "_":

            # We concatenate the next line.
            while line[-1:] == "_":
                result += line[:-1]
                line = inputStream.readline()

            result += line+"\n"

        else:
            # We are just returning the next line.
            result = line+"\n"


        return result
    
    ## Handles #include
    #
    #
    def __handleInclude(self, outputStream, line  ):
    
        self.__runTimeState.push()

        #
        # We add the indentation of the include statement
        # So the included file stays at the column of the include statement.
        #
        if self.__runTimeState.get(Preprocessor.ST_KEEP_INDENTATION):
            self.__runTimeState.set(Preprocessor.ST_INDENTATION, self.__runTimeState.get(Preprocessor.ST_INDENTATION)+self.__getIndentation(line) )

        #
        # We read the name of the file to include.
        # (All parameters of the include statement.)
        #
        parameters = self.__getParameters(line)
        
        #
        # looking for the include file.
        #
        for f in self.libFolders:
            pathIncludeFile = os.path.join(f,parameters[0])
            if os.path.isfile( pathIncludeFile ):
            
                # We found it so we include it.
                # we open the include file
                with io.open(pathIncludeFile, "r", encoding="utf-8") as includefile:
                    # We need indentation as parameter, because it could be changed
                    # in the includes file.
                    self.__main(outputStream, includefile)#, self.indentation)
                
                # At the end we need to write a line break
                # Because there is a linebreak at the end of
                # include directive.
                outputStream.write( "\n" )

        self.__runTimeState.pop()

    ## Handles #config
    #
    #
    def __handlePragma(self, outputStream, line  ):
        parameters = self.__getParameters(line)
        cmd = parameters[0]
        value = parameters[1]
        
        if cmd.lower() == Preprocessor.CK_KEEP_INDENTATION:
            self.__runTimeState.set(Preprocessor.ST_KEEP_INDENTATION, value.lower() == "true" )
            
        else:
            raise ValueError("Config command {} not recognized!".format(cmd) )
            
    ## Handles #define
    #
    #
    def __handleDefine(self, outputStream, line  ):

        # line cleaning.
        line = line.lstrip()
        line = line.rstrip("\n")

        # We remove the '#define' string
        line = line[len(Preprocessor.CMD_DEFINE):].lstrip()

        # We extract the macro name
        # The macro name ends at space or '('
        macroName = ""
        hasParams = False
        params = []
        while len(line) > 0:
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
            # We extract the parameter definition
            paramString = line[:line.find(")")+1].strip()
            line        = line[len(paramString):]

            # We remove "(" and ")"
            paramString = paramString[1:-1].strip()

            params = paramString.split(",")
            for i,v in enumerate(list(params)):
                params[i] = v.strip()

        # Add symbol to symbol table.
        self.__symbolTable.addSymbol( macroName, line.lstrip(), params )
        
    ## Handles #undefine
    #
    #
    def __handleUndefine(self, outputStream, line  ):
        parameters = self.__getParameters(line)
        assignee = parameters[0]
        self.__symbolTable.removeSymbol(assignee)

    ## Handles #ifdef
    #
    #
    def __handleIfdef(self, outputStream, line  ):
        parameters = self.__getParameters(line)

        assignee = parameters[0]
        if self.__symbolTable.symbolExists(assignee):
            self.__runTimeState.set(Preprocessor.ST_WRITE_LINE, True )
        else:
            self.__runTimeState.set(Preprocessor.ST_WRITE_LINE, False )
            
    ## Handles #ifndef
    #
    #
    def __handleIfNdef(self, outputStream, line  ):
        # We validate the if statement.
        self.__handleIfdef(outputStream,line)
        # We inverse the writeLine state
        self.__handleElse(outputStream,line)

    ## Handles #else
    #
    #
    def __handleElse(self, outputStream, line  ):
            self.__runTimeState.set(Preprocessor.ST_WRITE_LINE, not self.__runTimeState.get(Preprocessor.ST_WRITE_LINE))

    ## Handles #endif
    #
    #       
    def __handleEndif(self, outputStream, line  ):
            self.__runTimeState.set(Preprocessor.ST_WRITE_LINE, True )

    ##
    #
    #
    def __handleIf(self, outputStream, line  ):
        
        # line cleaning.
        line = line.lstrip()
        line = line.rstrip("\n")

        # removes the #if
        expr = line[len(Preprocessor.CMD_IF):].strip()

        # We take the expression and replace indentifiers with
        # their values.
        expr = self.__symbolTable.replaceSymbols(expr)
        
        # We take an compiler for the preprocessor
        # and validate the expression.
        compiler = Compiler(Config.PREPROCESSOR)
        result = compiler.compileExpression(expr )

        # If we don't get and result
        # something went wrong.
        if len(result.statements) != 1:
            raise ValueError("If-Condition couldn't be evaluated!: "+line)

        # If the validation results in true,
        # We write the next lines.
        self.__runTimeState.set(Preprocessor.ST_WRITE_LINE,result.statements[0].value)

