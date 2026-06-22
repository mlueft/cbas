import cbas
import cbas.Ast.Expressions
import cbas.DataStructures.TraverseMode
import cbas.Lexer.TokenTypes
import cbas.Lexer.Tokens
import cbas.Compiler.SymbolTable

from cbas.Exceptions.Exceptions import SemanticErrorException

TraverseMode = cbas.DataStructures.TraverseMode.TraverseMode
BinaryExpression = cbas.Ast.Expressions.BinaryExpression
PrimaryExpression = cbas.Ast.Expressions.PrimaryExpression
GroupingExpression = cbas.Ast.Expressions.GroupingExpression
PrefixExpression = cbas.Ast.Expressions.PrefixExpression
TokenTypes = cbas.Lexer.TokenTypes.TokenTypes
ChainToken = cbas.Lexer.Tokens.ChainToken
SymbolKind = cbas.Compiler.SymbolTable.SymbolKind

class AstOptimizer():
    
    def __init__(self):
        pass

    def main(self, node, direction):
        pass


class ArithmeticOptimizer(AstOptimizer):

    def __init__(self):
        super().__init__()

    def main(self, node, direction):
        
        #print( "{}".format(type(node))  )
        replacement = node
        replacement = self._resolveGrouping(replacement, direction)
        replacement = self._resolvePrefix(replacement, direction)
        replacement = self._resolveArithmetic(replacement, direction)
        node.replace(replacement)

    #
    # Prefix resolver
    #
    def _resolvePrefix(self, node, direction):

        if type(node) is not PrefixExpression:
            return node

        if direction == TraverseMode.TOP_DOWN:
            return self._resolvePrefixTopDown(node)
        if direction == TraverseMode.BOTTOM_UP:
            return self._resolvePrefixBottomUp(node)
        return node
    
    def _resolvePrefixBottomUp(self, node):
        
        op = node.operator.value
        expr = node.right

        if op  == '-':

            if type(expr) is PrimaryExpression:
                # if expr is a primary
                # prefix gets applies to its value.
                if expr.tag in ["integer","float"]:
                    left = float(expr.value)
                    if expr.tag == "integer":
                        left = int(expr.value)
                    left = -left
                    expr.value = left
                    return expr
    
        return node
    
    def _resolvePrefixTopDown(self, node):

        if node.operator.value not in  ['-']:
            return node

        op = node.operator.value
        expr = node.right

        if op  == '-':
            if type(expr) is BinaryExpression:

                if type(expr.left) in [BinaryExpression,PrimaryExpression]:
                    # if left is a BinrayExpression
                    # prefix gets a prefix of this BinaryExpression
                    expr.left.replace( PrefixExpression(PrimaryExpression("op",op),expr.left) )
                    return expr
                
                elif type(expr.left) is GroupingExpression:
                    # if left is a grouping
                    # the prefixs gets to the expression in the grouping
                    expr.left.replace( PrefixExpression(PrimaryExpression("op",op),expr.left.value) )
                    return expr
        return node
        
    #
    # Grouping resolver
    #
    def _resolveGrouping(self, node, direction):

        if direction != TraverseMode.BOTTOM_UP:
            return node
        
        if type(node) is not  GroupingExpression:
            return node
        
        return node.value

    #
    # Arithmetic resolver
    #
    def _resolveArithmetic(self, node, direction):

        if type(node) is not BinaryExpression:
            return node
        
        if type(node.left) is not PrimaryExpression:
            return node
        
        if type(node.operator) is not PrimaryExpression:
            return node
        
        if type(node.right) is not PrimaryExpression:
            return node

        if node.left.tag not in [ "integer", "float"]:
            return node
        
        if node.right.tag not in [ "integer", "float"]:
            return node
        
        if node.operator.value not in [ "+","-","*","/"]:
            return node

        symbolLeft = cbas.symbolTable.getSymbol(node.left.value)
        symbolRight = cbas.symbolTable.getSymbol(node.right.value)

        lv = float(symbolLeft.code)
        rv = float(symbolRight.code)
        op = node.operator.value

        if   op == "+": newLiteral = lv+rv
        elif op == "-": newLiteral = lv-rv
        elif op == "*": newLiteral = lv*rv
        elif op == "/": newLiteral = lv/rv

        #
        # New type is float if one of the operants is float
        #
        newType = "integer"
        if node.left.tag == "float" or node.right.tag == "float":
            newType = "float"

        #
        # We store the result in the symbol table
        #
        symbolId = cbas.symbolTable.addSymbol(newType,newLiteral,None,None,SymbolKind.LITERAL)

        if newType == "float":
            replacement = PrimaryExpression(newType,symbolId, ChainToken(symbolId,None,None,TokenTypes.FLOAT ) )
        else:
            replacement = PrimaryExpression(newType,symbolId, ChainToken(symbolId,None,None,TokenTypes.INTEGER ) )

        return replacement

