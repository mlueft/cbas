import cbas.Lexer.TokenTypes
import cbas.Parser.BindingPower
import cbas.Ast.Expressions
import cbas.Ast.Statements

TokenTypes          = cbas.Lexer.TokenTypes.TokenTypes
BindingPower        = cbas.Parser.BindingPower.BindingPower
ExpressionParser    = cbas.Ast.Expressions.ExpressionParser
StatementParser     = cbas.Ast.Statements.StatementParser

class ParserMatrix():

    Statements = [
        TokenTypes.CLR,
        TokenTypes.NEW,
        TokenTypes.RESTORE,
        TokenTypes.RETURN,
        TokenTypes.ST,
        TokenTypes.STATUS,
        TokenTypes.STOP,
        TokenTypes.TI,
        TokenTypes.TI_DOLLAR,
        TokenTypes.TIME,
        TokenTypes.TIME_DOLLAR,
        TokenTypes.PISIGN,
        TokenTypes.END,
        TokenTypes.CONT,
        TokenTypes.GOTO,
        TokenTypes.GOSUB,
        TokenTypes.RUN,
        TokenTypes.CLOSE,
        TokenTypes.POKE,
        TokenTypes.VERIFY,
        TokenTypes.SAVE,
        TokenTypes.LOAD,
        TokenTypes.WAIT,
        TokenTypes.OPEN,
        TokenTypes.NEXT,
        TokenTypes.LIST,
        TokenTypes.READ,
        TokenTypes.DATA,
        TokenTypes.GET,
        TokenTypes.GET_SHARP,
        TokenTypes.INPUT_SHARP,
        TokenTypes.PRINT_SHARP,
        TokenTypes.CMD,
        TokenTypes.DEF,
        TokenTypes.ON,
        TokenTypes.INPUT,
        TokenTypes.DIM,
        TokenTypes.PRINT,
        TokenTypes.SEMICOLON,
        TokenTypes.IF,
        TokenTypes.FOR
    ]

    Functions = [
        TokenTypes.SYS,
        TokenTypes.ABS,
        TokenTypes.LEFT_DOLLAR,
        TokenTypes.MID_DOLLAR,
        TokenTypes.RIGHT_DOLLAR,
        TokenTypes.STR_DOLLAR,
        TokenTypes.CHR_DOLLAR,
        TokenTypes.ABS,
        TokenTypes.ASC,
        TokenTypes.ATN,
        TokenTypes.PEEK,
        TokenTypes.COS,
        TokenTypes.FRE,
        TokenTypes.INT,
        TokenTypes.LEN,
        TokenTypes.LOG,
        TokenTypes.POS,
        TokenTypes.RND,
        TokenTypes.SGN,
        TokenTypes.SIN,
        TokenTypes.SPC,
        TokenTypes.SQR,
        TokenTypes.TAB,
        TokenTypes.TAN,
        TokenTypes.USR,
        TokenTypes.VAL,
        TokenTypes.EXP
    ]

    Parameters = [
        
        {
            "name":""
        },
        {
            "name":""
        },
        {
            "name":""
        },
        {
            "name":""
        },
        {
            "name":""
        },
        {
            "name":""
        },
        {
            "name":""
        },
        {
            "name":""
        },
        {
            "name":""
        }
    ]
    
    Tokens = {
        
        # 0 - default

        # 1 - comma

        # 2 - Assignment
        "assignment":         { "category": "led", "bindingpower": BindingPower.ASSIGNMENT,    "type": TokenTypes.ASSIGNMENT,    "handler": ExpressionParser.parseAssignmentExpression    },

        # 3 - Logical
        "logicAnd":           { "category": "led", "bindingpower": BindingPower.LOGICAL,       "type": TokenTypes.AND,           "handler": ExpressionParser.parseBinaryExpression    },
        "logicOr":            { "category": "led", "bindingpower": BindingPower.LOGICAL,       "type": TokenTypes.OR,            "handler": ExpressionParser.parseBinaryExpression    },
        "logicNot":           { "category": "led", "bindingpower": BindingPower.LOGICAL,       "type": TokenTypes.NOT,           "handler": ExpressionParser.parseBinaryExpression    },
        "logicNotPref":       { "category": "nud", "bindingpower": BindingPower.LOGICAL,       "type": TokenTypes.NOT,           "handler": ExpressionParser.parsePrefixExpression    },

        # 4 - Relational
        "compareEQ":          { "category": "led", "bindingpower": BindingPower.RELATIONAL,    "type": TokenTypes.EQ,            "handler": ExpressionParser.parseBinaryExpression    },
        "compareNeq":         { "category": "led", "bindingpower": BindingPower.RELATIONAL,    "type": TokenTypes.NEQ,           "handler": ExpressionParser.parseBinaryExpression    },
        "compareLessEqual":   { "category": "led", "bindingpower": BindingPower.RELATIONAL,    "type": TokenTypes.LE,            "handler": ExpressionParser.parseBinaryExpression    },
        "compareGraterEqual": { "category": "led", "bindingpower": BindingPower.RELATIONAL,    "type": TokenTypes.GE,            "handler": ExpressionParser.parseBinaryExpression    },
        "compareLess":        { "category": "led", "bindingpower": BindingPower.RELATIONAL,    "type": TokenTypes.LESS,          "handler": ExpressionParser.parseBinaryExpression    },
        "compareGreater":     { "category": "led", "bindingpower": BindingPower.RELATIONAL,    "type": TokenTypes.MORE,          "handler": ExpressionParser.parseBinaryExpression    },

        # 5 - Additive
        "arithmeticAdd":      { "category": "led", "bindingpower": BindingPower.ADDITIVE,      "type" :TokenTypes.ADD,           "handler": ExpressionParser.parseBinaryExpression    },
        "arithmeticMinus":    { "category": "led", "bindingpower": BindingPower.ADDITIVE,      "type": TokenTypes.MINUS,         "handler": ExpressionParser.parseBinaryExpression    },

        # 6 - Multiplicative
        "arithmeticMul":      { "category": "led", "bindingpower": BindingPower.MULTIPLICATIVE, "type": TokenTypes.MUL,          "handler": ExpressionParser.parseBinaryExpression    },
        "arithmeticDiv":      { "category": "led", "bindingpower": BindingPower.MULTIPLICATIVE, "type": TokenTypes.DIV,          "handler": ExpressionParser.parseBinaryExpression    },
        "arithmeticExponent": { "category": "led", "bindingpower": BindingPower.MULTIPLICATIVE, "type": TokenTypes.EXPONENTIAL,  "handler": ExpressionParser.parseBinaryExpression    },

        # 7 - literals & symbols
        "literalScientific":  { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.SIENTIFIC,    "handler": ExpressionParser.parsePrimaryExpression   },
        "literalFloat":       { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.FLOAT,        "handler": ExpressionParser.parsePrimaryExpression   },
        "literalInt":         { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.INTEGER,      "handler": ExpressionParser.parsePrimaryExpression   },
        "literalString":      { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.STRING,       "handler": ExpressionParser.parsePrimaryExpression   },
        "literalBoolean":     { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.BOOLEAN,      "handler": ExpressionParser.parsePrimaryExpression   },
        "identifier":         { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.IDENTIFIER,   "handler": ExpressionParser.parsePrimaryExpression   },
        "lineNumber":         { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.LINENUMBER,   "handler": ExpressionParser.parsePrimaryExpression   },
        "label":              { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.LABEL,        "handler": StatementParser.parseLabelStatement     },
        
        # 8 - unary & prefix
        "unary":              { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.MINUS,        "handler": ExpressionParser.parsePrefixExpression    },

        # 9 - call 
        "call":               { "category": "led", "bindingpower": BindingPower.CALL,          "type": TokenTypes.ROUNDOPEN,     "handler": ExpressionParser.parseProcedureCallExpression      },


        # 10 - member / computed & call

        "sys":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.SYS,          "handler": ExpressionParser.parsePrimaryExpression    },
        "abs":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.ABS,          "handler": ExpressionParser.parsePrimaryExpression    },
        "asc":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.ASC,          "handler": ExpressionParser.parsePrimaryExpression    },
        "atn":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.ATN,          "handler": ExpressionParser.parsePrimaryExpression    },
        "str_dollar":         { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.STR_DOLLAR,   "handler": ExpressionParser.parsePrimaryExpression    },
        "right_dollar":       { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.RIGHT_DOLLAR, "handler": ExpressionParser.parsePrimaryExpression    },
        "left_dollar":        { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.LEFT_DOLLAR,  "handler": ExpressionParser.parsePrimaryExpression    },
        "mid_dollar":         { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.MID_DOLLAR,   "handler": ExpressionParser.parsePrimaryExpression    },
        "chr_dollar":         { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.CHR_DOLLAR,   "handler": ExpressionParser.parsePrimaryExpression    },
        "peek":               { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.PEEK,         "handler": ExpressionParser.parsePrimaryExpression    },
        "cos":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.COS,          "handler": ExpressionParser.parsePrimaryExpression    },
        "fre":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.FRE,          "handler": ExpressionParser.parsePrimaryExpression    },
        "int":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.INT,          "handler": ExpressionParser.parsePrimaryExpression    },
        "len":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.LEN,          "handler": ExpressionParser.parsePrimaryExpression    },
        "log":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.LOG,          "handler": ExpressionParser.parsePrimaryExpression    },
        "pos":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.POS,          "handler": ExpressionParser.parsePrimaryExpression    },
        "rnd":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.RND,          "handler": ExpressionParser.parsePrimaryExpression    },
        "sgn":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.SGN,          "handler": ExpressionParser.parsePrimaryExpression    },
        "sin":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.SIN,          "handler": ExpressionParser.parsePrimaryExpression    },
        "spc":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.SPC,          "handler": ExpressionParser.parsePrimaryExpression    },
        "sqr":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.SQR,          "handler": ExpressionParser.parsePrimaryExpression    },
        "tab":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.TAB,          "handler": ExpressionParser.parsePrimaryExpression    },
        "tan":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.TAN,          "handler": ExpressionParser.parsePrimaryExpression    },
        "usr":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.USR,          "handler": ExpressionParser.parsePrimaryExpression    },
        "val":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.VAL,          "handler": ExpressionParser.parsePrimaryExpression    },
        "exp":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.EXP,          "handler": ExpressionParser.parsePrimaryExpression    },
        "semicolon":          { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.SEMICOLON,    "handler": ExpressionParser.parsePrimaryExpression    },

        "clr":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.CLR,          "handler": StatementParser.parseStatementCallStatement    },
        "new":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.NEW,          "handler": StatementParser.parseStatementCallStatement    },
        "restore":            { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.RESTORE,      "handler": StatementParser.parseStatementCallStatement    },
        "return":             { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.RETURN,       "handler": StatementParser.parseStatementCallStatement    },
        "st":                 { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.ST,           "handler": StatementParser.parseStatementCallStatement    },
        "status":             { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.STATUS,       "handler": StatementParser.parseStatementCallStatement    },
        "stop":               { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.STOP,         "handler": StatementParser.parseStatementCallStatement    },
        "ti":                 { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.TI,           "handler": StatementParser.parseStatementCallStatement    },
        "ti_dollar":          { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.TI_DOLLAR,    "handler": StatementParser.parseStatementCallStatement    },
        "time":               { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.TIME,         "handler": StatementParser.parseStatementCallStatement    },
        "time_dollar":        { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.TIME_DOLLAR,  "handler": StatementParser.parseStatementCallStatement    },
        "pisign":             { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.PISIGN,       "handler": StatementParser.parseStatementCallStatement    },
        "end":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.END,          "handler": StatementParser.parseStatementCallStatement    },
        "cont":               { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.CONT,         "handler": StatementParser.parseStatementCallStatement    },
        "goto":               { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.GOTO,         "handler": StatementParser.parseStatementCallStatement    },
        "gosub":              { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.GOSUB,        "handler": StatementParser.parseStatementCallStatement    },
        "run":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.RUN,          "handler": StatementParser.parseStatementCallStatement    },
        "close":              { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.CLOSE,        "handler": StatementParser.parseStatementCallStatement    },
        "verify":             { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.VERIFY,       "handler": StatementParser.parseStatementCallStatement    },
        "save":               { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.SAVE,         "handler": StatementParser.parseStatementCallStatement    },
        "load":               { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.LOAD,         "handler": StatementParser.parseStatementCallStatement    },
        "wait":               { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.WAIT,         "handler": StatementParser.parseStatementCallStatement    },
        "poke":               { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.POKE,         "handler": StatementParser.parseStatementCallStatement    },
        "open":               { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.OPEN,         "handler": StatementParser.parseStatementCallStatement    },
        "next":               { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.NEXT,         "handler": StatementParser.parseStatementCallStatement    },
        "list":               { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.LIST,         "handler": StatementParser.parseListStatement          },
        "fn":                 { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.FN,           "handler": ExpressionParser.parseFNExpression           },
        "read":               { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.READ,         "handler": StatementParser.parseStatementCallStatement    },
        "data":               { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.DATA,         "handler": StatementParser.parseStatementCallStatement    },
        "get":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.GET,          "handler": StatementParser.parseStatementCallStatement    },
        "get_sharp":          { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.GET_SHARP,    "handler": StatementParser.parseStatementCallStatement    },
        "print_sharp":        { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.PRINT_SHARP,  "handler": StatementParser.parseStatementCallStatement    },
        "input_sharp":        { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.INPUT_SHARP,  "handler": StatementParser.parseStatementCallStatement    },
        "cmd":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.CMD,          "handler": StatementParser.parseCMDStatement          },
        "def":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.DEF,          "handler": StatementParser.parseDEFStatement          },
        "colon":              { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.COLON,        "handler": ExpressionParser.parsePrimaryExpression      },
        "on":                 { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.ON,           "handler": ExpressionParser.parseONExpression           },
        "input":              { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.INPUT,        "handler": StatementParser.parseINPUTStatement        },
        "dim":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.DIM,          "handler": StatementParser.parseDIMStatement          },
        "print":              { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.PRINT,        "handler": StatementParser.parsePRINTStatement        },
        "if":                 { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.IF,           "handler": StatementParser.parseIFStatement           },
        "for":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.FOR,          "handler": StatementParser.parseFORStatement          },


        "to":                 { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.TO,           "handler": ExpressionParser.parsePrimaryExpression      },
        
        # grouping expr
        "grouping":           { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.ROUNDOPEN,    "handler": ExpressionParser.parseGroupingExpression     },
        "block_statement":    { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.CURLYOPEN,    "handler": StatementParser.parseBlockStatement          },


        "lineend":            { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.LINEEND,      "handler": ExpressionParser.parsePrimaryExpression      },
        "eof":                { "category": "led", "bindingpower": 0,                           "type": TokenTypes.EOF,          "handler": ExpressionParser.parseIgnoreToken            }

    }

    Matrix = {
        # ------------------------------------------------------------------
        #                         AR    PP    V2    v3.5  v3.6  v4    v4+   v7    v10
        # ------------------------------------------------------------------
        "assignment":           [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],

        "logicAnd":             [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "logicOr":              [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "logicNot":             [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "logicNotPref":         [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "compareEQ":            [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "compareNeq":           [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "compareLessEqual":     [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "compareGraterEqual":   [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "compareLess":          [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "compareGreater":       [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],

        "arithmeticAdd":        [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "arithmeticMinus":      [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "arithmeticMul":        [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "arithmeticDiv":        [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "arithmeticExponent":   [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ], # not yet implemented
        
        "eof":                  [ 1,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "literalScientific":    [ 1,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "literalFloat":         [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "literalInt":           [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "literalString":        [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "literalBoolean":       [ 0,    1,    0,    0,    0,    0,    0,    0,    0    ],
        "identifier":           [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "lineNumber":           [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "label":                [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "unary":                [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "grouping":             [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "block_statement":      [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],

        "sys":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "abs":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "asc":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "atn":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "str_dollar":           [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "right_dollar":         [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "left_dollar":          [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "mid_dollar":           [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "chr_dollar":           [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "peek":                 [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "cos":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "fre":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "int":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "len":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "log":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "pos":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "rnd":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "sgn":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "sin":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "spc":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "sqr":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "tab":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "tan":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "usr":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "val":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "exp":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],

        "clr":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "new":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "restore":              [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "return":               [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "st":                   [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "status":               [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "stop":                 [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "ti":                   [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "ti_dollar":            [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "time_dollar":          [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "time":                 [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "pisign":               [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "end":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "cont":                 [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],

        "to":                   [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "goto":                 [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "gosub":                [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "run":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "close":                [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "poke":                 [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "verify":               [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        
        "save":                 [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "load":                 [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "wait":                 [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "open":                 [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "next":                 [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "list":                 [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "fn":                   [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "read":                 [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "data":                 [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "get":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "get_sharp":            [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "print_sharp":          [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "input_sharp":          [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "cmd":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "def":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "colon":                [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "on":                   [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "input":                [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "dim":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "print":                [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "semicolon":            [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "if":                   [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        "for":                  [ 0,    0,    1,    1,    0,    0,    0,    0,    0    ],
        
        "lineend":              [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],

        "call":                 [ 0,    0,    1,    0,    0,    0,    0,    0,    0    ]

    }
