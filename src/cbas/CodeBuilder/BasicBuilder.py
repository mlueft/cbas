import re

import cbas
import cbas.DataStructures.TraverseMode
import cbas.Ast.Expressions
import cbas.Ast.Statements
import cbas.Lexer.TokenTypes
import cbas.CodeBuilder.Tokenizer

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

class BasicBuilder():

    BASIC  = 0
    PRG    = 1

    def __init__(self, configIndex=2, prettify=True):
        self.configIndex = configIndex
        self.codeLines = []
        self.prettify = prettify
        self.tokenizer = self._createTokenizer(configIndex)

        self.prittifier = b""
        if prettify:
            self.prittifier = b" "

        self.EOL = b''
        if self.configIndex == BasicBuilder.BASIC:
            self.EOL = b"\n"

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

    def _createTokenizer(self, configIndex):
        return Tokenizer(configIndex)
    
    def resolveSymbols(self,line):

        #
        # OPEN SCOPE
        #
        pattern = re.compile(b".*\{.*")
        matches = pattern.findall(line)
        for match in matches:
            cbas.symbolTable.openScope()


        #line = line.decode("ascii")
        pattern = re.compile(b"#[0-9][0-9][0-9]")
        matches = pattern.findall(line)
        for match in matches:
            symbolName = match
            variableName = cbas.symbolTable.getVariable(symbolName.decode("ascii"))
            
            a = bytearray(variableName.upper(),"ascii")
            line = line.replace( symbolName,a)

        #
        # CLOSE SCOPE
        #
        pattern = re.compile(b".*\}.*")
        matches = pattern.findall(line)
        for match in matches:
            cbas.symbolTable.closeScope()

        return line

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
                self.codeLines.append(l+self.EOL)

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

            # Seperate code parts and strings
            # We have to break up the line into a list
            # of code and string literals.
            #
            parts = []
            pos = 0
            partLine = bytearray()
            while pos < len(line):
                c = line[pos]
                
                if c == b'"'[0]:

                    parts.append(partLine.rstrip(b"\n"))
                    partLine = bytearray()

                    # a string starts
                    partLine += c.to_bytes(length=1, byteorder='big')

                    # we read till the end of the string
                    while pos < len(line)-1:
                        pos += 1
                        c = line[pos]
                        if c != b'"'[0]:
                            partLine += c.to_bytes(length=1, byteorder='big')
                        else:
                            # end of string reached
                            partLine += c.to_bytes(length=1, byteorder='big')
                            parts.append(partLine.rstrip(b"\n"))
                            partLine = bytearray()

                else:
                    partLine += c.to_bytes(length=1, byteorder='big')

                pos += 1

            parts.append(partLine.rstrip(b"\n"))


            #
            # Remove empty parts
            #
            tmp1 = []
            for p in parts:
                if len(p)>0:
                    tmp1.append(p)
            parts=tmp1


            #
            # Remove SCOPE definitions
            #
            isScope=False
            pattern = re.compile(b".*[\{\}].*")
            i=0
            while i < len(parts):
                part=parts[i]
                if part[0] != b'"'[0]:
                    matches = pattern.findall(part)
                    if matches:
                        isScope=True

                i+=1

            if not isScope:
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

        _before = []

        result = []

        linenr = len(codeLines)-1
        while  linenr > 0 :
            line = codeLines[linenr].rstrip(b"\n")
            prevLine  = codeLines[linenr-1].rstrip(b"\n")
            if line is not None:
                concat = True

                if len(line)+len(prevLine) >= 80 - len(prevLine) + 1: concat = False 
                if prevLine == b'}': concat = False
                if line == b'}': concat = False
                if prevLine == b'{': concat = False
                if line == b'{': concat = False
                if b'@' in line: concat = False
                if b'@' in prevLine: concat = False


                if concat:
                    prevLine += self.tokenizer.tokenize(TokenTypes.COLON)
                    prevLine += line
                    codeLines[linenr-1] = prevLine+self.EOL
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
    
    def main(self, ast):
        self.codeLines = []

        #
        # Generate code lines
        #
        ast.topDown(self.astHandler)

        codeLines = self.__replaceSymbols(self.codeLines)

        codeLines = self.__concatenateLines(codeLines)

        codeLines = self.__cleanupCodeLines(codeLines)

        self.codeLines = codeLines

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
        line += self.prittifier

        for p in node.parameters:
            handler = self.getHandler(p)
            b = handler(p)
            line += b[0]
            if p != node.parameters[-1]:
                line += self.prittifier

        line += self.prittifier

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

        line += self.prittifier

        for p in node.parameters:
            handler = self.getHandler(p)
            b = handler(p)
            line += b[0]
            if p != node.parameters[-1]:
                line += self.prittifier
        
        line += self.prittifier

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
        line += self.prittifier

        handler = self.getHandler(node.runner)
        b = handler(node.runner)
        line += b[0]
        line += self.prittifier

        #line += "="
        line += self.tokenizer.tokenize(TokenTypes.EQ)
        line += self.prittifier

        handler = self.getHandler(node.start)
        b = handler(node.start)
        line += b[0]

        line += self.prittifier


        #line += "to"
        line += self.tokenizer.tokenize(TokenTypes.TO)

        line += self.prittifier
        
        handler = self.getHandler(node.end)
        b = handler(node.end)
        line += b[0]

        if node.step is not None:
            #line += "step"
            line += self.tokenizer.tokenize(TokenTypes.STEP)
            line += self.prittifier
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
        line += self.prittifier

        # condition
        line += self.tokenizer.tokenize(TokenTypes.NOT)
        line += self.tokenizer.tokenize(TokenTypes.ROUNDOPEN)
        line += conditionLine
        line += self.tokenizer.tokenize(TokenTypes.ROUNDCLOSE)
        line += self.prittifier
        
        #THEN
        line += self.tokenizer.tokenize(TokenTypes.GOTO)
        line += self.prittifier
        line += endifLabel

        result.append(line)

        # TRUE CODE
        for trueLine in trueLines:
            result.append(trueLine)

        # ELIF CODE

        # ELSE CODE

        # ENDIF LABEL
        line = bytearray()
        line += self.prittifier
        line += endifLabel
        line += self.prittifier
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


        #line += "dim"
        line += self.tokenizer.tokenize(TokenTypes.DIM)

        line += self.prittifier

        #b = node.variable.toBasic()
        handler=self.getHandler( node.variable)
        r = handler(node.variable)
        line += r[0]
        #line += "("
        line += self.tokenizer.tokenize(TokenTypes.ROUNDOPEN)

        for p in node.dimensions:
            #b = p.toBasic()
            handler=self.getHandler( p)
            b = handler(p)
            line += b[0]
            if p != node.dimensions[-1]:
                #line += ","
                line += self.tokenizer.tokenize(TokenTypes.COMMA)
                line += self.prittifier

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
        
        line += self.prittifier
        
        handler = self.getHandler(node.index)
        b = handler(node.index)[0]
        if self.castTypes and type(node.index) == PrimaryExpression and node.index.type == TokenTypes.FLOAT:
            b = bytearray(str(int(float(b))),encoding="ascii")
        line += b
        
        line += self.prittifier
        
        handler = self.getHandler(node.jumpMethode)
        b = handler(node.jumpMethode)
        line += b[0]
        
        line += self.prittifier
        
        for p in node.lineNumbers:
            handler = self.getHandler(p)
            b = handler(p)[0]
            if self.castTypes and type(p) == PrimaryExpression and p.type == TokenTypes.FLOAT:
                b = bytearray(str(int(float(b))),encoding="ascii")
            line += b
            if p != node.lineNumbers[-1]:
                #line += ","
                line += self.tokenizer.tokenize(TokenTypes.COMMA)
                line += self.prittifier
        

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

        line += self.prittifier

        #line += "fn"
        line += self.tokenizer.tokenize(TokenTypes.FN)

        line += self.prittifier

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
                line += self.prittifier
        
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

        line += self.prittifier

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

                line += self.prittifier

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
        
        line += self.prittifier
        

        for p in node.parameters:
            handler = self.getHandler(p)
            b = handler(p)[0]
            if node.statement.type in self.castTypes and type(p) == PrimaryExpression and p.type == TokenTypes.FLOAT:
                b = bytearray(str(int(float(b))),encoding="ascii")
            line += b
            if p != node.parameters[-1]:
                line += seperator
        
        line += self.prittifier
        
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

                line += self.prittifier

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
        
        line += self.prittifier
        
        #line += "="
        r = self.tokenizer.tokenize(TokenTypes.EQ)
        line += r
        
        line += self.prittifier

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

        #result.append("{")
        result.append( self.tokenizer.tokenize(TokenTypes.CURLYOPEN) )
        result.append(handler(node.value))
        #result.append("}")
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

        line += self.prittifier

        line += bo[0]

        line += self.prittifier

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

        elif node.tag == "None":
            line = ""
        
        elif node.tag == "boolean":
            if node.value:
                line = self.tokenizer.tokenize(TokenTypes.TRUE)
            else:
                line = self.tokenizer.tokenize(TokenTypes.FALSE)

        else:
            #line = bytearray(str(node.value),"ascii")
            line = self.tokenizer.tokenize(node.type, node.value)

        result.append(line)

        return result
        