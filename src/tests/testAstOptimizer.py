import unittest

import cbas.AstOptimizer.AstOptimizer
import cbas.Config.Config
import cbas.Lexer.Tokens


AstOptimizer = cbas.AstOptimizer.AstOptimizer.AstOptimizer
Config = cbas.Config.Config.Config


class AstOptimizerTestCase(unittest.TestCase):

    def setUp(self):
        super().setUp()
 
    def tearDown(self):
        super().tearDown()

    def testChildren0(self):
        
        testStr = """4"""

        config = Config(0)
        c = config.getParserConfig()

        subject = AstOptimizer()
        subject.config = c


        """test Widget.children"""
        assert True, "firstToken is not of type ChainToken!"
        
