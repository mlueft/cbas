
class SyntaxErrorException(BaseException):

    def __init__(self, codeLine="", lineNumber=None, pos=None):
        self.codeLine = codeLine
        self.lineNumber = lineNumber
        self.pos = pos

    def __str__(self):
        msg = "Syntax error at line {}...\n".format(self.lineNumber)
        msg += "{}\n".format(self.codeLine)
        msg += "{}\n".format("."+self.pos)

class SemanticErrorException(BaseException):

    def __init__(self, message):
        self.message = message