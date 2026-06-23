import re

import cbas
import cbas.DataStructures.TraverseMode
import cbas.Ast.Expressions
import cbas.Ast.Statements
import cbas.Lexer.TokenTypes
import cbas.CodeBuilder.Tokenizer
import cbas.Compiler.SymbolTable

TraverseMode = cbas.DataStructures.TraverseMode.TraverseMode
TokenTypes = cbas.Lexer.TokenTypes.TokenTypes

BlockStatement = cbas.Ast.Statements.BlockStatement
ExpressionStatement = cbas.Ast.Statements.ExpressionStatement
InputStatement = cbas.Ast.Statements.InputStatement
PrintStatement = cbas.Ast.Statements.PrintStatement
ForStatement = cbas.Ast.Statements.ForStatement
IfStatement = cbas.Ast.Statements.IfStatement
DimStatement = cbas.Ast.Statements.DimStatement
OnExpression = cbas.Ast.Expressions.OnExpression
FunctionDefinitionStatement = cbas.Ast.Statements.FunctionDefinitionStatement
FunctionCallExpression = cbas.Ast.Expressions.FunctionCallExpression
StatementStatement = cbas.Ast.Statements.StatementStatement
CallExpression = cbas.Ast.Expressions.ProcesureCallExpression
AssignmentExpression = cbas.Ast.Expressions.AssignmentExpression
GroupingExpression = cbas.Ast.Expressions.GroupingExpression
PrefixExpression = cbas.Ast.Expressions.PrefixExpression
BinaryExpression = cbas.Ast.Expressions.BinaryExpression
PrimaryExpression = cbas.Ast.Expressions.PrimaryExpression
Tokenizer = cbas.CodeBuilder.Tokenizer.Tokenizer
SymbolKind = cbas.Compiler.SymbolTable.SymbolKind

class VariableNameManager():

    def __init__(self):
        # Reuses variable names from scopes
        self.reuseVariables = False
        self.buildGlobals = False

        self.variableNames = {}

        self.usedVariableNames = [{
            "reserved0":"DO",
            "reserved1":"DS",
            "reserved2":"DS$",
            "reserved3":"EL",
            "reserved4":"ER",
            "reserved5":"GO",
            "reserved6":"OR",
            "reserved7":"PI",
            "reserved8":"ST",
            "reserved9":"TI",
            "reserved10":"TI$",
            "reserved11":"TO",
            "reserved12":"π"

        }]
        
    ##
    #
    #
    def __isGlobal(self, symbol):
        
        if not self.buildGlobals:
            return False
        
        if (len(symbol.usages) >= 1 and symbol.kind != SymbolKind.LITERAL_STRING) or \
            (len(str(symbol.code)) > 4 and len(symbol.usages) >= 1 and symbol.kind == SymbolKind.LITERAL_STRING):
            return True
        return False
    
    ##
    #
    #
    def getGlobals(self):
        result = []

        for k,symbol in cbas.symbolTable.symbols.items():
            if symbol.isLiteral():
                if self.__isGlobal(symbol):
                    result.append(symbol)

        return result

    ##
    #
    #
    def getLiterals(self):
        result = []

        for k,symbol in cbas.symbolTable.symbols.items():
            if symbol.isLiteral():
                if not self.__isGlobal(symbol):
                    result.append(symbol)

        return result
    
    ## Opens a scope.
    #  All new variables are stored in the current scope.
    #  After closed the scope local variables will be released.
    #
    def openScope(self):
        if not self.reuseVariables:
            return
        self.usedVariableNames.append({})

    ## Closes the current scope.
    #  Local variable names will be released.
    #
    def closeScope(self):
        if not self.reuseVariables:
            return
        self.usedVariableNames.pop()
    

    # The BasicBuilder has to take care of variable names.
    # Name of the variable in generated basic code.
    ## Generates a variable name for the symbol defined by id
    #  and returns it.
    #
    def getVariableName(self,id):


        #
        # Return a already fixed variable name
        #
        if id in self.variableNames.keys():
            return self.variableNames[id]

        symbol = cbas.symbolTable.getSymbol(id)

        #
        # Generate the next free variable name.
        #
        suffix = ""
        if symbol.kind == SymbolKind.VARIABLE_STRING:
            suffix = "$"
        elif symbol.kind == SymbolKind.VARIABLE_INTEGER:
            suffix = "%"
        
        vnames0 = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        vnames1 = [""]+vnames0
        for v1 in vnames1:
            for v0 in vnames0:
                candidate = v0+v1+suffix

                found = False
                for i in range(len(self.usedVariableNames)-1,-1,-1):
                    usedVariableNames = self.usedVariableNames[i]
                    for k in usedVariableNames:
                        if usedVariableNames[k] == candidate:
                            found = True

                if not found:

                    #
                    # Store the variable name to the symbol
                    # and return the variable name.
                    #
                    self.usedVariableNames[len(self.usedVariableNames)-1][id] = candidate
                    self.variableNames[id] = candidate
                    
                    return candidate


