import cbas
import cbas.Lexer.TokenTypes
import cbas.Ast.Expressions
import cbas.Parser.BindingPower
import cbas.Parser.Lookups
import cbas.Events.EventManager
import cbas.Events.Event
import cbas.DataStructures.LinkedList
import cbas.DataStructures.TreeNode

Lookups = cbas.Parser.Lookups.Lookups
BindingPower = cbas.Parser.BindingPower.BindingPower
ExpressionParser = cbas.Ast.Expressions.ExpressionParser
EventManager = cbas.Events.EventManager.EventManager
Event = cbas.Events.Event.Event
LinkedList = cbas.DataStructures.LinkedList.LinkedList
TreeNode = cbas.DataStructures.TreeNode.TreeNode
TokenTypes = cbas.Lexer.TokenTypes.TokenTypes
PrimaryExpression = cbas.Ast.Expressions.PrimaryExpression


class StatementParser():
    
    ##
    #
    #
    @staticmethod
    def parseStatement(parser):
        cbas.log("start:parseStatement ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        tokenType = parser.currentTokenType

        if tokenType in Lookups.statement:
            statementFunction = Lookups.Lookups.statement[tokenType]
            result = statementFunction()
            cbas.log("end:parseStatement", "debug" )
            return result

        expression = ExpressionParser.parseExpression( parser, 0)
        #p.expect(TokenTypes.SEMICOLON)

        result = expression

        cbas.log("end:parseStatement", "debug" )
        return result
        
    ##
    #
    #
    @staticmethod
    def parseBlockStatement(parser):
        cbas.log("start:parseBlockStatement()", "debug")

        # we skip {
        start = parser.expect(TokenTypes.CURLYOPEN)
        
        statements = []
        ct = parser.currentTokenType
        while parser.hasTokens and ct != TokenTypes.CURLYCLOSE:
            statements.append( StatementParser.parseStatement(parser) )
            ct = parser.currentTokenType
        
        # We skip }
        parser.expect( TokenTypes.CURLYCLOSE )

        cbas.log("end:parseBlockStatement()", "debug")
        return BlockStatement(statements)

    ##
    #
    #
    @staticmethod
    def parseIFStatement(parser):
        cbas.log("start:parseIFExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        
        # We skip "if"
        parser.expect(TokenTypes.IF)

        condition = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)

        # We skip THEN
        parser.advance([TokenTypes.THEN])

        if parser.currentTokenType == TokenTypes.CURLYOPEN:
            # we have a scope after THEN

            trueCode = StatementParser.parseBlockStatement(parser)

        else:
            trueCode = []
            # We have a single command after THEN
            while parser.currentTokenType not in [TokenTypes.LINEEND,TokenTypes.EOF, TokenTypes.LINENUMBER]:
                
                right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)
                trueCode.append(right)
                
                # We skip ":"
                parser.advance(TokenTypes.COLON)
        
            trueCode = BlockStatement(trueCode)

        result = IfStatement(condition, trueCode)
        cbas.log("end:parseIFExpression", "debug" )
        return result

    ##
    #
    #
    @staticmethod
    def parseListStatement(parser):
        cbas.log("start:parseListStatement ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        statement = ExpressionParser.parsePrimaryExpression(parser)
        #right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)
        parameters = []

        if parser.currentTokenType not in [TokenTypes.LINEEND,TokenTypes.COLON,TokenTypes.EOF, TokenTypes.LINENUMBER]:
            right = ExpressionParser.parsePrimaryExpression(parser)
            parameters.append(right)
            
            if parser.currentTokenType == TokenTypes.MINUS:
                # We skip the "-"
                parser.advance(TokenTypes.MINUS)

                right = ExpressionParser.parsePrimaryExpression(parser)
                parameters.append(right)

        result = StatementStatement(statement,parameters)
        cbas.log("end:parseListStatement", "debug" )
        return result

    ##
    #
    #
    @staticmethod
    def parseCMDStatement(parser):
        cbas.log("start:parseCMDExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        statement = ExpressionParser.parsePrimaryExpression(parser)
        #right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)
        parameters = []
        while parser.currentTokenType not in [TokenTypes.LINEEND,TokenTypes.COLON,TokenTypes.EOF, TokenTypes.LINENUMBER]:
            right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)
            parameters.append(right)
            
            # We skip , or ;
            parser.advance( TokenTypes.COMMA )
            parser.advance( TokenTypes.SEMICOLON )

        result =  StatementStatement(statement,parameters)
        cbas.log("end:parseCMDExpression", "debug" )
        return result

    ##
    #
    #
    @staticmethod
    def parseINPUTStatement(parser):
        cbas.log("start:parseINPUTExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        statement = ExpressionParser.parsePrimaryExpression(parser)

        parameters = []
        while parser.currentTokenType not in [TokenTypes.LINEEND,TokenTypes.COLON,TokenTypes.EOF, TokenTypes.LINENUMBER]:
            right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)
            parameters.append(right)
            
            # For input we collect the seperator too.
            if parser.currentTokenType in [TokenTypes.COMMA, TokenTypes.SEMICOLON]:
                seperator = ExpressionParser.parsePrimaryExpression(parser)
                parameters.append(seperator)

        cbas.log("end:parseINPUTExpression", "debug" )
        result = InputStatement(statement,parameters)
        return result

    ##
    #
    #
    @staticmethod
    def parsePRINTStatement(parser):
        cbas.log("start:parsePRINTExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        statement = ExpressionParser.parsePrimaryExpression(parser)
        #right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)
        
        parameters = []
        while parser.currentTokenType not in [TokenTypes.LINEEND,TokenTypes.COLON,TokenTypes.EOF, TokenTypes.LINENUMBER,TokenTypes.CURLYCLOSE]:
            right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)
            parameters.append(right)
            
            # For print we collect the seperator too.
            if parser.currentTokenType in [TokenTypes.COMMA, TokenTypes.SEMICOLON]:
                seperator = ExpressionParser.parsePrimaryExpression(parser)
                parameters.append(seperator)

        result = PrintStatement(statement,parameters)
        cbas.log("end:parsePRINTExpression", "debug" )
        return result
      
    ##
    #  NEW
    #  CLR
    #  RESTORE
    #
    @staticmethod
    def parseStatementCallStatement(parser):
        cbas.log("start:parseStatementExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        statement = ExpressionParser.parsePrimaryExpression(parser)
        #right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)
        parameters = []

        while parser.currentTokenType not in [TokenTypes.LINEEND,TokenTypes.COLON,TokenTypes.EOF, TokenTypes.LINENUMBER]:
            if parser.currentTokenType == TokenTypes.COMMA:
                t=PrimaryExpression( "None", None, None )
                parameters.append(t)
                #parser.advance()
            else:
                right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)
                parameters.append(right)
            
            # We skip the ,
            parser.advance(TokenTypes.COMMA)
        
        if parser.lastTokenType == TokenTypes.COMMA:
            t=PrimaryExpression( "None", None, None )
            parameters.append(t)
            parser.advance()

        result = StatementStatement(statement,parameters)
        cbas.log("end:parseStatementExpression", "debug" )
        return result

    ##
    #
    #
    @staticmethod
    def parseDEFStatement(parser):
        cbas.log("start:parseDEFExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        
        # we skip def
        parser.expect(TokenTypes.DEF)
        
        # we skip fn
        parser.expect(TokenTypes.FN)

        functionName = ExpressionParser.parsePrimaryExpression(parser)

        # we skip (
        parser.expect(TokenTypes.ROUNDOPEN)

        parameters = []
        while parser.currentTokenType not in [TokenTypes.LINEEND,TokenTypes.ROUNDCLOSE,TokenTypes.EOF, TokenTypes.LINENUMBER]:
            right = ExpressionParser.parsePrimaryExpression(parser)
            parameters.append(right)
            
            # we skip ,
            parser.advance(TokenTypes.COMMA)

        # we skip )
        parser.expect(TokenTypes.ROUNDCLOSE)

        # we skip =
        parser.expect(TokenTypes.ASSIGNMENT)

        body = ExpressionParser.parseExpression(parser, BindingPower.DEFAULT)

        # Update Symboltable
        symbol = cbas.symbolTable.getSymbol(functionName.value)
        symbol.type = "function"
        symbol.parameters = len(parameters)

        result = FunctionDefinitionStatement(functionName,parameters,body)
        cbas.log("end:parseDEFExpression", "debug" )
        return result
    
    ##
    #
    #
    @staticmethod
    def parseFORStatement(parser):
        cbas.log("start:parseFORExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        
        # We skip for
        parser.expect(TokenTypes.FOR)

        runner = ExpressionParser.parsePrimaryExpression(parser)

        # We skip =
        parser.expect(TokenTypes.EQ)

        start = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)

        # We skip TO
        parser.expect(TokenTypes.TO)

        end = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)

        step = None
        if parser.currentTokenType in [TokenTypes.STEP]:
            # We skip step
            parser.advance()
            step = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)

        loopCode = []
        while parser.currentTokenType not in [TokenTypes.NEXT,TokenTypes.EOF, TokenTypes.LINENUMBER]:
            
            right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)
            loopCode.append(right)
            
            # We skip ":"
            parser.advance(TokenTypes.COLON)

        # 
        result = ForStatement(runner,start,end,step, loopCode)
        cbas.log("end:parseFORExpression", "debug" )
        return result

    ##
    #
    #
    @staticmethod
    def parseLabelStatement(parser):
        result = ExpressionParser.parsePrimaryExpression(parser)
        id = cbas.labelTable.addLabel(result.code)
        result.value = id
        return result
      
    ##
    #
    #
    @staticmethod
    def parseDIMStatement(parser):
        cbas.log("start:parseDIMExpression ... {} @ {}".format(parser.currentToken.code, parser.pos), "debug" )
        
        # We skip dim
        parser.expect(TokenTypes.DIM)

        variable = ExpressionParser.parsePrimaryExpression(parser)
        
        # We skip (
        parser.expect(TokenTypes.ROUNDOPEN)

        parameters = []
        while parser.currentTokenType not in [TokenTypes.LINEEND,TokenTypes.ROUNDCLOSE,TokenTypes.EOF, TokenTypes.LINENUMBER]:
            right = ExpressionParser.parseExpression(parser,BindingPower.DEFAULT)
            parameters.append(right)
            
            # we skip ,
            parser.advance(TokenTypes.COMMA)

        # We skip )
        parser.expect(TokenTypes.ROUNDCLOSE)

        assignment = None
        # There could be an assignment
        if parser.currentTokenType in [TokenTypes.ASSIGNMENT]:
            # We skip thee "="
            parser.advance(TokenTypes.ASSIGNMENT)
            assignment = ExpressionParser.parseExpression(parser, BindingPower.DEFAULT)

        result = DimStatement(variable,parameters, assignment)
        cbas.log("end:parseDIMExpression", "debug" )
        return result


