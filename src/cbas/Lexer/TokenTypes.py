
class TokenTypes():


	UNDEFINED     = -1

	# MISC
	LINENUMBER    = 0
	ASSIGNMENT    = 1
	CURLYOPEN     = 2
	CURLYCLOSE    = 3
	ROUNDOPEN     = 4
	ROUNDCLOSE    = 5
	SEMICOLON     = 6
	COLON         = 7
	COMMA         = 8
	COMMENT       = 9
	IGNORE        = 10
	LINESTART     = 11
	LINEEND       = 12
	IDENTIFIER    = 13
	WHITESPACE    = 14
	EOF           = 15


	# DATA TYPES
	BOOLEAN       = 16
	INTEGER       = 17
	FLOAT         = 18
	SIENTIFIC     = 19
	STRING        = 20

	# ARITHMETIC
	ADD           = 21
	MINUS         = 22
	MUL           = 23
	DIV           = 24
	EXPONENTIAL   = 25

	# LOGIC
	AND           = 26
	OR            = 27
	NOT           = 28

	EQ            = 29
	NEQ           = 30
	LE            = 31
	GE            = 32
	LESS          = 33
	MORE          = 34


	# STATEMENTS
	CLR           = 35
	CONT          = 36
	END           = 37
	NEW           = 38
	PISIGN        = 39
	RESTORE       = 40
	RETURN        = 41
	ST            = 42
	STATUS        = 43
	STOP          = 44
	TI            = 45
	TI_DOLLAR     = 46
	TIME          = 47
	TIME_DOLLAR   = 48

	# FUNCTIONS
	ABS           = 49
	ASC           = 50
	ATN           = 51
	COS           = 52
	EXP           = 53
	FRE           = 54
	INT           = 55
	LEN           = 56
	LOG           = 57
	POS           = 58
	RND           = 59
	SGN           = 60
	SIN           = 61
	SPC           = 62
	SQR           = 63
	SYS           = 64
	TAB           = 65
	TAN           = 66
	USR           = 67
	VAL           = 68



	APPEND        = 69
	AUTO          = 70
	BACKUP        = 71
	BANK          = 72
	BEGIN         = 73
	BEND          = 74
	BLOAD         = 75
	BOOT          = 76
	BOX           = 77
	BSAVE         = 78
	BUMP          = 79
	CATALOG       = 80
	CHAR          = 81
	CHR_DOLLAR    = 82
	CIRCLE        = 83
	CLOSE         = 84
	CMD           = 85
	COLLECT       = 86
	COLLISION     = 87
	COLOR         = 88
	CONCAT        = 89
	COPY          = 90
	DATA          = 91
	DCLOSE        = 92
	DEC           = 93
	DECLARE       = 94
	DEF           = 95
	DEF           = 96
	DEF_FN        = 97
	DELETE        = 98
	DIM           = 99
	DIRECTORY     = 100
	DISPOSE       = 101
	DLOAD         = 102
	DO            = 103
	DOPEN         = 104
	DRAW          = 105
	DS            = 106
	DS_DOLLAR     = 107
	DSAVE         = 108
	DVERIFY       = 109
	EL            = 110
	ELSE          = 111
	END           = 112
	ENVELOPE      = 113
	ER            = 114
	ERR_DOLLAR    = 115
	ESC           = 116
	EXIT          = 117
	FAST          = 118
	FETCH         = 119
	FILTER        = 120
	FN            = 121
	FOR           = 122
	GET           = 123
	GET_SHARP     = 124
	GETKEY        = 125
	GO            = 126
	GO64          = 127
	GOSUB         = 128
	GOTO          = 129
	GRAPHIC       = 130
	GSHAPE        = 131
	HEADER        = 132
	HELP          = 133
	HEX_DOLLAR    = 134
	IF            = 135
	INPUT         = 136
	INPUT_SHARP   = 137
	INSTR         = 138
	JOY           = 139
	KEY           = 140
	LEFT_DOLLAR   = 141
	LET           = 142
	LIST          = 143
	LOAD          = 144
	LOCATE        = 145
	LOOP          = 146
	MID_DOLLAR    = 147
	MONITOR       = 148
	MOVSPR        = 149
	NEXT          = 150
	OFF           = 151
	ON            = 152
	OPEN          = 153
	PAINT         = 154
	PEEK          = 155
	PEN           = 156
	PI            = 157
	PLAY          = 158
	POINTER       = 159
	POKE          = 160
	POPUPS        = 161
	POT           = 162
	PRINT         = 163
	PRINT_SHARP   = 164
	PRINTUSING    = 165
	PUDEF         = 166
	QUIT          = 167
	RCLR          = 168
	RDOT          = 169
	READ          = 170
	READ_SHARP    = 171
	RECORD        = 172
	RENAME        = 173
	RENUMBER      = 174
	RESUME        = 175
	RGR           = 176
	RIGHT_DOLLAR  = 177
	RLUM          = 178
	RREG          = 179
	RSPCOLOR      = 180
	RSPPOS        = 181
	RSSPRITE      = 182
	RUN           = 183
	RWINDOW       = 184
	SAVE          = 185
	SCALE         = 186
	SCNCLR        = 187
	SCRATCH       = 188
	SLEEP         = 189
	SLOW          = 190
	SOUND         = 191
	SPRCOLOR      = 192
	SPRDEF        = 193
	SPRITE        = 194
	SPRSAV        = 195
	SSHAPE        = 196
	STASH         = 197
	STEP          = 198
	STR_DOLLAR    = 199
	SWAP          = 200
	TEMPO         = 201
	THEN          = 202
	TO            = 203
	TRAP          = 204
	TROFF         = 205
	TRON          = 206
	UNTIL         = 207
	USER          = 208
	USING         = 209
	VERIFY        = 210
	VOL           = 211
	VOLUME        = 212
	WAIT          = 213
	WHILE         = 214
	WIDTH         = 215
	WINDOW        = 216
	XOR           = 217

	# MEX
	LABEL         = 218


    
	__matchTable = {
		"undefined":   UNDEFINED,
		"integer":     INTEGER,
		"float":       FLOAT,
		"sientific":   SIENTIFIC,
		"linenumber":  LINENUMBER,
		"string":      STRING,
		"boolean":     BOOLEAN,
		#"statement":   STATEMENT,
		#"function":    FUNCTION,
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
		"assignment":  ASSIGNMENT,
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
		"eof":         EOF,

		# Statements
		"clr":         CLR,
		"new":         NEW,
		"restore":     RESTORE,
		"return":      RETURN,
		"st":          ST,
		"status":      STATUS,
		"stop":        STOP,
		"ti":          TI,
		"ti_dollar":   TI_DOLLAR,
		"time":        TIME,
		"time_dollar": TIME_DOLLAR,
		"pisign":      PISIGN,
		"end":         END,
		"cont":        CONT,

		# Functions
        "rspcolor":     RSPCOLOR,
		"sprcolor":     SPRCOLOR,
        "rsprite":      RSSPRITE ,
        "right_dollar": RIGHT_DOLLAR,
        "hex_dollar":   HEX_DOLLAR,
        "rsppos":       RSPPOS   ,
        "left_dollar":  LEFT_DOLLAR,
        "instr":        INSTR,
        "chr_dollar":   CHR_DOLLAR,
        "mid_dollar":   MID_DOLLAR,
        "str_dollar":   STR_DOLLAR,
        "err_dollar":   ERR_DOLLAR,
        "rdot":         RDOT ,
        "peek":         PEEK ,
        "dec":          DEC,
        "pen":          PEN ,
        "pot":          POT,
        "usr":          USR,
        "abs":          ABS,
        "asc":          ASC,
        "atn":          ATN,
        "int":          INT,
        "cos":          COS,
        "exp":          EXP,
        "fre":          FRE,
        "len":          LEN,
        "log":          LOG,
        "pos":          POS,
        "rnd":          RND,
        "sgn":          SGN,
        "sin":          SIN,
        "spc":          SPC,
        "sqr":          SQR,
        "sys":          SYS,
        "tab":          TAB,
        "tan":          TAN,
        "val":          VAL,

		"to":           TO,
		"goto":         GOTO,
		"gosub":        GOSUB,
		"run":          RUN,
		"close":        CLOSE,
		"poke":         POKE,
		"verify":       VERIFY,

		"save":         SAVE,
		"load":         LOAD,
		"wait":         WAIT,
		"open":         OPEN,
		"next":         NEXT,
		"list":         LIST,
		"let":          LET,
		"fn":           FN,
		"READ":         READ,
		"def":          DEF,
		"on":           ON,
		"input":        INPUT,
		"print":        PRINT,
		"if":           IF,
		"then":         THEN,
		"for":          FOR,
		"to":           TO,
		"step":         STEP,
		"get":          GET,
		"get#":         GET_SHARP,
		"getkey":       GETKEY,
		"label":        LABEL
	}

	@staticmethod
	def toType(value):
		if value in TokenTypes.__matchTable:
			return TokenTypes.__matchTable[value]
		raise ValueError("Token type '{}' not recognized!".format(value))

	@staticmethod
	def toString(value):
		for e in TokenTypes.__matchTable:
			if TokenTypes.__matchTable[e] == value:
				return e
		#raise ValueError("Token type '{}' not recognized!".format(value))