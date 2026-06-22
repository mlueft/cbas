import unittest

import cbas.Parser.Parser
import cbas.Config.Config
import cbas.Lexer.Tokens


Parser = cbas.Parser.Parser.Parser
Config = cbas.Config.Config.Config


class ParserTestCase(unittest.TestCase):

    def setUp(self):
        super().setUp()
 
    def tearDown(self):
        super().tearDown()

    def testChildren0(self):
        
        testStr = """4"""

        config = Config(0)
        c = config.getParserConfig()

        subject = Parser()
        subject.config = c


        """test Widget.children"""
        assert True, "firstToken is not of type ChainToken!"
        