class BasicBuilder():

    BASIC  = 0
    PRG    = 1

    def __init__(self, configIndex=2):
        self.configIndex = configIndex
        self.codeLines = []

        self.concatenateLines = False
        self.tokenizer = self._createTokenizer(configIndex)

        self.__beautifier = b""
        self.__beautify = False

        self.__EOL = b''
        if self.configIndex == BasicBuilder.BASIC:
            self.__EOL = b"\n"

        # For these Types float parameters are cast to integer
        self.castTypes = [
            TokenTypes.POKE,
            TokenTypes.PEEK,
            TokenTypes.VERIFY,
            TokenTypes.RIGHT_DOLLAR,
            TokenTypes.LEFT_DOLLAR,
            TokenTypes.CHR_DOLLAR,
            TokenTypes.MID_DOLLAR,
            TokenTypes.POS,
            TokenTypes.SPC,
            TokenTypes.TAB,
            TokenTypes.GOTO,
            TokenTypes.GOSUB,
            TokenTypes.CLOSE,
            TokenTypes.SAVE,
            TokenTypes.LOAD,
            TokenTypes.WAIT,
            TokenTypes.OPEN,
            TokenTypes.LIST,
            TokenTypes.READ,
            TokenTypes.GET_SHARP,
            TokenTypes.INPUT_SHARP,
            TokenTypes.CMD,
            TokenTypes.ON,
            TokenTypes.INPUT
        ]

        self.skipOpen = [
            TokenTypes.SPC,
            TokenTypes.TAB
        ]

        self.reuseVariables = False
        self.variableNameManager = False
        self.buildGlobals = False

    @property
    def beautify(self):
        return self.__beautify
    
    @beautify.setter
    def beautify(self,value):
        if self.__beautify == value:
            return
        
        self.__beautify = value
        self.__beautifier = b""

        if self.__beautify:
            self.__beautifier = b" "
        
    def _createTokenizer(self, configIndex):
        return Tokenizer(configIndex)

    def _createVariableNameManager(self):
        if self.variableNameManager:
            return self.variableNameManager
        
        result = VariableNameManager()
        result.reuseVariables = self.reuseVariables
        result.buildGlobals = self.buildGlobals

        return result



    def resolveSymbols(self,line):

        self.variableNameManager = self._createVariableNameManager()

        # We need a copy of line to look for { or }
        # Becase replacing symbols could add } in line.
        result = line

        #
        # OPEN SCOPE
        #
        pattern = re.compile(b".*\{.*")
        matches = pattern.findall(line)
        for match in matches:
            self.variableNameManager.openScope()


        literals = self.variableNameManager.getLiterals()
        
        #line = line.decode("ascii")
        pattern = re.compile(b"#[0-9][0-9][0-9]")
        matches = pattern.findall(result)
        for match in matches:

            #
            # Replace symbol by its literal.
            #
            for l in literals:
                if bytes(l.placeholder,"ascii") == match:

                    _type = TokenTypes.STRING
                    data = l.code
                    if l.kind == SymbolKind.LITERAL_INTEGER:
                        _type = TokenTypes.INTEGER
                        data = int(data)
                    elif l.kind == SymbolKind.LITERAL_FLOAT:
                        _type = TokenTypes.FLOAT
                        data = float(data)
                    elif l.kind == SymbolKind.LITERAL_BOOLEAN:
                        _type = TokenTypes.BOOLEAN
                                            
                    a = self.tokenizer.tokenize(_type, data)
                    result = result.replace( match,a)

            #
            # Replace symbol by its variable name.
            #
            symbolName = match
            variableName = self.variableNameManager.getVariableName(symbolName.decode("ascii"))
            
            a = bytearray(variableName.upper(),"ascii")
            result = result.replace( symbolName,a)

        #
        # CLOSE SCOPE
        #
        pattern = re.compile(b".*\}.*")
        matches = pattern.findall(line)
        for match in matches:
            self.variableNameManager.closeScope()

        return result

    def getHandler(self,node):
        _type = type(node)

        if _type == BlockStatement:return self.renderBlockStatement
        if _type == ExpressionStatement:return self.renderExpressionStatement
        if _type == InputStatement:return self.renderInputExpression
        if _type == PrintStatement:return self.renderPrintExpression
        if _type == ForStatement:return self.renderForExpression
        if _type == IfStatement:return self.renderIfExpression
        if _type == DimStatement:return self.renderDimExpression
        if _type == OnExpression:return self.renderOnExpression
        if _type == FunctionDefinitionStatement:return self.renderFunctionDefinitionExpression
        if _type == FunctionCallExpression:return self.renderFunctionCallExpression
        if _type == StatementStatement:return self.renderStatementExpression
        if _type == CallExpression:return self.renderCallExpression
        if _type == AssignmentExpression:return self.renderAssignmentExpression
        if _type == GroupingExpression:return self.renderGroupingExpression
        if _type == PrefixExpression:return self.renderPrefixExpression
        if _type == BinaryExpression:return self.renderBinaryExpression
        if _type == PrimaryExpression:return self.renderPrimaryExpression

    def astHandler(self, node, traverseMode):
        handler = self.getHandler(node)
        lines = handler(node)

        if lines is not None:
            for l in lines:
                self.codeLines.append(l)

    ## Replaces symbols with their values
    #
    #
    def __replaceSymbols(self, codeLines):
        result = []
        for line in codeLines:
            result.append( self.resolveSymbols(line) )

        return result
    
    ## Does some code cleaning.
    #  * Removes { and }
    #
    def __cleanupCodeLines(self, codeLines):
        #
        # Codelines cleanup
        # 
        result = []
        for line in codeLines:
            if line != b"{" and line != b"}":
                result.append(line)

        return result
    
    ##
    # Concatenate code lines.
    #
    # We have each statement in it's seperate line.
    # We can concatenate some of them.
    # Line length is limited to 80 chars.
    # Labeldefinitions are going to be line numbers.
    # For linenumbers are 5 chars reserved
    #  Labeldefinition are "@label_nnnnn"
    #  So we remove "@label_" to get the correct length
    #  of the command after linker.
    #
    # * Lines between { and } can be concatenated
    # * A Labeldefinition has to be in it's own line.
    # 
    # When do we need a new line?
    # * After a next
    # * after a goto/gosub
    # * before "{"
    # * before IF - not sure about this
    # * after "}"
    #
    def __concatenateLines(self, codeLines):

        if not self.concatenateLines:
            return codeLines
        
        _before = []

        result = []

        linenr = len(codeLines)-1
        while  linenr > 0 :
            line = codeLines[linenr]
            prevLine  = codeLines[linenr-1]
            if line is not None:
                concat = True

                if len(line)+len(prevLine) >= 70 - len(prevLine) + 1: concat = False 
                if prevLine == b'}': concat = False
                if line == b'}': concat = False
                if prevLine == b'{': concat = False
                if line == b'{': concat = False
                if b'@' in line: concat = False
                if b'@' in prevLine: concat = False


                if concat:
                    prevLine += self.tokenizer.tokenize(TokenTypes.COLON)
                    prevLine += line
                    codeLines[linenr-1] = prevLine
                    codeLines[linenr] = None
            linenr -= 1

        #
        # Remove wmpty Lines
        #
        tmp = []
        for l in codeLines:
            if l is not None:
                tmp.append(l)

        return tmp
    
    ## Generates the globals definition.
    #
    #
    def __generateGlobals(self, codeLines):
        #return codeLines
        result = []

        #
        #
        #
        self.variableNameManager = self._createVariableNameManager()

        globals = self.variableNameManager.getGlobals()
        for symbol in globals:
            line = bytearray()

            _type = TokenTypes.STRING
            if symbol.kind == SymbolKind.LITERAL_INTEGER:
                _type = TokenTypes.INTEGER
            elif symbol.kind == SymbolKind.LITERAL_FLOAT:
                _type = TokenTypes.FLOAT
            elif symbol.kind == SymbolKind.LITERAL_BOOLEAN:
                _type = TokenTypes.BOOLEAN

            # We don't ust variableName, but the
            # function call reserves a variable name.
            variableName = self.variableNameManager.getVariableName(symbol.placeholder)

            line = self.tokenizer.tokenize(_type, symbol.placeholder)

            line += self.tokenizer.tokenize(TokenTypes.EQ)

            line += self.tokenizer.tokenize(_type, symbol.code)

            result.append(line)
        

        #
        #
        #
        result = codeLines[:1] + result + codeLines[1:]

        return result
    
    def main(self, ast):
        self.codeLines = []

        #
        # Generate code lines
        #
        ast.topDown(self.astHandler)

        codeLines = self.codeLines

        codeLines = self.__generateGlobals(codeLines)

        codeLines = self.__replaceSymbols(codeLines)

        # tokenizer should be extracted from replaceSymbols
        codeLines = codeLines# self.__concatenateLines(codeLines)

        codeLines = self.__concatenateLines(codeLines)

        codeLines = self.__cleanupCodeLines(codeLines)

        self.codeLines = []
        for line in codeLines:
            self.codeLines.append(line+self.__EOL)

        return self.codeLines

    ##
    #
    #
    def renderBlockStatement(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True

        result = []
        result.append(b"{")

        for s in node.statements:
            handler = self.getHandler(s)
            b = handler(s)
            if b is not None:
                for b1 in b:
                    result.append(b1)

        result.append(b"}")
        
        return result
    
    ##
    #
    #
    def renderExpressionStatement(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True


        handler = node.getHandler(node.statement)
        return [handler(node.statement)]

    ## InputExpression
    #
    #
    def renderInputExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True
        

        line = bytearray()

        result = []

        # CMD
        handler = self.getHandler(node.statement)
        b = handler(node.statement)
        line += b[0]
        line += self.__beautifier

        for p in node.parameters:
            handler = self.getHandler(p)
            b = handler(p)
            line += b[0]
            if p != node.parameters[-1]:
                line += self.__beautifier

        line += self.__beautifier

        result.append(line)
        
        return result
        
    ## PrintExpression
    #
    #
    def renderPrintExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True


        line = bytearray()

        result = []

        # CMD
        handler = self.getHandler(node.statement)
        b = handler(node.statement)
        line += b[0]

        line += self.__beautifier

        for p in node.parameters:
            handler = self.getHandler(p)
            b = handler(p)
            line += b[0]
            if p != node.parameters[-1]:
                line += self.__beautifier
        
        line += self.__beautifier

        result.append(line)

        return result

    ## ForExpression
    #
    #
    def renderForExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True


        result = []
        
        line = bytearray()
        line += self.tokenizer.tokenize(TokenTypes.FOR)
        line += self.__beautifier

        handler = self.getHandler(node.runner)
        b = handler(node.runner)
        line += b[0]
        line += self.__beautifier

        #line += "="
        line += self.tokenizer.tokenize(TokenTypes.EQ)
        line += self.__beautifier

        handler = self.getHandler(node.start)
        b = handler(node.start)
        line += b[0]

        line += self.__beautifier


        #line += "to"
        line += self.tokenizer.tokenize(TokenTypes.TO)

        line += self.__beautifier
        
        handler = self.getHandler(node.end)
        b = handler(node.end)
        line += b[0]

        if node.step is not None:
            #line += "step"
            line += self.tokenizer.tokenize(TokenTypes.STEP)
            line += self.__beautifier
            handler = self.getHandler(node.step)
            b = handler(node.step)
            line += b[0]
        
        result.append(line)

        for l in node.loopCode:
            handler = self.getHandler(l)
            b = handler(l)
            if b is not None:
                for b1 in b:
                    result.append(b1)

        
        return result

    ## IfExpression
    #
    #
    def renderIfExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True

        result =  []

        handler = self.getHandler(node.condition)
        condition = handler(node.condition)
        conditionLine = condition[0]

        trueLines = self.renderBlockStatement(node.trueCode)

        # ENDIF LABEL
        endifLabel = b"@label_"+bytearray(("00000"+node.id)[-5:],"ascii")

        line = bytearray()
        # IF
        line += self.tokenizer.tokenize(TokenTypes.IF)
        line += self.__beautifier

        # condition
        line += self.tokenizer.tokenize(TokenTypes.NOT)
        line += self.tokenizer.tokenize(TokenTypes.ROUNDOPEN)
        line += conditionLine
        line += self.tokenizer.tokenize(TokenTypes.ROUNDCLOSE)
        line += self.__beautifier
        
        #THEN
        line += self.tokenizer.tokenize(TokenTypes.GOTO)
        line += self.__beautifier
        line += endifLabel

        result.append(line)

        # TRUE CODE
        for trueLine in trueLines:
            result.append(trueLine)

        # ELIF CODE

        # ELSE CODE

        # ENDIF LABEL
        line = bytearray()
        line += self.__beautifier
        line += endifLabel
        line += self.__beautifier
        result.append(line)

        return result
        
    ## DimExpression
    #
    #
    def renderDimExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True


        line = bytearray()


        line += self.tokenizer.tokenize(TokenTypes.DIM)

        line += self.__beautifier

        handler=self.getHandler( node.variable)
        r = handler(node.variable)
        line += r[0]
        #line += "("
        line += self.tokenizer.tokenize(TokenTypes.ROUNDOPEN)

        for p in node.dimensions:
            handler=self.getHandler( p)
            b = handler(p)
            line += b[0]
            if p != node.dimensions[-1]:
                #line += ","
                line += self.tokenizer.tokenize(TokenTypes.COMMA)
                line += self.__beautifier

        #line += ")"
        line += self.tokenizer.tokenize(TokenTypes.ROUNDCLOSE)

        return [line]
    
    ## OnExpression
    #
    #
    def renderOnExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True
        

        line = bytearray()
        #line += "on"
        line += self.tokenizer.tokenize(TokenTypes.ON)
        
        line += self.__beautifier
        
        handler = self.getHandler(node.index)
        b = handler(node.index)[0]
        if self.castTypes and type(node.index) == PrimaryExpression and node.index.type == TokenTypes.FLOAT:
            b = bytearray(str(int(float(b))),encoding="ascii")
        line += b
        
        line += self.__beautifier
        
        handler = self.getHandler(node.jumpMethode)
        b = handler(node.jumpMethode)
        line += b[0]
        
        line += self.__beautifier
        
        for p in node.lineNumbers:
            handler = self.getHandler(p)
            b = handler(p)[0]
            if self.castTypes and type(p) == PrimaryExpression and p.type == TokenTypes.FLOAT:
                b = bytearray(str(int(float(b))),encoding="ascii")
            line += b
            if p != node.lineNumbers[-1]:
                #line += ","
                line += self.tokenizer.tokenize(TokenTypes.COMMA)
                line += self.__beautifier
        

        return [line]

    ## FunctionDefinitionExpression
    #
    #
    def renderFunctionDefinitionExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True


        line = bytearray()
        
        #line += "def"
        line += self.tokenizer.tokenize(TokenTypes.DEF)

        line += self.__beautifier

        #line += "fn"
        line += self.tokenizer.tokenize(TokenTypes.FN)

        line += self.__beautifier

        handler = self.getHandler(node.functionName)
        b = handler(node.functionName)
        line += b[0]

        #line += "("
        line += self.tokenizer.tokenize(TokenTypes.ROUNDOPEN)

        for p in node.parameters:
            handler = self.getHandler(p)
            b = handler(p)
            line += b[0]
            if p != node.parameters[-1]:
                #line += ","
                line += self.tokenizer.tokenize(TokenTypes.COMMA)
                line += self.__beautifier
        
        #line += ")="
        line += self.tokenizer.tokenize(TokenTypes.ROUNDCLOSE)
        line += self.tokenizer.tokenize(TokenTypes.EQ)

        handler= self.getHandler(node.body)
        b = handler(node.body)
        line += b[0]

        return [line]

    ## FunctionCallExpression
    #
    #
    def renderFunctionCallExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True
        

        line = bytearray()
        
        #line += "fn"
        line += self.tokenizer.tokenize(TokenTypes.FN)

        line += self.__beautifier

        handler = self.getHandler(node.functionName)
        b = handler(node.functionName)
        line += b[0]
        
        #line += "("
        line += self.tokenizer.tokenize(TokenTypes.ROUNDOPEN)
        
        for p in node.parameters:
            handler = self.getHandler(p)
            b = handler(p)
            line += b[0]
            if p != node.parameters[-1]:
                #line += ","
                line += self.tokenizer.tokenize(TokenTypes.COMMA)

                line += self.__beautifier

        #line += ")"
        line += self.tokenizer.tokenize(TokenTypes.ROUNDCLOSE)

        return [line]
    
    ## StatementExpression
    #
    #
    def renderStatementExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True


        line = bytearray()

        #seperator = ","
        seperator = self.tokenizer.tokenize(TokenTypes.COMMA)

        if node.statement.type == TokenTypes.LIST:
            #seperator = "-"
            seperator = self.tokenizer.tokenize(TokenTypes.MINUS)

        handler = self.getHandler(node.statement)
        b = handler(node.statement)
        line += b[0]
        
        line += self.__beautifier
        

        for p in node.parameters:
            handler = self.getHandler(p)
            b = handler(p)[0]
            if node.statement.type in self.castTypes and type(p) == PrimaryExpression and p.type == TokenTypes.FLOAT:
                b = bytearray(str(int(float(b))),encoding="ascii")
            line += b
            if p != node.parameters[-1]:
                line += seperator
        
        line += self.__beautifier
        
        return [line]

    ## CallExpression
    #
    #
    def renderCallExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True


        line = bytearray()

        handler = self.getHandler(node.function)
        f = handler(node.function)
        line += f[0]
        
        #line += "("
        # tab and spc must not have a ( in prg!
        if not node.function.type in self.skipOpen or self.configIndex == BasicBuilder.BASIC:
            line += self.tokenizer.tokenize(TokenTypes.ROUNDOPEN)
        
        for p in node.parameters:
            handler = self.getHandler(p)
            
            b = handler(p)[0]
            if node.function.type in self.castTypes and type(p) == PrimaryExpression and p.type == TokenTypes.FLOAT:
                b = bytearray(str(int(float(b))),encoding="ascii")
            line += b
            
            if p != node.parameters[-1]:
                #line += ","
                line += self.tokenizer.tokenize(TokenTypes.COMMA)

                line += self.__beautifier

            #print("p"+line.decode("ascii"))

        #line += ")"
        line += self.tokenizer.tokenize(TokenTypes.ROUNDCLOSE)

        return [line]

    ## AssignmentExpression
    #
    #
    def renderAssignmentExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True


        handler = self.getHandler(node.left)

        result = []

        line = bytearray()
        r = handler(node.left)
        line += r[0]

        if line is None:
            line = ""

        handler = self.getHandler(node.right)
        right = handler(node.right)

        #line = line[0]
        
        line += self.__beautifier
        
        #line += "="
        r = self.tokenizer.tokenize(TokenTypes.EQ)
        line += r
        
        line += self.__beautifier

        line += right[0]

        result.append(line)
        return result
    
    ## GroupingExpression
    #
    #
    def renderGroupingExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True
        

        result = []

        handler = self.getHandler(node.value)

        result.append( self.tokenizer.tokenize(TokenTypes.CURLYOPEN) )
        result.append(handler(node.value))
        result.append( self.tokenizer.tokenize(TokenTypes.CURLYCLOSE) )

        return result
    
    ## PrefixExpression
    #
    #
    def renderPrefixExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True


        handler = self.getHandler(node.operator)
        op = handler(node.operator)

        handler = self.getHandler(node.right)
        right = handler(node.right)
        
        result = []
    
        result.append(op[0]+right[0])

        return result

    ## BinaryExpression
    #
    #
    def renderBinaryExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True


        handler=self.getHandler(node.left)
        bl = handler(node.left)
        
        handler=self.getHandler(node.operator)
        bo = handler(node.operator)

        handler=self.getHandler(node.right)
        br = handler(node.right)


        line = bytearray()

        line = bl[0]

        line += self.__beautifier

        line += bo[0]

        line += self.__beautifier

        line += br[0]

        result =  []
        result.append(line)
        return result
        
    ## PrimaryExpression
    #
    #
    def renderPrimaryExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True
        
        result = []

        if node.type == TokenTypes.LINEEND or node.type == TokenTypes.COLON:
            return None

        else:
            line = self.tokenizer.tokenize(node.type, node.value)

        result.append(line)

        return result
        