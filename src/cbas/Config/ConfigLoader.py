import json
from operator import attrgetter

import cbas.Ast.Expressions as Expression
import cbas.Lexer.TokenTypes as TokenTypes
import cbas.Lexer.ConfigToken as LConfigToken
import cbas.Parser.ConfigToken as PConfigToken
import cbas.Config.LexerConfig as LexerConfig
import cbas.Config.ParserConfig as ParserConfig

class ConfigLoader():
    
    def __init__(self, fileName):
        self.__configFile = fileName
        self.__json = None
  
    def loadConfig( self ):
        if self.__json != None:
            return
        
        if self.__configFile != None:
            with open(self.__configFile, 'r') as file:
                self.__json = json.load(file) 
    
    ##
     #
     #
    def getLexerConfig(self, name, recursion = 0):
        result = LexerConfig.LexerConfig()
        #result = []
    
        self.loadConfig()
      
        configFound = False
        for c in self.__json["lexer"]:
            config = c["config"]

            if config["name"] == name:

                result.name = config["name"]

                if "markLinestart" in config:
                    result.markLinestart = config["markLinestart"]

                if "markLineend" in config:
                    result.markLineend = config["markLineend"]
                
                configFound = True
                if config["extends"] != None:
                    _base = self.getLexerConfig(config["extends"], recursion+1)
     
                    for t in _base.tokens:
                        result.tokens.append(t)
      
                for t in c["tokens"]:
                    result.tokens.append(
                        LConfigToken(
                            TokenTypes.getType(t["type"]),
                            t["expression"],
                            t["order"],
                            t["name"],
                            t["description"]
                        )
                    )

        if not configFound:
            raise ValueError("Config '{}' for lexer not found!".format(name) )

        result.tokens = sorted(result.tokens, key=attrgetter('order'))

        return result

    ##
    #
    #
    def getParserConfig(self, name, recursion = 0):
        result = ParserConfig.ParserConfig()
        
        self.loadConfig()
        
        for c in self.__json["parser"]:
            config = c["config"]

            if config["name"] == name:
                
                result.name = config["name"]

                configFound = True
                if config["extends"] != None:
                    _base = self.getParserConfig(config["extends"], recursion+1)
     
                    for t in _base.tokens:
                        result.tokens.append(t)

                for t in c["lookups"]:
                    result.tokens.append(PConfigToken.ConfigToken(
                        t["bindingpower"],
                        TokenTypes.getType(t["type"]),
                        t["category"],
                    ) )

        if not configFound:
            raise ValueError("Config '{}' for parser not found!".format(name) )
        
        result.tokens = sorted(result.tokens, key=attrgetter('bindingpower'))

        return result

    ##
    #
    #
    def bla(self):
        pass