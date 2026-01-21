
class TokenTypes():
	_index = 0
	INTEGER     =  _index;_index += 1
	FLOAT       =  _index;_index += 1
	SIENTIFIC   =  _index;_index += 1
	LINENUMBER  =  _index;_index += 1
	STRING      =  _index;_index += 1
	STATEMENT   =  _index;_index += 1
	FUNCTION    =  _index;_index += 1

	ADD         = _index;_index += 1
	MINUS       = _index;_index += 1
	MUL         = _index;_index += 1
	DIV         = _index;_index += 1
	EXPONENTIAL = _index;_index += 1

	EQ          = _index;_index += 1
	NEQ         = _index;_index += 1
	LE          = _index;_index += 1
	GE          = _index;_index += 1
	LESS        = _index;_index += 1
	MORE        = _index;_index += 1

	AND         = _index;_index += 1
	OR          = _index;_index += 1
	NOT         = _index;_index += 1

	CURLYOPEN   = _index;_index += 1
	CURLYCLOSE  = _index;_index += 1
	ROUNDOPEN   = _index;_index += 1
	ROUNDCLOSE  = _index;_index += 1
	
	SEMICOLON   = _index;_index += 1
	COLON       = _index;_index += 1
	
	COMMA       = _index;_index += 1
	COMMENT     = _index;_index += 1
	IGNORE      = _index;_index += 1
	LINESTART   = _index;_index += 1
	LINEEND     = _index;_index += 1
	IDENTIFIER  = _index;_index += 1
	WHITESPACE  = _index;_index += 1
	EOF         = _index;_index += 1

	__matchTable = {
		"integer":     INTEGER,
		"float":       FLOAT,
		"sientific":   SIENTIFIC,
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