class StringOptimizer(AstOptimizer):

    def __init__(self):
        super().__init__()

    def main(self, node, direction):

        replacement = node
        replacement = self._resolveStringArithmetic(replacement)
        node.replace(replacement)
        
    def _resolveStringArithmetic(self, node):

        if type(node) is not BinaryExpression:
            return node

        if type(node.left) is not PrimaryExpression:
            return node
        
        if type(node.operator) is not PrimaryExpression:
            return node
        
        if type(node.right) is not PrimaryExpression:
            return node
        
        if node.left.tag not in [ "integer", "string"]:
            return node
        
        if node.right.tag not in [ "integer", "string"]:
            return node
        
        if node.operator.value not in [ "*", "+" ]:
            return node
                
        symbolLeft = cbas.symbolTable.getSymbol(node.left.value)
        symbolRight = cbas.symbolTable.getSymbol(node.right.value)

        if symbolLeft.type == "integer":
            lv = int(symbolLeft.code)
        else:
            lv = symbolLeft.code[1:-1]

        if symbolRight.type == "integer":
            rv = int(symbolRight.code)
        else:
            # literals are stored in symbol table
            rv = symbolRight.code[1:-1]

        op = node.operator.value

        if   op == "*":
            newLiteral = lv*rv
        elif op == "+": 
            newLiteral = str(lv) + str(rv)

        #
        # We store the result in the symbol table
        #
        symbolId = cbas.symbolTable.addSymbol("string",'"{}"'.format(newLiteral),None,None,SymbolKind.LITERAL)

    
        replacement = PrimaryExpression("string",symbolId,ChainToken(str(newLiteral),None,None,TokenTypes.STRING ))

        #print( "{}{}{} => {}".format(lv,op,rv,r) )
        return replacement
        return replacement

class LogicOptimizer(AstOptimizer):

    def __init__(self):
        super().__init__()

    def main(self, node,direction):
        #print( "{}".format(type(node))  )
        replacement = node
        replacement = self._resolveComparor(replacement, direction)
        node.replace(replacement)
    
    def _resolveComparor(self, node,direction):
        
        if type(node) is not BinaryExpression:
            return node
        
        if type(node.left) is not PrimaryExpression:
            return node
        
        if type(node.operator) is not PrimaryExpression:
            return node
        
        if type(node.right) is not PrimaryExpression:
            return node

        if node.left.tag not in [ "integer", "float", "boolean"]:
            return node
        
        if node.right.tag not in [ "integer", "float", "boolean"]:
            return node
        
        if node.operator.value not in [ "=","<",">","<=",">=","<>" ]:
            return node

        symbolLeft = cbas.symbolTable.getSymbol(node.left.value)
        symbolRight = cbas.symbolTable.getSymbol(node.right.value)

        if symbolLeft.type == "boolean":
            lv = symbolLeft.code
        else:
            lv = float(symbolLeft.code)

        if symbolRight.type == "boolean":
            rv = symbolRight.code
        else:
            rv = float(symbolRight.code)

        op = node.operator.value

        if   op == "=": newLiteral = lv==rv
        elif op == "<": newLiteral = lv<rv
        elif op == ">": newLiteral = lv>rv
        elif op == "<=": newLiteral = lv<=rv
        elif op == ">=": newLiteral = lv>=rv
        elif op == "<>": newLiteral = lv!=rv
        
        if newLiteral:
            newLiteral = "{true}"
        else:
            newLiteral = "{false}"

        #
        # We store the result in the symbol table
        #
        symbolId = cbas.symbolTable.addSymbol("boolean",newLiteral,None,None,SymbolKind.LITERAL)

        replacement = PrimaryExpression("boolean",symbolId, ChainToken(symbolId,None,None,TokenTypes.BOOLEAN ) )

        return replacement

