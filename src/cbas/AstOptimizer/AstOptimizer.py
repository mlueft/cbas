import cbas
import cbas.Ast.Expressions
import cbas.DataStructures.TraverseMode
import cbas.Lexer.TokenTypes
from cbas.Exceptions.Exceptions import SemanticErrorException

TraverseMode = cbas.DataStructures.TraverseMode.TraverseMode
BinaryExpression = cbas.Ast.Expressions.BinaryExpression
PrimaryExpression = cbas.Ast.Expressions.PrimaryExpression
GroupingExpression = cbas.Ast.Expressions.GroupingExpression
PrefixExpression = cbas.Ast.Expressions.PrefixExpression
TokenTypes = cbas.Lexer.TokenTypes.TokenTypes


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
                if expr.tag in ["int","float"]:
                    left = float(expr.value)
                    if expr.tag == "int":
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

        if node.left.tag not in [ "int", "float"]:
            return node
        
        if node.right.tag not in [ "int", "float"]:
            return node
        
        if node.operator.value not in [ "+","-","*","/"]:
            return node


        lv = float(node.left.value)
        rv = float(node.right.value)
        op = node.operator.value

        if   op == "+": r = lv+rv
        elif op == "-": r = lv-rv
        elif op == "*": r = lv*rv
        elif op == "/": r = lv/rv
        else:return node

        replacement = PrimaryExpression("float",r)

        #if node.right.tag == "int" or node.left.tag == "int":
        #    replacement.tag   = "int"
        #    replacement.value = int(replacement.value)

        #print( "{}{}{} => {}".format(lv,op,rv,r) )
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

        if node.left.tag not in [ "int", "float", "boolean"]:
            return node
        
        if node.right.tag not in [ "int", "float", "boolean"]:
            return node
        
        if node.operator.value not in [ "=","<",">","<=",">=","<>" ]:
            return node

        if node.left.tag == "boolean":
            lv = node.left.value
        else:
            lv = float(node.left.value)

        if node.right.tag == "boolean":
            rv = node.right.value
        else:
            rv = float(node.right.value)

        op = node.operator.value

        if   op == "=": r = lv==rv
        elif op == "<": r = lv<rv
        elif op == ">": r = lv>rv
        elif op == "<=": r = lv<=rv
        elif op == ">=": r = lv>=rv
        elif op == "<>": r = lv!=rv
        else:return node

        replacement = PrimaryExpression("boolean",r)

        #print( "{}{}{} => {}".format(lv,op,rv,r) )
        return replacement


class StringOptimizer(AstOptimizer):

    def __init__(self):
        super().__init__()

    def main(self, node, direction):
        pass


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
        
        if type(node) == cbas.Ast.Expressions.StatementExpression:
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