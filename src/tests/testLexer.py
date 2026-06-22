import unittest

import cbas.Lexer.Lexer
import cbas.Config.Config
import cbas.Lexer.Tokens

Lexer = cbas.Lexer.Lexer.Lexer
TokenTypes = cbas.Lexer.TokenTypes
Config = cbas.Config.Config.Config
ChainToken = cbas.Lexer.Tokens.ChainToken

class LexerTestCase(unittest.TestCase):

    def setUp(self):
        super().setUp()
 
    def tearDown(self):
        super().tearDown()

    def testChildren0(self):
        
        testStr = """4"""

        config = Config(0)
        c = config.getLexerConfig()

        subject = Lexer()
        subject.config = c

        subject.tokenizeLine( testStr )

        firstToken = subject.firstToken

        print(firstToken)

        """test Widget.children"""
        assert type(firstToken) == ChainToken, "firstToken is not of type ChainToken!"
        
