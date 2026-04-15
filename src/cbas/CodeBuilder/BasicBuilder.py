import re

import cbas
import cbas.DataStructures.TraverseMode
import cbas.Ast.Expressions
import cbas.Ast.Statements
import cbas.Lexer.TokenTypes

TraverseMode = cbas.DataStructures.TraverseMode.TraverseMode
TokenTypes = cbas.Lexer.TokenTypes.TokenTypes

BlockStatement = cbas.Ast.Statements.BlockStatement
ExpressionStatement = cbas.Ast.Statements.ExpressionStatement
InputExpression = cbas.Ast.Expressions.InputExpression
PrintExpression = cbas.Ast.Expressions.PrintExpression
ForExpression = cbas.Ast.Expressions.ForExpression
IfExpression = cbas.Ast.Expressions.IfExpression
DimExpression = cbas.Ast.Expressions.DimExpression
OnExpression = cbas.Ast.Expressions.OnExpression
FunctionDefinitionExpression = cbas.Ast.Expressions.FunctionDefinitionExpression
FunctionCallExpression = cbas.Ast.Expressions.FunctionCallExpression
StatementExpression = cbas.Ast.Expressions.StatementExpression
CallExpression = cbas.Ast.Expressions.CallExpression
AssignmentExpression = cbas.Ast.Expressions.AssignmentExpression
GroupingExpression = cbas.Ast.Expressions.GroupingExpression
PrefixExpression = cbas.Ast.Expressions.PrefixExpression
BinaryExpression = cbas.Ast.Expressions.BinaryExpression
PrimaryExpression = cbas.Ast.Expressions.PrimaryExpression