##
#
#
class Statement(TreeNode):
    
    def __init__(self, value = None):
        super().__init__()
        self.value = value
        self._basicGenerated = False

    def toBasic(self):
        if self._basicGenerated:
            return None
        self._basicGenerated = True        
        return [self.value]

##
# {
#  statement0
#  statement1
#  ...
# }
#
class BlockStatement(Statement):

    def __init__(self, statements):
        super().__init__()
        self.statements = statements
        for s in self.statements:
            s.onReplace.add(self._hndReplaceLeft)

    def _hndReplaceLeft(self,ev):
        #print("BlockStatement::_hndReplaceLeft")
        for i,v in enumerate(self.statements):
            if ev.eventSource == v:
                self.statements[i].onReplace.remove(self._hndReplaceLeft)
                self.statements[i] = ev.replacement
                self.statements[i].onReplace.add(self._hndReplaceLeft)
                return


    def _getNodes(self):
        return self.statements

## expression 
# 4+6
# 4-6
# ...
class ExpressionStatement(Statement):

    def __init__(self, statement):
        super().__init__()
        self.statement = statement
        
        self.statement.onReplace.add(self._hndReplace)

    def _hndReplace(self,ev):
        #print("ExpressionStatement::_hndReplace")
        self.statement.onReplace.remove(self._hndReplace)
        self.statement = ev.replacement
        self.statement.onReplace.add(self._hndReplace)

    def _getNodes(self):
        return self.statement
    
