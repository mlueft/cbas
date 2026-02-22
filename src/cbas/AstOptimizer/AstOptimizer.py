import cbas.Ast.Expressions
import cbas.DataStructures.TraverseMode

TraverseMode = cbas.DataStructures.TraverseMode.TraverseMode
BinaryExpression = cbas.Ast.Expressions.BinaryExpression
PrimaryExpression = cbas.Ast.Expressions.PrimaryExpression
GroupingExpression = cbas.Ast.Expressions.GroupingExpression
PrefixExpression = cbas.Ast.Expressions.PrefixExpression

class ArithmeticOptimizer():

    @staticmethod
    def main(node, direction):
        
        #print( "{}".format(type(node))  )
        replacement = node
        replacement = ArithmeticOptimizer._resolveGrouping(replacement, direction)
        replacement = ArithmeticOptimizer._resolvePrefix(replacement, direction)
        replacement = ArithmeticOptimizer._resolveArithmetic(replacement, direction)
        node.replace(replacement)

    #
    # Prefix resolver
    #
    def _resolvePrefix(node, direction):

        if type(node) is not PrefixExpression:
            return node

        if direction == TraverseMode.TOP_DOWN:
            return ArithmeticOptimizer._resolvePrefixTopDown(node)
        if direction == TraverseMode.BOTTOM_UP:
            return ArithmeticOptimizer._resolvePrefixBottomUp(node)
        return node
    
    def _resolvePrefixBottomUp(node):
        
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
    
    def _resolvePrefixTopDown(node):

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
    def _resolveGrouping(node, direction):

        if direction != TraverseMode.BOTTOM_UP:
            return node
        
        if type(node) is not  GroupingExpression:
            return node
        
        return node.value

    #
    # Arithmetic resolver
    #
    def _resolveArithmetic(node, direction):
        #return node
    
        if direction != TraverseMode.BOTTOM_UP:
            return node

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


class LogicOptimizer():

    @staticmethod
    def main(node,direction):
        #print( "{}".format(type(node))  )
        replacement = node
        replacement = LogicOptimizer._resolveComparor(replacement, direction)
        node.replace(replacement)
    
    @staticmethod
    def _resolveComparor(node,direction):
        
        if direction != TraverseMode.BOTTOM_UP:
            return node

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
    
class StringOptimizer():

    @staticmethod
    def main(node):
        pass
