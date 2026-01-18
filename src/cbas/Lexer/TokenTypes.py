
class TokenTypes():
	NUMBER      =  0
	LINENUMBER  =  1
	STRING      =  2
	STATEMENT   =  3
	FUNCTION    =  4

	ADD         = 10
	MINUS       = 11
	MUL         = 12
	DIV         = 13
	EXPONENTIAL = 14

	EQ          = 20
	NEQ         = 21
	LE          = 22
	GE          = 23
	LESS        = 24
	MORE        = 25

	AND         = 30
	OR          = 31
	NOT         = 32

	CURLYOPEN   = 40
	CURLYCLOSE  = 41
	ROUNDOPEN   = 42
	ROUNDCLOSE  = 43
	
	SEMICOLON   = 50
	COLON       = 51
	
	COMMA       = 60
	COMMENT     = 61
	IGNORE      = 62
	LINESTART   = 63
	LINEEND     = 64
	IDENTIFIER  = 65
	WHITESPACE  = 66
	EOF         = 67

	__matchTable = {
		"number":      NUMBER,
		"linenumber":  LINENUMBER,
		"string":      STRING,
		"statement":   STATEMENT,
		"function":    FUNCTION,
		"add":         ADD,
		"minus":       MINUS,
		"mul":         MUL,
		"div":         DIV,
		"exponential": EXPONENTIAL,
		"le":          LE,
		"ge":          GE,
		"less":        LESS,
		"more":        MORE,
		"neq":         NEQ,
		"curlyopen":   CURLYOPEN,
		"curlyclose":  CURLYCLOSE,
		"roundopen":   ROUNDOPEN,
		"roundclose":  ROUNDCLOSE,
		"semicolon":   SEMICOLON,
		"colon":       COLON,
		"eq":          EQ,
		"comma":       COMMA,
		"comment":     COMMENT,
		"ignore":      IGNORE,
		"linestart":   LINESTART,
		"lineend":     LINEEND,
		"identifier":  IDENTIFIER,
		"whitespace":  WHITESPACE,
		"and":         AND,
		"or":          OR,
		"not":         NOT,
		"eof":         EOF
	}

	@staticmethod
	def getType(value):
		if value in TokenTypes.__matchTable:
			return TokenTypes.__matchTable[value]
		raise ValueError("Token type '{}' not recognized!".format(value))

	@staticmethod
	def getString(value):
		for e in TokenTypes.__matchTable:
			if TokenTypes.__matchTable[e] == value:
				return e
		raise ValueError("Token type '{}' not recognized!".format(value))