##
#
#
class IfStatement(Statement):

    def __init__(self, condition, code):
        super().__init__()
        self.condition = condition
        self.trueCode = code
        
        self.condition.onReplace.add(self._hndReplaceCondition)
        self.trueCode.onReplace.add(self._hndReplaceCode)


    def _hndReplaceCondition(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.condition.onReplace.remove(self._hndReplaceCondition)
        self.condition = ev.replacement
        self.condition.onReplace.add(self._hndReplaceCondition)

    def _hndReplaceCode(self,ev):
        #print("BlockStatement::_hndReplaceLeft")
        for i,v in enumerate(self.trueCode):
            if ev.eventSource == v:
                self.trueCode[i].onReplace.remove(self._hndReplaceCode)
                self.trueCode[i] = ev.replacement
                self.trueCode[i].onReplace.add(self._hndReplaceCode)
                return
            
    def _getNodes(self):
        result = []
        result.append(self.condition)
        result.append(self.trueCode)
        return result
    

##
#
#
class InputStatement(Statement):

    def __init__(self, statement, parameters):
        super().__init__()
        self.statement = statement
        self.parameters = parameters

        self.statement.onReplace.add(self._hndReplaceFunction)

        for s in self.parameters:
            s.onReplace.add(self._hndReplaceParameter)

    def _hndReplaceFunction(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.statement.onReplace.remove(self._hndReplaceFunction)
        self.statement = ev.replacement
        self.statement.onReplace.add(self._hndReplaceFunction)

    def _hndReplaceParameter(self,ev):
        #print("BlockStatement::_hndReplaceLeft")
        for i,v in enumerate(self.parameters):
            if ev.eventSource == v:
                self.parameters[i].onReplace.remove(self._hndReplaceParameter)
                self.parameters[i] = ev.replacement
                self.parameters[i].onReplace.add(self._hndReplaceParameter)
                return
            
    def _getNodes(self):
        result = []
        result.append(self.statement) 
        for p in self.parameters:
            result.append(p)
        return result
    

##
#
#
class StatementStatement(Statement):

    def __init__(self, statement, parameters):
        super().__init__()
        self.statement = statement
        self.parameters = parameters

        self.statement.onReplace.add(self._hndReplaceFunction)

        for s in self.parameters:
            s.onReplace.add(self._hndReplaceParameter)

    def _hndReplaceFunction(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.statement.onReplace.remove(self._hndReplaceFunction)
        self.statement = ev.replacement
        self.statement.onReplace.add(self._hndReplaceFunction)

    def _hndReplaceParameter(self,ev):
        #print("BlockStatement::_hndReplaceLeft")
        for i,v in enumerate(self.parameters):
            if ev.eventSource == v:
                self.parameters[i].onReplace.remove(self._hndReplaceParameter)
                self.parameters[i] = ev.replacement
                self.parameters[i].onReplace.add(self._hndReplaceParameter)
                return
            
    def _getNodes(self):
        result = []
        result.append(self.statement) 
        for p in self.parameters:
            result.append(p)
        return result
    

##
#
#
class PrintStatement(Statement):

    def __init__(self, statement, parameters):
        super().__init__()
        self.statement = statement
        self.parameters = parameters

        self.statement.onReplace.add(self._hndReplaceFunction)

        for s in self.parameters:
            s.onReplace.add(self._hndReplaceParameter)

    def _hndReplaceFunction(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.statement.onReplace.remove(self._hndReplaceFunction)
        self.statement = ev.replacement
        self.statement.onReplace.add(self._hndReplaceFunction)

    def _hndReplaceParameter(self,ev):
        #print("BlockStatement::_hndReplaceLeft")
        for i,v in enumerate(self.parameters):
            if ev.eventSource == v:
                self.parameters[i].onReplace.remove(self._hndReplaceParameter)
                self.parameters[i] = ev.replacement
                self.parameters[i].onReplace.add(self._hndReplaceParameter)
                return
            
    def _getNodes(self):
        result = []
        result.append(self.statement) 
        for p in self.parameters:
            result.append(p)
        return result
   
##
#
#
class FunctionDefinitionStatement(Statement):

    def __init__(self, functionName, parameters, body):
        super().__init__()
        self.functionName = functionName
        self.parameters = parameters
        self.body = body

        self.functionName.onReplace.add(self._hndReplaceFunction)
        self.body.onReplace.add(self._hndReplaceBody)

        for s in self.parameters:
            s.onReplace.add(self._hndReplaceParameter)

    def _hndReplaceFunction(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.functionName.onReplace.remove(self._hndReplaceFunction)
        self.functionName = ev.replacement
        self.functionName.onReplace.add(self._hndReplaceFunction)

    def _hndReplaceBody(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.body.onReplace.remove(self._hndReplaceBody)
        self.body = ev.replacement
        self.body.onReplace.add(self._hndReplaceBody)

    def _hndReplaceParameter(self,ev):
        #print("BlockStatement::_hndReplaceLeft")
        for i,v in enumerate(self.parameters):
            if ev.eventSource == v:
                self.parameters[i].onReplace.remove(self._hndReplaceParameter)
                self.parameters[i] = ev.replacement
                self.parameters[i].onReplace.add(self._hndReplaceParameter)
                return
            
    def _getNodes(self):
        result = []
        result.append(self.functionName) 
        for p in self.parameters:
            result.append(p)
        result.append(self.body)
        return result
    

##
#
#
class ForStatement(Statement):

    def __init__(self, runner, start, end, step=None, loopCode=None):
        super().__init__()
        
        self.runner = runner
        self.start = start
        self.end = end
        self.step = step
        self.loopCode = loopCode
        
        self.runner.onReplace.add(self._hndReplaceRunner)
        self.start.onReplace.add(self._hndReplaceStart)
        self.end.onReplace.add(self._hndReplaceEnd)
        if self.step is not None:
            self.step.onReplace.add(self._hndReplaceStep)

        if self.loopCode is not None:
            for s in self.loopCode:
                s.onReplace.add(self._hndReplaceLoopCode)            

    def _hndReplaceRunner(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.runner.onReplace.remove(self._hndReplaceRunner)
        self.runner = ev.replacement
        self.runner.onReplace.add(self._hndReplaceRunner)

    def _hndReplaceStart(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.start.onReplace.remove(self._hndReplaceStart)
        self.start = ev.replacement
        self.start.onReplace.add(self._hndReplaceStart)

    def _hndReplaceEnd(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.end.onReplace.remove(self._hndReplaceEnd)
        self.end = ev.replacement
        self.end.onReplace.add(self._hndReplaceEnd)

    def _hndReplaceStep(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.step.onReplace.remove(self._hndReplaceStep)
        self.step = ev.replacement
        self.step.onReplace.add(self._hndReplaceStep)

    def _hndReplaceLoopCode(self,ev):
        #print("BlockStatement::_hndReplaceLeft")
        for i,v in enumerate(self.loopCode):
            if ev.eventSource == v:
                self.loopCode[i].onReplace.remove(self._hndReplaceLoopCode)
                self.loopCode[i] = ev.replacement
                self.loopCode[i].onReplace.add(self._hndReplaceLoopCode)
                return
            
    def _getNodes(self):

        result = []
        result.append(self.runner)
        result.append(self.start)
        result.append(self.end)
        if self.step is not None:
            result.append(self.step)
        if self.loopCode is not None:
            for p in self.loopCode:
                result.append(p)            
        return result
    
##
#
#
class DimStatement(Statement):

    def __init__(self, variable, dimensions, assignment=None):
        super().__init__()
        self.variable = variable
        self.dimensions = dimensions
        self.assignment = None
        
        self.variable.onReplace.add(self._hndReplaceVariable)

        if assignment is not None:
            self.assignment = assignment
            self.assignment.onReplace.add(self._hndReplaceAssignment)


        for s in self.dimensions:
            s.onReplace.add(self._hndReplaceDimension)

    def _hndReplaceVariable(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.variable.onReplace.remove(self._hndReplaceVariable)
        self.variable = ev.replacement
        self.variable.onReplace.add(self._hndReplaceVariable)

    def _hndReplaceAssignment(self,ev):
        #print("GroupingExpression::_hndReplaceFunction")
        self.assignment.onReplace.remove(self._hndReplaceAssignment)
        self.assignment = ev.replacement
        self.assignment.onReplace.add(self._hndReplaceAssignment)

    def _hndReplaceDimension(self,ev):
        #print("BlockStatement::_hndReplaceLeft")
        for i,v in enumerate(self.dimensions):
            if ev.eventSource == v:
                self.dimensions[i].onReplace.remove(self._hndReplaceDimension)
                self.dimensions[i] = ev.replacement
                self.dimensions[i].onReplace.add(self._hndReplaceDimension)
                return
            
    def _getNodes(self):
        result = []
        result.append(self.variable)
        for p in self.dimensions:
            result.append(p)
        if self.assignment is not None:
            result.append(self.assignment)
        return result
    