class SyntaxCheckerV2(AstOptimizer):

    def __init__(self):
        super().__init__()

    def __expectParameterCounf(self, node, min=0, max=100):
            token = node.statement.token
            qty = len(node.parameters)
            if qty < min :
                message = "Too little parameters for {} in line @ {}:{}.".format(TokenTypes.toString(token.type).upper(),token.line,token.pos)
                raise SemanticErrorException(message)
            elif qty > max :
                message = "Too much parameters for {} in line @ {}:{}.".format(TokenTypes.toString(token.type).upper(),token.line,token.pos)
                raise SemanticErrorException(message)
                        
    def __checkStsParameterQantity(self,node):
        
        if type(node) == cbas.Ast.Statements.StatementStatement:
            token = node.statement.token
            qty = len(node.parameters)
            if token.type in[ TokenTypes.CLR, TokenTypes.NEW, TokenTypes.RESTORE, TokenTypes.RETURN, TokenTypes.ST, TokenTypes.STATUS, TokenTypes.STOP, TokenTypes.TI, TokenTypes.TI_DOLLAR, TokenTypes.TIME, TokenTypes.TIME_DOLLAR, TokenTypes.PISIGN, TokenTypes.END, TokenTypes.CONT ]:
                self.__expectParameterCounf( node,0,0 )
           
            elif token.type in[ TokenTypes.RUN ]:
                self.__expectParameterCounf( node,0,1 )
            
            elif token.type in[ TokenTypes.GOTO, TokenTypes.GOSUB, TokenTypes.CLOSE ]:
                self.__expectParameterCounf( node,1,1 )
            
            elif token.type in[ TokenTypes.POKE ]:
                self.__expectParameterCounf( node,2,2 )
                
            elif token.type == TokenTypes.WAIT:
                self.__expectParameterCounf( node,2,3 )

            elif token.type == TokenTypes.VERIFY:
                self.__expectParameterCounf( node,0,2 )

            elif token.type in [TokenTypes.SAVE, TokenTypes.LOAD]:
                self.__expectParameterCounf( node,0,3 )

            elif token.type == TokenTypes.OPEN:
                self.__expectParameterCounf( node,1,4 )

            elif token.type == TokenTypes.LIST:
                self.__expectParameterCounf( node,0,1 )

            elif token.type == TokenTypes.GET:
                self.__expectParameterCounf( node,1,100 )

            elif token.type == TokenTypes.GET_SHARP:
                self.__expectParameterCounf( node,2,100 )
            
            elif token.type == TokenTypes.INPUT:
                self.__expectParameterCounf( node,1,100 )

        elif type(node) == cbas.Ast.Expressions.FunctionCallExpression:
            if len(node.parameters) != 1:
                message = "Too much parameters for {} in line @ {}:{}.".format(TokenTypes.toString(token.type).upper(),token.line,token.pos)
                raise SemanticErrorException(message)
            

    def main(self, node, direction):
        self.__checkStsParameterQantity(node)