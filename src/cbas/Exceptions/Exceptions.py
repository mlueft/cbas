
class SyntaxErrorException(BaseException):

    def __init__(self, message):
        pass

class SemanticErrorException(BaseException):

    def __init__(self, message):
        self.message = message