class BasicBuilder():

    def __init__(self):
        #self.configIndex = configIndex
        self.basicLines = []


    def resolveSymbols(self,line):
        pattern = re.compile("#[0-9][0-9][0-9]")
        matches = pattern.findall(line)
        for match in matches:
            symbolName = match
            variableName = cbas.symbolTable.getVariable(symbolName)
            line = line.replace( symbolName,"{}".format(variableName,symbolName) )
        return line

    def getHandler(self,node):
        _type = type(node)

        if _type == BlockStatement:return self.renderBlockStatement
        if _type == ExpressionStatement:return self.renderExpressionStatement
        if _type == InputExpression:return self.renderInputExpression
        if _type == PrintExpression:return self.renderPrintExpression
        if _type == ForExpression:return self.renderForExpression
        if _type == IfExpression:return self.renderIfExpression
        if _type == DimExpression:return self.renderDimExpression
        if _type == OnExpression:return self.renderOnExpression
        if _type == FunctionDefinitionExpression:return self.renderFunctionDefinitionExpression
        if _type == FunctionCallExpression:return self.renderFunctionCallExpression
        if _type == StatementExpression:return self.renderStatementExpression
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
                l = self.resolveSymbols(l)
                self.basicLines.append(l)


    def main(self, ast):
        self.basicLines = []
        ast.topDown(self.astHandler)
        return self.basicLines



    def renderBlockStatement(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True

        result = []

        for s in node.statements:
            handler = self.getHandler(s)
            b = handler(s)
            if b is not None:
                for b1 in b:
                    result.append(b1)

        return result
    
    def renderExpressionStatement(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True
        handler = node.getHandler(node.statement)
        return [handler(node.statement)]

    # InputExpression
    def renderInputExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True
        
        line = ""

        result = []

        # CMD
        handler = self.getHandler(node.statement)
        b = handler(node.statement)
        line += b[0]
        line += " "

        for p in node.parameters:
            handler = self.getHandler(p)
            b = handler(p)
            line += b[0]
            if p != node.parameters[-1]:
                line += " "

        line += " "

        result.append(line)
        
        return result
        
    # PrintExpression
    def renderPrintExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True
        line = ""

        result = []

        # CMD
        handler = self.getHandler(node.statement)
        b = handler(node.statement)
        line += b[0]
        line += " "

        for p in node.parameters:
            handler = self.getHandler(p)
            b = handler(p)
            line += b[0]
            if p != node.parameters[-1]:
                line += " "

        line += " "

        result.append(line)

        return result

    # ForExpression
    def renderForExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True

        result = []
        
        line = "for "
        handler = self.getHandler(node.runner)
        b = handler(node.runner)
        line += b[0]
        line += "="
        handler = self.getHandler(node.start)
        b = handler(node.start)
        line += b[0]
        line += "to"
        handler = self.getHandler(node.end)
        b = handler(node.end)
        line += b[0]

        if node.step is not None:
            line += "step"
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

    # IfExpression
    def renderIfExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True

        result =  []

        line = "if "
        handler = self.getHandler(node.condition)
        right = handler(node.condition)
        line += right[0]
        
        line += " then "

        if len(node.trueCode)>0:
            t = type(node.trueCode[0])
            if t == cbas.Ast.Expressions.StatementExpression:
                if node.trueCode[0].statement.type == TokenTypes.GOTO:
                    line += " "
        
        #result.append(line)

        for p in node.trueCode:
            handler=self.getHandler(p)
            b = handler(p)
            line += b[0]
            #result.append(line)
            if p != node.trueCode[-1]:
                line += ","
        
        result.append(line)

        return result
        
    # DimExpression
    def renderDimExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True
        result = "dim "

        b = node.variable.toBasic()
        result += b[0]
        result += "("
        for p in node.dimensions:
            b = p.toBasic()
            result += b[0]
            if p != node.dimensions[-1]:
                result += ","
        result += ")"
        return [result]
    
    # OnExpression
    def renderOnExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True
        result = "on "

        handler = self.getHandler(node.index)
        b = handler(node.index)
        result += b[0]
        result += " "
        handler = self.getHandler(node.jumpMethode)
        b = handler(node.jumpMethode)
        result += b[0]
        result += " "
        for p in node.lineNumbers:
            handler = self.getHandler(p)
            b = handler(p)
            result += b[0]
            if p != node.lineNumbers[-1]:
                result += ","
        

        return [result]

    # FunctionDefinitionExpression
    def renderFunctionDefinitionExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True
        result = "def fn "

        handler = self.getHandler(node.functionName)
        b = handler(node.functionName)
        result += b[0]
        result += "("
        for p in node.parameters:
            handler = self.getHandler(p)
            b = handler(p)
            result += b[0]
            if p != node.parameters[-1]:
                result += ","
        result += ")="

        handler= self.getHandler(node.body)
        b = handler(node.body)
        result += b[0]

        return [result]

    # FunctionCallExpression
    def renderFunctionCallExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True
        result = "fn "

        handler = self.getHandler(node.functionName)
        b = handler(node.functionName)
        result += b[0]
        result += "("
        for p in node.parameters:
            handler = self.getHandler(p)
            b = handler(p)
            result += b[0]
            if p != node.parameters[-1]:
                result += ","
        result += ")"
        return [result]
    
    # StatementExpression
    def renderStatementExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True
        result = ""

        seperator = ","
        if node.statement.type == TokenTypes.LIST:
            seperator = "-"

        handler = self.getHandler(node.statement)
        b = handler(node.statement)
        result += b[0]
        result += " "
        for p in node.parameters:
            handler = self.getHandler(p)
            b = handler(p)
            result += b[0]
            if p != node.parameters[-1]:
                result += seperator
        result += " "
        return [result]

    # CallExpression
    def renderCallExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True
        result = ""

        handler = self.getHandler(node.function)
        f = handler(node.function)
        result += f[0]
        result += "("
        for p in node.parameters:
            handler = self.getHandler(p)
            b = handler(p)
            result += b[0]
            if p != node.parameters[-1]:
                result += ","
        result += ")"
        return [result]

    # AssignmentExpression
    def renderAssignmentExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True
        handler = self.getHandler(node.left)
        left = handler(node.left)
        if left is None:
            left = ""

        handler = self.getHandler(node.right)
        right = handler(node.right)
        return [left[0] +"="+ right[0]]
    
    # GroupingExpression
    def renderGroupingExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True
        handler = self.getHandler(node.value)
        return ["{"]+ handler(node.value) +["}"]
    
    # PrefixExpression
    def renderPrefixExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True
        handler = self.getHandler(node.operator)
        op = handler(node.operator)
        handler = self.getHandler(node.right)
        right = handler(node.right)
        return [op[0] + right[0]]
        
    # BinaryExpression
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
        return [bl[0] +" "+ bo[0] +" "+ br[0]]
        
    # PrimaryExpression
    def renderPrimaryExpression(self,node):
        if node._basicGenerated:
            return None
        node._basicGenerated = True
        
        if node.type == TokenTypes.LINEEND or node.type == TokenTypes.COLON:
            return None
        elif node.tag == "boolean":
            if node.value:
                return ["0"]
            return ["-1"]
        elif node.tag == "None":
            return ['']
        return [str(node.value)]
        