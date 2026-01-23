from operator import attrgetter

import cbas.Lexer.TokenTypes
import cbas.Parser.BindingPower
import cbas.Lexer.ConfigToken
import cbas.Parser.ConfigToken
import cbas.Config.LexerConfig
import cbas.Config.ParserConfig

TokenTypes = cbas.Lexer.TokenTypes.TokenTypes
BindingPower = cbas.Parser.BindingPower.BindingPower
LexerConfigToken = cbas.Lexer.ConfigToken.ConfigToken
LexerConfig = cbas.Config.LexerConfig.LexerConfig
ParserConfigToken = cbas.Parser.ConfigToken.ConfigToken
ParserConfig = cbas.Config.ParserConfig.ParserConfig

class Config():

    ARITHMETIC   = 0
    PREPROCESSOR = 1
    V2           = 2
    V35          = 3
    V36          = 4
    V4           = 5
    V4P          = 6
    V7           = 7
    V10          = 8

    # Order is important
    lexerTokens = {

        "lineNumber":           { "order":    0, "type": TokenTypes.LINENUMBER,  "expression": "^[0-9]+" },

        "literalSientific":     { "order":   10, "type": TokenTypes.SIENTIFIC,   "expression": "(?i)-?[0-9]+[.]?[0-9]*e-*[0-9]+[.]?[0-9]*" },
        "literalFloat":         { "order":   20, "type": TokenTypes.FLOAT,       "expression": "[0-9]+[.][0-9]*" },
        "literalInt":           { "order":   40, "type": TokenTypes.INTEGER,     "expression": "[0-9]+[%]?" },
        "literalString":        { "order":   50, "type": TokenTypes.STRING,      "expression": "(?i)\"[^\"]*\"" },

        "comment":              { "order":  100, "type": TokenTypes.COMMENT,     "expression": "(?i)rem[^:]*" },
        "printUsing":           { "order":  110, "type": TokenTypes.STATEMENT,   "expression": "(?i)PRINT USING" },
        "collision":            { "order":  120, "type": TokenTypes.STATEMENT,   "expression": "(?i)COLLISION" },
        "directory":            { "order":  130, "type": TokenTypes.STATEMENT,   "expression": "(?i)DIRECTORY" },
        "envelope":             { "order":  140, "type": TokenTypes.STATEMENT,   "expression": "(?i)ENVELOPE" },
        "renumber":             { "order":  150, "type": TokenTypes.STATEMENT,   "expression": "(?i)RENUMBER" },
        "rspcolor":             { "order":  160, "type": TokenTypes.STATEMENT,   "expression": "(?i)RSPCOLOR" },
        "sprcolor":             { "order":  170, "type": TokenTypes.STATEMENT,   "expression": "(?i)SPRCOLOR" },
        "catalog":              { "order":  180, "type": TokenTypes.STATEMENT,   "expression": "(?i)CATALOG" },
        "collect":              { "order":  190, "type": TokenTypes.STATEMENT,   "expression": "(?i)COLLECT" },
        "dispose":              { "order":  200, "type": TokenTypes.STATEMENT,   "expression": "(?i)DISPOSE" },
        "dverify":              { "order":  210, "type": TokenTypes.STATEMENT,   "expression": "(?i)DVERIFY" },
        "graphic":              { "order":  220, "type": TokenTypes.STATEMENT,   "expression": "(?i)GRAPHIC" },
        "monitor":              { "order":  230, "type": TokenTypes.STATEMENT,   "expression": "(?i)MONITOR" },
        "pointer":              { "order":  240, "type": TokenTypes.STATEMENT,   "expression": "(?i)POINTER" },
        "rsprite":              { "order":  250, "type": TokenTypes.STATEMENT,   "expression": "(?i)RSPRITE" },
        "rwindow":              { "order":  260, "type": TokenTypes.STATEMENT,   "expression": "(?i)RWINDOW" },
        "scratch":              { "order":  270, "type": TokenTypes.STATEMENT,   "expression": "(?i)SCRATCH" },
        "restore":              { "order":  280, "type": TokenTypes.STATEMENT,   "expression": "(?i)RESTORE" },
        "right$":               { "order":  290, "type": TokenTypes.FUNCTION,    "expression": "(?i)RIGHT\$" },
        "time$":                { "order":  300, "type": TokenTypes.STATEMENT,   "expression": "(?i)TIME\$" },
        "quit":                 { "order":  310, "type": TokenTypes.STATEMENT,   "expression": "(?i)(QUIT)" },
        "append":               { "order":  320, "type": TokenTypes.STATEMENT,   "expression": "(?i)APPEND" },
        "backup":               { "order":  330, "type": TokenTypes.STATEMENT,   "expression": "(?i)BACKUP" },
        "circle":               { "order":  340, "type": TokenTypes.STATEMENT,   "expression": "(?i)CIRCLE" },
        "concat":               { "order":  350, "type": TokenTypes.STATEMENT,   "expression": "(?i)CONCAT" },
        "dclear":               { "order":  360, "type": TokenTypes.STATEMENT,   "expression": "(?i)DCLEAR" },
        "dclose":               { "order":  370, "type": TokenTypes.STATEMENT,   "expression": "(?i)DCLOSE" },
        "deffn":                { "order":  380, "type": TokenTypes.STATEMENT,   "expression": "(?i)DEF FN" },
        "delete":               { "order":  390, "type": TokenTypes.STATEMENT,   "expression": "(?i)DELETE" },
        "filter":               { "order":  400, "type": TokenTypes.STATEMENT,   "expression": "(?i)FILTER" },
        "getkey":               { "order":  410, "type": TokenTypes.STATEMENT,   "expression": "(?i)GETKEY" },
        "gshape":               { "order":  420, "type": TokenTypes.STATEMENT,   "expression": "(?i)GSHAPE" },
        "header":               { "order":  430, "type": TokenTypes.STATEMENT,   "expression": "(?i)HEADER" },
        "hex$":                 { "order":  440, "type": TokenTypes.STATEMENT,   "expression": "(?i)HEX\$"  },
        "locate":               { "order":  450, "type": TokenTypes.STATEMENT,   "expression": "(?i)LOCATE" },
        "movspr":               { "order":  460, "type": TokenTypes.STATEMENT,   "expression": "(?i)MOVSPR" },
        "record":               { "order":  470, "type": TokenTypes.STATEMENT,   "expression": "(?i)RECORD" },
        "rename":               { "order":  480, "type": TokenTypes.STATEMENT,   "expression": "(?i)RENAME" },
        "resume":               { "order":  490, "type": TokenTypes.STATEMENT,   "expression": "(?i)RESUME" },
        "rsppos":               { "order":  500, "type": TokenTypes.STATEMENT,   "expression": "(?i)RSPPOS" },
        "scnclr":               { "order":  510, "type": TokenTypes.STATEMENT,   "expression": "(?i)SCNCLR" },
        "sprdef":               { "order":  520, "type": TokenTypes.STATEMENT,   "expression": "(?i)SPRDEF" },
        "sprite":               { "order":  530, "type": TokenTypes.STATEMENT,   "expression": "(?i)SPRITE" },
        "sprsav":               { "order":  540, "type": TokenTypes.STATEMENT,   "expression": "(?i)SPRSAV" },
        "sshape":               { "order":  550, "type": TokenTypes.STATEMENT,   "expression": "(?i)SSHAPE" },
        "window":               { "order":  560, "type": TokenTypes.STATEMENT,   "expression": "(?i)WINDOW" },
        "popups":               { "order":  570, "type": TokenTypes.STATEMENT,   "expression": "(?i)POPUPS" },
        "volume":               { "order":  580, "type": TokenTypes.STATEMENT,   "expression": "(?i)VOLUME" },
        "status":               { "order":  590, "type": TokenTypes.STATEMENT,   "expression": "(?i)STATUS" },
        "return":               { "order":  600, "type": TokenTypes.STATEMENT,   "expression": "(?i)RETURN" },
        "verify":               { "order":  610, "type": TokenTypes.STATEMENT,   "expression": "(?i)VERIFY" },
        "input#":               { "order":  620, "type": TokenTypes.STATEMENT,   "expression": "(?i)INPUT#" },
        "print#":               { "order":  630, "type": TokenTypes.STATEMENT,   "expression": "(?i)PRINT#" },
        "left$":                { "order":  640, "type": TokenTypes.FUNCTION,    "expression": "(?i)LEFT\$" },
        "pudef":                { "order":  650, "type": TokenTypes.STATEMENT,   "expression": "(?i)PUDEF" },
        "off":                  { "order":  660, "type": TokenTypes.STATEMENT,   "expression": "(?i)(OFF)" },
        "bload":                { "order":  670, "type": TokenTypes.STATEMENT,   "expression": "(?i)BLOAD" },
        "bsave":                { "order":  680, "type": TokenTypes.STATEMENT,   "expression": "(?i)BSAVE" },
        "dload":                { "order":  690, "type": TokenTypes.STATEMENT,   "expression": "(?i)DLOAD" },
        "dopen":                { "order":  700, "type": TokenTypes.STATEMENT,   "expression": "(?i)DOPEN" },
        "ds$":                  { "order":  710, "type": TokenTypes.STATEMENT,   "expression": "(?i)DS\$"  },
        "dsave":                { "order":  720, "type": TokenTypes.STATEMENT,   "expression": "(?i)DSAVE" },
        "fetch":                { "order":  730, "type": TokenTypes.STATEMENT,   "expression": "(?i)FETCH" },
        "instr":                { "order":  740, "type": TokenTypes.STATEMENT,   "expression": "(?i)INSTR" },
        "paint":                { "order":  750, "type": TokenTypes.STATEMENT,   "expression": "(?i)PAINT" },
        "read#":                { "order":  760, "type": TokenTypes.STATEMENT,   "expression": "(?i)READ#" },
        "scale":                { "order":  770, "type": TokenTypes.STATEMENT,   "expression": "(?i)SCALE" },
        "sleep":                { "order":  780, "type": TokenTypes.STATEMENT,   "expression": "(?i)SLEEP" },
        "sound":                { "order":  790, "type": TokenTypes.STATEMENT,   "expression": "(?i)SOUND" },
        "stash":                { "order":  800, "type": TokenTypes.STATEMENT,   "expression": "(?i)STASH" },
        "tempo":                { "order":  810, "type": TokenTypes.STATEMENT,   "expression": "(?i)TEMPO" },
        "troff":                { "order":  820, "type": TokenTypes.STATEMENT,   "expression": "(?i)TROFF" },
        "using":                { "order":  830, "type": TokenTypes.STATEMENT,   "expression": "(?i)USING" },
        "while":                { "order":  840, "type": TokenTypes.STATEMENT,   "expression": "(?i)WHILE" },
        "width":                { "order":  850, "type": TokenTypes.STATEMENT,   "expression": "(?i)WIDTH" },
        "until":                { "order":  860, "type": TokenTypes.STATEMENT,   "expression": "(?i)UNTIL" },
        "print":                { "order":  870, "type": TokenTypes.STATEMENT,   "expression": "(?i)PRINT" },
        "gosub":                { "order":  880, "type": TokenTypes.STATEMENT,   "expression": "(?i)GOSUB" },
        "input":                { "order":  890, "type": TokenTypes.STATEMENT,   "expression": "(?i)INPUT" },
        "close":                { "order":  900, "type": TokenTypes.STATEMENT,   "expression": "(?i)CLOSE" },
        "chr$":                 { "order":  910, "type": TokenTypes.FUNCTION,    "expression": "(?i)CHR\$" },
        "mid$":                 { "order":  920, "type": TokenTypes.FUNCTION,    "expression": "(?i)MID\$" },
        "str$":                 { "order":  930, "type": TokenTypes.FUNCTION,    "expression": "(?i)STR\$" },
        "err$":                 { "order":  940, "type": TokenTypes.STATEMENT,   "expression": "(?i)ERR\$" },
        "color":                { "order":  950, "type": TokenTypes.STATEMENT,   "expression": "(?i)COLOR" },
        "begin":                { "order":  960, "type": TokenTypes.STATEMENT,   "expression": "(?i)BEGIN" },
        "auto":                 { "order":  970, "type": TokenTypes.STATEMENT,   "expression": "(?i)AUTO" },
        "bank":                 { "order":  980, "type": TokenTypes.STATEMENT,   "expression": "(?i)BANK" },
        "pi":                   { "order":  990, "type": TokenTypes.STATEMENT,   "expression": "(?i)(PI)" },
        "bend":                 { "order": 1000, "type": TokenTypes.STATEMENT,   "expression": "(?i)BEND" },
        "boot":                 { "order": 1010, "type": TokenTypes.STATEMENT,   "expression": "(?i)BOOT" },
        "bump":                 { "order": 1020, "type": TokenTypes.STATEMENT,   "expression": "(?i)BUMP" },
        "char":                 { "order": 1030, "type": TokenTypes.STATEMENT,   "expression": "(?i)CHAR" },
        "copy":                 { "order": 1040, "type": TokenTypes.STATEMENT,   "expression": "(?i)COPY" },
        "draw":                 { "order": 1050, "type": TokenTypes.STATEMENT,   "expression": "(?i)DRAW" },
        "else":                 { "order": 1060, "type": TokenTypes.STATEMENT,   "expression": "(?i)ELSE" },
        "exit":                 { "order": 1070, "type": TokenTypes.STATEMENT,   "expression": "(?i)EXIT" },
        "fast":                 { "order": 1080, "type": TokenTypes.STATEMENT,   "expression": "(?i)FAST" },
        "go64":                 { "order": 1090, "type": TokenTypes.STATEMENT,   "expression": "(?i)GO64" },
        "help":                 { "order": 1100, "type": TokenTypes.STATEMENT,   "expression": "(?i)HELP" },
        "loop":                 { "order": 1110, "type": TokenTypes.STATEMENT,   "expression": "(?i)LOOP" },
        "play":                 { "order": 1120, "type": TokenTypes.STATEMENT,   "expression": "(?i)PLAY" },
        "rclr":                 { "order": 1130, "type": TokenTypes.STATEMENT,   "expression": "(?i)RCLR" },
        "rdot":                 { "order": 1140, "type": TokenTypes.STATEMENT,   "expression": "(?i)RDOT" },
        "rreg":                 { "order": 1150, "type": TokenTypes.STATEMENT,   "expression": "(?i)RREG" },
        "step":                 { "order": 1160, "type": TokenTypes.STATEMENT,   "expression": "(?i)STEP" },
        "swap":                 { "order": 1170, "type": TokenTypes.STATEMENT,   "expression": "(?i)SWAP" },
        "then":                 { "order": 1180, "type": TokenTypes.STATEMENT,   "expression": "(?i)THEN" },
        "trap":                 { "order": 1190, "type": TokenTypes.STATEMENT,   "expression": "(?i)TRAP" },
        "tron":                 { "order": 1200, "type": TokenTypes.STATEMENT,   "expression": "(?i)TRON" },
        "user":                 { "order": 1210, "type": TokenTypes.STATEMENT,   "expression": "(?i)USER" },
        "rlum":                 { "order": 1220, "type": TokenTypes.STATEMENT,   "expression": "(?i)RLUM" },
        "time":                 { "order": 1230, "type": TokenTypes.STATEMENT,   "expression": "(?i)TIME" },
        "step":                 { "order": 1250, "type": TokenTypes.STATEMENT,   "expression": "(?i)STEP" },
        "goto":                 { "order": 1260, "type": TokenTypes.STATEMENT,   "expression": "(?i)GOTO" },
        "read":                 { "order": 1270, "type": TokenTypes.STATEMENT,   "expression": "(?i)READ" },
        "open":                 { "order": 1280, "type": TokenTypes.STATEMENT,   "expression": "(?i)OPEN" },
        "peek":                 { "order": 1290, "type": TokenTypes.FUNCTION,    "expression": "(?i)PEEK" },
        "poke":                 { "order": 1300, "type": TokenTypes.STATEMENT,   "expression": "(?i)POKE" },
        "list":                 { "order": 1310, "type": TokenTypes.STATEMENT,   "expression": "(?i)LIST" },
        "load":                 { "order": 1320, "type": TokenTypes.STATEMENT,   "expression": "(?i)LOAD" },
        "next":                 { "order": 1330, "type": TokenTypes.STATEMENT,   "expression": "(?i)NEXT" },
        "save":                 { "order": 1340, "type": TokenTypes.STATEMENT,   "expression": "(?i)SAVE" },
        "stop":                 { "order": 1350, "type": TokenTypes.STATEMENT,   "expression": "(?i)STOP" },
        "data":                 { "order": 1360, "type": TokenTypes.STATEMENT,   "expression": "(?i)DATA" },
        "slow":                 { "order": 1370, "type": TokenTypes.STATEMENT,   "expression": "(?i)SLOW" },
        "wait":                 { "order": 1380, "type": TokenTypes.STATEMENT,   "expression": "(?i)WAIT" },
        "cont":                 { "order": 1390, "type": TokenTypes.STATEMENT,   "expression": "(?i)CONT" },
        "get#":                 { "order": 1400, "type": TokenTypes.STATEMENT,   "expression": "(?i)GET#" },
        "get":                  { "order": 1410, "type": TokenTypes.STATEMENT,   "expression": "(?i)GET" },
        "box":                  { "order": 1420, "type": TokenTypes.STATEMENT,   "expression": "(?i)BOX" },
        "dec":                  { "order": 1430, "type": TokenTypes.STATEMENT,   "expression": "(?i)DEC" },
        "def":                  { "order": 1440, "type": TokenTypes.STATEMENT,   "expression": "(?i)DEF" },
        "end":                  { "order": 1450, "type": TokenTypes.STATEMENT,   "expression": "(?i)END" },
        "esc":                  { "order": 1460, "type": TokenTypes.STATEMENT,   "expression": "(?i)ESC" },
        "joy":                  { "order": 1470, "type": TokenTypes.STATEMENT,   "expression": "(?i)JOY" },
        "key":                  { "order": 1480, "type": TokenTypes.STATEMENT,   "expression": "(?i)KEY" },
        "pen":                  { "order": 1490, "type": TokenTypes.STATEMENT,   "expression": "(?i)PEN" },
        "pot":                  { "order": 1500, "type": TokenTypes.STATEMENT,   "expression": "(?i)POT" },
        "rgr":                  { "order": 1510, "type": TokenTypes.STATEMENT,   "expression": "(?i)RGR" },
        "vol":                  { "order": 1520, "type": TokenTypes.STATEMENT,   "expression": "(?i)VOL" },
        "xor":                  { "order": 1530, "type": TokenTypes.STATEMENT,   "expression": "(?i)XOR" },
        "usr":                  { "order": 1540, "type": TokenTypes.FUNCTION,    "expression": "(?i)USR" },
        "def":                  { "order": 1550, "type": TokenTypes.STATEMENT,   "expression": "(?i)DEF" },
        "end":                  { "order": 1560, "type": TokenTypes.STATEMENT,   "expression": "(?i)END" },
        "let":                  { "order": 1570, "type": TokenTypes.STATEMENT,   "expression": "(?i)LET" },
        "abs":                  { "order": 1580, "type": TokenTypes.FUNCTION,    "expression": "(?i)ABS" },
        "asc":                  { "order": 1590, "type": TokenTypes.FUNCTION,    "expression": "(?i)ASC" },
        "atn":                  { "order": 1600, "type": TokenTypes.FUNCTION,    "expression": "(?i)ATN" },
        "clr":                  { "order": 1610, "type": TokenTypes.STATEMENT,   "expression": "(?i)CLR" },
        "cmd":                  { "order": 1620, "type": TokenTypes.STATEMENT,   "expression": "(?i)CMD" },
        "int":                  { "order": 1630, "type": TokenTypes.FUNCTION,    "expression": "(?i)INT" },
        "cos":                  { "order": 1640, "type": TokenTypes.FUNCTION,    "expression": "(?i)COS" },
        "exp":                  { "order": 1650, "type": TokenTypes.FUNCTION,    "expression": "(?i)EXP" },
        "for":                  { "order": 1660, "type": TokenTypes.STATEMENT,   "expression": "(?i)FOR" },
        "fre":                  { "order": 1670, "type": TokenTypes.FUNCTION,    "expression": "(?i)FRE" },
        "len":                  { "order": 1680, "type": TokenTypes.FUNCTION,    "expression": "(?i)LEN" },
        "log":                  { "order": 1690, "type": TokenTypes.FUNCTION,    "expression": "(?i)LOG" },
        "new":                  { "order": 1700, "type": TokenTypes.STATEMENT,   "expression": "(?i)NEW" },
        "pos":                  { "order": 1710, "type": TokenTypes.FUNCTION,    "expression": "(?i)POS" },
        "rnd":                  { "order": 1730, "type": TokenTypes.FUNCTION,    "expression": "(?i)RND" },
        "run":                  { "order": 1740, "type": TokenTypes.STATEMENT,   "expression": "(?i)RUN" },
        "sgn":                  { "order": 1750, "type": TokenTypes.FUNCTION,    "expression": "(?i)SGN" },
        "sin":                  { "order": 1760, "type": TokenTypes.FUNCTION,    "expression": "(?i)SIN" },
        "spc":                  { "order": 1770, "type": TokenTypes.FUNCTION,    "expression": "(?i)SPC" },
        "sqr":                  { "order": 1780, "type": TokenTypes.FUNCTION,    "expression": "(?i)SQR" },
        "sys":                  { "order": 1790, "type": TokenTypes.STATEMENT,   "expression": "(?i)SYS" },
        "tab":                  { "order": 1800, "type": TokenTypes.FUNCTION,    "expression": "(?i)TAB" },
        "tan":                  { "order": 1810, "type": TokenTypes.FUNCTION,    "expression": "(?i)TAN" },
        "val":                  { "order": 1820, "type": TokenTypes.FUNCTION,    "expression": "(?i)VAL" },
        "dim":                  { "order": 1830, "type": TokenTypes.STATEMENT,   "expression": "(?i)DIM" },
        "logicAnd":             { "order": 1840, "type": TokenTypes.AND,         "expression": "(?i)AND" },
        "logicNot":             { "order": 1850, "type": TokenTypes.NOT,         "expression": "(?i)NOT" },
        "usr":                  { "order": 1860, "type": TokenTypes.FUNCTION,    "expression": "(?i)USR" },
        "ti$":                  { "order": 1870, "type": TokenTypes.STATEMENT,   "expression": "(?i)TI\$" },
        "ti":                   { "order": 1880, "type": TokenTypes.STATEMENT,   "expression": "(?i)TI" },
        "to":                   { "order": 1890, "type": TokenTypes.STATEMENT,   "expression": "(?i)TO" },
        "fn":                   { "order": 1900, "type": TokenTypes.STATEMENT,   "expression": "(?i)FN" },
        "do":                   { "order": 1910, "type": TokenTypes.STATEMENT,   "expression": "(?i)DO" },
        "ds":                   { "order": 1920, "type": TokenTypes.STATEMENT,   "expression": "(?i)DS" },
        "el":                   { "order": 1930, "type": TokenTypes.STATEMENT,   "expression": "(?i)EL" },
        "er":                   { "order": 1940, "type": TokenTypes.STATEMENT,   "expression": "(?i)ER" },
        "go":                   { "order": 1950, "type": TokenTypes.STATEMENT,   "expression": "(?i)GO" },
        "st":                   { "order": 1960, "type": TokenTypes.STATEMENT,   "expression": "(?i)ST" },
        "pi":                   { "order": 1970, "type": TokenTypes.STATEMENT,   "expression": "(?i)PI" },
        "to":                   { "order": 1980, "type": TokenTypes.STATEMENT,   "expression": "(?i)TO" },
        "st":                   { "order": 1990, "type": TokenTypes.STATEMENT,   "expression": "(?i)ST" },
        "if":                   { "order": 2000, "type": TokenTypes.STATEMENT,   "expression": "(?i)IF" },
        "on":                   { "order": 2010, "type": TokenTypes.STATEMENT,   "expression": "(?i)ON" },

        "logicOr":              { "order": 2020, "type": TokenTypes.OR,          "expression": "(?i)OR" },
        "piSign":               { "order": 2030, "type": TokenTypes.STATEMENT,   "expression": "(?i)π" },
        
        "arithmeticAdd":        { "order": 3000, "type": TokenTypes.ADD,         "expression": "(?i)\+" },
        "arithmeticMinus":      { "order": 3010, "type": TokenTypes.MINUS,       "expression": "(?i)\-" },
        "arithmeticMul":        { "order": 3020, "type": TokenTypes.MUL,         "expression": "(?i)\*" },
        "arithmeticDiv":        { "order": 3030, "type": TokenTypes.DIV,         "expression": "(?i)\/" },
        "arithmeticExponent":   { "order": 3040, "type": TokenTypes.EXPONENTIAL, "expression": "(?i)\^" },

        "compareNeq":           { "order": 3050, "type": TokenTypes.NEQ,         "expression": "(?i)\<>" },
        "compareLessEqual":     { "order": 3060, "type": TokenTypes.LE,          "expression": "(?i)\<=" },
        "compareGraterEqual":   { "order": 3070, "type": TokenTypes.GE,          "expression": "(?i)\>=" },
        "compareLess":          { "order": 3080, "type": TokenTypes.LESS,        "expression": "(?i)\<" },
        "compareGreater":       { "order": 3090, "type": TokenTypes.MORE,        "expression": "(?i)\>" },

        "curlyopen":            { "order": 3100, "type": TokenTypes.CURLYOPEN,   "expression": "(?i)\{" },
        "curlyclose":           { "order": 3110, "type": TokenTypes.CURLYCLOSE,  "expression": "(?i)\}" },
        "roundopen":            { "order": 3120, "type": TokenTypes.ROUNDOPEN,   "expression": "(?i)\(" },
        "roundclose":           { "order": 3130, "type": TokenTypes.ROUNDCLOSE,  "expression": "(?i)\)" },
        "semicolon":            { "order": 3140, "type": TokenTypes.SEMICOLON,   "expression": "(?i)\;" },
        "colon":                { "order": 3150, "type": TokenTypes.COLON,       "expression": "(?i)\:" },
        "eq":                   { "order": 3160, "type": TokenTypes.EQ,          "expression": "(?i)\=" },
        "comma":                { "order": 3170, "type": TokenTypes.COMMA,       "expression": "(?i)\," },

        "identifier":           { "order": 3180, "type": TokenTypes.IDENTIFIER,  "expression": "(?i)[a-z]{1}[a-z0-9]*[$]?" },
        "whitespace":           { "order": 3190, "type": TokenTypes.WHITESPACE,  "expression": "[\s]" }

    }
    
    lexerConfig = {
        # ------------------------------------------------------------------
        #                         AR    PP    V2    v3.5  v3.6  v4    v4+   v7    v10
        # ------------------------------------------------------------------
        "lineNumber":           [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "literalSientific":     [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "literalFloat":         [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "literalInt":           [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "literalString":        [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],

        "abs":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "append":               [ 0,    0,    0,    0,    1,    1,    1,    1,    1    ],
        "asc":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "atn":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "auto":                 [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "backup":               [ 0,    0,    0,    1,    1,    1,    1,    1,    1    ],
        "bank":                 [ 0,    0,    0,    0,    1,    0,    1,    1,    1    ],
        "begin":                [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "bend":                 [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "bload":                [ 0,    0,    0,    0,    1,    0,    1,    1,    1    ],
        "boot":                 [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "box":                  [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "bsave":                [ 0,    0,    0,    0,    1,    0,    1,    1,    1    ],
        "bump":                 [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "catalog":              [ 0,    0,    0,    0,    1,    1,    1,    1,    1    ],
        "char":                 [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "chr$":                 [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "circle":               [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "close":                [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "clr":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "cmd":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "collect":              [ 0,    0,    0,    1,    1,    1,    0,    1,    1    ],
        "collision":            [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "color":                [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "comment":              [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "concat":               [ 0,    0,    0,    0,    1,    1,    0,    1,    1    ],
        "cont":                 [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "copy":                 [ 0,    0,    0,    1,    1,    1,    1,    1,    1    ],
        "cos":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "data":                 [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "dclear":               [ 0,    0,    0,    0,    1,    0,    1,    1,    1    ],
        # ------------------------------------------------------------------
        #                         AR    PP    V2    v3.5  v3.6  v4    v4+   v7    v10
        # ------------------------------------------------------------------
        "dclose":               [ 0,    0,    0,    0,    1,    1,    1,    1,    1    ],
        "dec":                  [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "def":                  [ 0,    0,    1,    1,    0,    1,    1,    0,    0    ],
        "deffn":                [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "delete":               [ 0,    0,    0,    1,    1,    0,    1,    1,    1    ],
        "dim":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "directory":            [ 0,    0,    0,    1,    1,    1,    1,    1,    1    ],
        "dispose":              [ 0,    0,    0,    0,    0,    0,    1,    0,    0    ],
        "dload":                [ 0,    0,    0,    1,    1,    1,    1,    1,    1    ],
        "do":                   [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "dopen":                [ 0,    0,    0,    0,    1,    1,    1,    1,    1    ],
        "draw":                 [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "ds":                   [ 0,    0,    0,    1,    1,    1,    1,    1,    1    ],
        "ds$":                  [ 0,    0,    0,    1,    1,    1,    1,    1,    1    ],
        "dsave":                [ 0,    0,    0,    1,    1,    1,    1,    1,    1    ],
        "dverify":              [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "el":                   [ 0,    0,    0,    1,    1,    0,    1,    1,    1    ],
        "else":                 [ 0,    0,    0,    1,    1,    0,    1,    1,    1    ],
        "end":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "envelope":             [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "er":                   [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "err$":                 [ 0,    0,    0,    1,    1,    0,    1,    1,    1    ],
        "esc":                  [ 0,    0,    0,    0,    0,    0,    1,    0,    0    ],
        "exit":                 [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "exp":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "fast":                 [ 0,    0,    0,    0,    0,    0,    0,    1,    1    ],
        "fetch":                [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "filter":               [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "fn":                   [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "for":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "fre":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "get":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "get#":                 [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "getkey":               [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "go":                   [ 0,    0,    0,    0,    0,    1,    1,    0,    0    ],
        "go64":                 [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "gosub":                [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "goto":                 [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "graphic":              [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "gshape":               [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "header":               [ 0,    0,    0,    1,    1,    1,    1,    1,    1    ],
        "help":                 [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "hex$":                 [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "if":                   [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "input":                [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "input#":               [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "instr":                [ 0,    0,    0,    1,    0,    0,    1,    1,    1    ],
        "int":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        # ------------------------------------------------------------------
        #                         AR    PP    V2    v3.5  v3.6  v4    v4+   v7    v10
        # ------------------------------------------------------------------
        "joy":                  [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "key":                  [ 0,    0,    0,    1,    1,    0,    1,    1,    1    ],
        "left$":                [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "len":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "let":                  [ 0,    0,    1,    0,    0,    0,    0,    0,    0    ],
        "list":                 [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "load":                 [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "locate":               [ 0,    0,    0,    1,    0,    0,    0,    1,    1    ],
        "log":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "loop":                 [ 0,    0,    0,    1,    0,    0,    0,    1,    1    ],
        "mid$":                 [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "monitor":              [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "movspr":               [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "new":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "next":                 [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "off":                  [ 0,    0,    0,    0,    0,    0,    0,    1,    0    ],
        "on":                   [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "open":                 [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "paint":                [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "peek":                 [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "pen":                  [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "pi":                   [ 0,    0,    0,    0,    1,    0,    0,    0,    0    ],
        "play":                 [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "pointer":              [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "poke":                 [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "popups":               [ 0,    0,    0,    0,    1,    0,    0,    0,    0    ],
        "pos":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "pot":                  [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "print":                [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "print#":               [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "printUsing":           [ 0,    0,    0,    1,    1,    0,    1,    1,    1    ],
        "pudef":                [ 0,    0,    0,    1,    1,    0,    1,    1,    1    ],
        "quit":                 [ 0,    0,    0,    0,    0,    0,    0,    1,    1    ],
        "rclr":                 [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "rdot":                 [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "read":                 [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "read#":                [ 0,    0,    0,    0,    0,    1,    1,    0,    0    ],
        "record":               [ 0,    0,    0,    0,    1,    1,    1,    1,    1    ],
        "rename":               [ 0,    0,    0,    1,    1,    1,    1,    1,    1    ],
        "renumber":             [ 0,    0,    0,    1,    1,    0,    0,    0,    1    ],
        "restore":              [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "resume":               [ 0,    0,    0,    1,    1,    0,    1,    1,    1    ],
        "return":               [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "rgr":                  [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        # ------------------------------------------------------------------
        #                         AR    PP    V2    v3.5  v3.6  v4    v4+   v7    v10
        # ------------------------------------------------------------------
        "right$":               [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "rlum":                 [ 0,    0,    0,    1,    0,    0,    0,    0,    0    ],
        "rnd":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "rreg":                 [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "rspcolor":             [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "rsppos":               [ 0,    0,    0,    0,    0,    0,    0,    1,    1    ],
        "rsprite":              [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "run":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "rwindow":              [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "save":                 [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "scale":                [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "scnclr":               [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "scratch":              [ 0,    0,    0,    1,    1,    1,    1,    1,    1    ],
        "sgn":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "sin":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "sleep":                [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "slow":                 [ 0,    0,    0,    0,    0,    0,    0,    1,    1    ],
        "sound":                [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "spc":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "sprcolor":             [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "sprdef":               [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "sprite":               [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "sprsav":               [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "sqr":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "sshape":               [ 0,    0,    0,    1,    0,    0,    0,    0,    1    ],
        "st":                   [ 0,    0,    1,    0,    1,    1,    1,    1,    1    ],
        "stash":                [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "status":               [ 0,    0,    1,    0,    0,    0,    0,    0,    0    ],
        "step":                 [ 0,    0,    1,    0,    1,    1,    1,    1,    1    ],
        "stop":                 [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "str$":                 [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "swap":                 [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "sys":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "tab":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "tan":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "tempo":                [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "then":                 [ 0,    0,    0,    0,    1,    1,    1,    1,    1    ],
        "ti":                   [ 0,    0,    1,    0,    1,    1,    0,    1,    1    ],
        "ti$":                  [ 0,    0,    1,    0,    1,    1,    1,    1,    1    ],
        "time":                 [ 0,    0,    1,    0,    0,    0,    0,    0,    0    ],
        "time$":                [ 0,    0,    1,    0,    0,    0,    0,    0,    0    ],
        "to":                   [ 0,    0,    1,    0,    1,    1,    1,    0,    1    ],
        "trap":                 [ 0,    0,    0,    1,    1,    0,    1,    1,    1    ],
        # ------------------------------------------------------------------
        #                         AR    PP    V2    v3.5  v3.6  v4    v4+   v7    v10
        # ------------------------------------------------------------------
        "troff":                [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "tron":                 [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "until":                [ 0,    0,    0,    1,    0,    0,    0,    0,    0    ],
        "user":                 [ 0,    0,    0,    0,    0,    1,    1,    0,    0    ],
        "using":                [ 0,    0,    0,    0,    0,    0,    1,    0,    0    ],
        "usr":                  [ 0,    0,    1,    1,    1,    0,    0,    1,    1    ],
        "val":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "verify":               [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "vol":                  [ 0,    0,    0,    1,    0,    0,    0,    1,    1    ],
        "volume":               [ 0,    0,    0,    0,    1,    0,    0,    0,    0    ],
        "wait":                 [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "while":                [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "width":                [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "window":               [ 0,    0,    0,    0,    0,    0,    0,    1,    1    ],
        "xor":                  [ 0,    0,    0,    0,    0,    0,    0,    1,    1    ],


        "piSign":               [ 0,    0,    1,    0,    0,    0,    0,    0,    0    ],

        "logicAnd":             [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "logicNot":             [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "logicOr":              [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],

        "arithmeticAdd":        [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "arithmeticMinus":      [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "arithmeticMul":        [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "arithmeticDiv":        [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "arithmeticExponent":   [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],

        "compareNeq":           [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "compareLessEqual":     [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "compareGraterEqual":   [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "compareLess":          [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "compareGreater":       [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],

        "curlyopen":            [ 0,    0,    0,    0,    0,    0,    0,    0,    0    ],
        "curlyclose":           [ 0,    0,    0,    0,    0,    0,    0,    0,    0    ],

        "roundopen":            [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "roundclose":           [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],

        "semicolon":            [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "colon":                [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        
        "eq":                   [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        
        "comma":                [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "identifier":           [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "whitespace":           [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ]

    }

    # Order is important
    parserTokens = {
        
        # 0 - default

        # 1 - comma

        # 2 - Assignment

        # 3 - Logical
        "logicAnd":           { "category": "led", "bindingpower": BindingPower.LOGICAL,       "type": TokenTypes.AND        },
        "logicOr":            { "category": "led", "bindingpower": BindingPower.LOGICAL,       "type": TokenTypes.OR         },
        "logicNot":           { "category": "led", "bindingpower": BindingPower.LOGICAL,       "type": TokenTypes.NOT        },

        # 4 - Relational
        "eq":                 { "category": "led", "bindingpower": BindingPower.RELATIONAL,    "type": TokenTypes.EQ         },
        "compareNeq":         { "category": "led", "bindingpower": BindingPower.RELATIONAL,    "type": TokenTypes.NEQ        },
        "compareLessEqual":   { "category": "led", "bindingpower": BindingPower.RELATIONAL,    "type": TokenTypes.LE         },
        "compareGraterEqual": { "category": "led", "bindingpower": BindingPower.RELATIONAL,    "type": TokenTypes.GE         },
        "compareLess":        { "category": "led", "bindingpower": BindingPower.RELATIONAL,    "type": TokenTypes.LESS       },
        "compareGreater":     { "category": "led", "bindingpower": BindingPower.RELATIONAL,    "type": TokenTypes.MORE       },

        # 5 - Additive
        "arithmeticAdd":      { "category": "led", "bindingpower": BindingPower.ADDITIVE,      "type" :TokenTypes.ADD        },
        "arithmeticMinus":    { "category": "led", "bindingpower": BindingPower.ADDITIVE,      "type": TokenTypes.MINUS      },

        # 6 - Multiplicative
        "arithmeticMul":      { "category": "led", "bindingpower": BindingPower.MULTIPLICATIVE, "type": TokenTypes.MUL       },
        "arithmeticDiv":      { "category": "led", "bindingpower": BindingPower.MULTIPLICATIVE, "type": TokenTypes.DIV       },
        "arithmeticExponent": { "category": "led", "bindingpower": BindingPower.MULTIPLICATIVE, "type": TokenTypes.EXPONENTIAL },

        # 7 - literals & symbols
        "literalScientific":  { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.SIENTIFIC  },
        "literalFloat":       { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.FLOAT      },
        "literalInt":         { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.INTEGER    },
        "literalString":      { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.STRING     },
        "identifier":         { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.IDENTIFIER },
        "lineNumber":         { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.LINENUMBER },
        "comment":            { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.COMMENT    },
        
        # 8 - unary & prefix
        "unary":              { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.MINUS      },

        # 9 - call 

        # 10 - member / computed & call

        # grouping expr


        "eof":                { "category": "nud", "bindingpower": 0,                           "type": TokenTypes.EOF        }
    }

    parserConfig = {
        # ------------------------------------------------------------------
        #                         AR    PP    V2    v3.5  v3.6  v4    v4+   v7    v10
        # ------------------------------------------------------------------
        "logicAnd":             [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "logicOr":              [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "logicNot":             [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "eq":                   [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "compareNeq":           [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "compareLessEqual":     [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "compareGraterEqual":   [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "compareLess":          [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "compareGreater":       [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "arithmeticAdd":        [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "arithmeticMinus":      [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "arithmeticMul":        [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "arithmeticDiv":        [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "arithmeticExponent":   [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "eof":                  [ 1,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "literalScientific":    [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "literalFloat":         [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "literalInt":           [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "literalString":        [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "identifier":           [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "lineNumber":           [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "comment":              [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "unary":                [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ]
    }

    def getLexerToken(self, token):
        return LexerConfigToken(
                            token["type"],
                            token["expression"],
                            token["order"]
                        )
    
    def getLexerConfig(self, index):
        result = LexerConfig()
        for key in Config.lexerConfig.keys():
            if Config.lexerConfig[key][index] == 1:
                result.tokens.append(self.getLexerToken(self.lexerTokens[key]))

        result.tokens = sorted(result.tokens, key=attrgetter('order'))
        return result
    
    def getParserToken(self, token):
        return ParserConfigToken(
                        token["bindingpower"],
                        token["type"],
                        token["category"],
                    )

    def getParserConfig(self,index):
        result = ParserConfig()

        for key in Config.parserConfig.keys():
            if Config.parserConfig[key][index] == 1:
                result.tokens.append(self.getParserToken(self.parserTokens[key]))

        result.tokens = sorted(result.tokens, key=attrgetter('bindingpower'))
        
        return result
