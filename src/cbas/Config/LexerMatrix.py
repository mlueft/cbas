import cbas.Lexer.TokenTypes
import cbas.Lexer.Lexer

TokenTypes = cbas.Lexer.TokenTypes.TokenTypes
Tokenizer  = cbas.Lexer.Lexer.Tokenizer

class LexerMatrix():

    Parameters = [
        # AR    PP    V2    v3.5  v3.6  v4    v4+   v7    v10
        {
            "name": "",
            "description":"",
            "markLinestart":False,
            "markLineend": False,
            "markEOF":True
        },
        # PP    V2    v3.5  v3.6  v4    v4+   v7    v10
        {
            "name": "",
            "description":"",
            "markLinestart":False,
            "markLineend": True,
            "markEOF":False
        },
        # V2    v3.5  v3.6  v4    v4+   v7    v10
        {
            "name": "",
            "description":"",
            "markLinestart":False,
            "markLineend": True,
            "markEOF":True
        },
        # v3.5  v3.6  v4    v4+   v7    v10
        {
            "name": "",
            "description":"",
            "markLinestart":False,
            "markLineend": True,
            "markEOF":True
        },
        # v3.6  v4    v4+   v7    v10
        {
            "name": "",
            "description":"",
            "markLinestart":False,
            "markLineend": True,
            "markEOF":True
        },
        # v4    v4+   v7    v10
        {
            "name": "",
            "description":"",
            "markLinestart":False,
            "markLineend": True,
            "markEOF":True
        },
        # v4+   v7    v10
        {
            "name": "",
            "description":"",
            "markLinestart":False,
            "markLineend": True,
            "markEOF":True
        },
        # v7    v10
        {
            "name": "",
            "description":"",
            "markLinestart":False,
            "markLineend": True,
            "markEOF":True
        },
        # v10
        {
            "name": "",
            "description":"",
            "markLinestart":False,
            "markLineend": True,
            "markEOF":True
        },
        
    ]

    Tokens = {

        "lineNumber":           { "order":    0, "handler": Tokenizer.defaultHandler , "type": TokenTypes.LINENUMBER,  "expression": "^[0-9]+" },
        "literalSientific":     { "order":   10, "handler": Tokenizer.defaultHandler , "type": TokenTypes.SIENTIFIC,   "expression": "(?i)-?[0-9]+[.]?[0-9]*e-*[0-9]+[.]?[0-9]*" },
        "literalFloat":         { "order":   20, "handler": Tokenizer.defaultHandler , "type": TokenTypes.FLOAT,       "expression": "[0-9]+[.][0-9]*" },
        "literalInt":           { "order":   40, "handler": Tokenizer.defaultHandler , "type": TokenTypes.INTEGER,     "expression": "[0-9]+[%]?" },
        "literalBoolean":       { "order":   41, "handler": Tokenizer.defaultHandler , "type": TokenTypes.BOOLEAN,     "expression": "(?i)(true|false)" },
        "literalString":        { "order":   50, "handler": Tokenizer.stringHandler  , "type": TokenTypes.STRING,      "expression": '(?i)"[^"]*"' },
        "comment":              { "order":  100, "handler": Tokenizer.defaultHandler , "type": TokenTypes.COMMENT,     "expression": "(?i)rem.*" }, # s $8F
        "printUsing":           { "order":  110, "handler": Tokenizer.defaultHandler , "type": TokenTypes.PRINTUSING,  "expression": "(?i)PRINT USING" },
        "collision":            { "order":  120, "handler": Tokenizer.defaultHandler , "type": TokenTypes.COLLISION,   "expression": "(?i)COLLISION" }, # s $fe $17
        "directory":            { "order":  130, "handler": Tokenizer.defaultHandler , "type": TokenTypes.DIRECTORY,   "expression": "(?i)DIRECTORY" }, # s v4 $DA v34 v7 $EE
        "envelope":             { "order":  140, "handler": Tokenizer.defaultHandler , "type": TokenTypes.ENVELOPE,    "expression": "(?i)ENVELOPE" },
        "renumber":             { "order":  150, "handler": Tokenizer.defaultHandler , "type": TokenTypes.RENUMBER,    "expression": "(?i)RENUMBER" }, # s $F8
        "rspcolor":             { "order":  160, "handler": Tokenizer.defaultHandler , "type": TokenTypes.RSPCOLOR,    "expression": "(?i)RSPCOLOR" }, # f $ce $07
        "sprcolor":             { "order":  170, "handler": Tokenizer.defaultHandler , "type": TokenTypes.SPRCOLOR,    "expression": "(?i)SPRCOLOR" }, # s $fe $08
        "catalog":              { "order":  180, "handler": Tokenizer.defaultHandler , "type": TokenTypes.CATALOG,     "expression": "(?i)CATALOG" }, # s v4 $D7 v7 $OC
        "collect":              { "order":  190, "handler": Tokenizer.defaultHandler , "type": TokenTypes.COLLECT,     "expression": "(?i)COLLECT" }, # s v4 $D1 v35 v7 $F3
        "dispose":              { "order":  200, "handler": Tokenizer.defaultHandler , "type": TokenTypes.DISPOSE,     "expression": "(?i)DISPOSE" },
        "dverify":              { "order":  210, "handler": Tokenizer.defaultHandler , "type": TokenTypes.DVERIFY,     "expression": "(?i)DVERIFY" },
        "graphic":              { "order":  220, "handler": Tokenizer.defaultHandler , "type": TokenTypes.GRAPHIC,     "expression": "(?i)GRAPHIC" }, # s $de
        "monitor":              { "order":  230, "handler": Tokenizer.defaultHandler , "type": TokenTypes.MONITOR,     "expression": "(?i)MONITOR" }, # s $fa
        "pointer":              { "order":  240, "handler": Tokenizer.defaultHandler , "type": TokenTypes.POINTER,     "expression": "(?i)POINTER" },
        "rsprite":              { "order":  250, "handler": Tokenizer.defaultHandler , "type": TokenTypes.RSSPRITE,    "expression": "(?i)RSPRITE" }, # f $ce $06
        "rwindow":              { "order":  260, "handler": Tokenizer.defaultHandler , "type": TokenTypes.RWINDOW,     "expression": "(?i)RWINDOW" },
        "scratch":              { "order":  270, "handler": Tokenizer.defaultHandler , "type": TokenTypes.SCRATCH,     "expression": "(?i)SCRATCH" }, # s v4 $D9 v35 v7 $F2
        "restore":              { "order":  280, "handler": Tokenizer.defaultHandler , "type": TokenTypes.RESTORE,     "expression": "(?i)RESTORE" }, # s $8C
        "right_dollar":         { "order":  290, "handler": Tokenizer.defaultHandler , "type": TokenTypes.RIGHT_DOLLAR,"expression": "(?i)RIGHT\$" }, # f $C9
        "time_dollar":          { "order":  300, "handler": Tokenizer.defaultHandler , "type": TokenTypes.TIME_DOLLAR, "expression": "(?i)TIME\$" }, # s
        "quit":                 { "order":  310, "handler": Tokenizer.defaultHandler , "type": TokenTypes.QUIT,        "expression": "(?i)(QUIT)" }, # s $fe $1e
        "append":               { "order":  320, "handler": Tokenizer.defaultHandler , "type": TokenTypes.APPEND,      "expression": "(?i)APPEND" }, # s v4 $D4 v7 $FE $OE
        "backup":               { "order":  330, "handler": Tokenizer.defaultHandler , "type": TokenTypes.BACKUP,      "expression": "(?i)BACKUP" }, # s V4 $D2 V35 7 $F6
        "circle":               { "order":  340, "handler": Tokenizer.defaultHandler , "type": TokenTypes.CIRCLE,      "expression": "(?i)CIRCLE" }, # s 
        "concat":               { "order":  350, "handler": Tokenizer.defaultHandler , "type": TokenTypes.CONCAT,      "expression": "(?i)CONCAT" },
        "dclear":               { "order":  360, "handler": Tokenizer.defaultHandler , "type": TokenTypes.DECLARE,     "expression": "(?i)DCLEAR" },
        "dclose":               { "order":  370, "handler": Tokenizer.defaultHandler , "type": TokenTypes.DCLOSE,      "expression": "(?i)DCLOSE" },
        "def_fn":               { "order":  380, "handler": Tokenizer.defaultHandler , "type": TokenTypes.DEF_FN,      "expression": "(?i)DEF FN" },
        "delete":               { "order":  390, "handler": Tokenizer.defaultHandler , "type": TokenTypes.DELETE,      "expression": "(?i)DELETE" }, # s $F7
        "filter":               { "order":  400, "handler": Tokenizer.defaultHandler , "type": TokenTypes.FILTER,      "expression": "(?i)FILTER" },
        "getkey":               { "order":  410, "handler": Tokenizer.defaultHandler , "type": TokenTypes.GETKEY,      "expression": "(?i)GETKEY" },
        "gshape":               { "order":  420, "handler": Tokenizer.defaultHandler , "type": TokenTypes.GSHAPE,      "expression": "(?i)GSHAPE" }, # s $e3
        "header":               { "order":  430, "handler": Tokenizer.defaultHandler , "type": TokenTypes.HEADER,      "expression": "(?i)HEADER" }, # s v4 $D0 v35 v7 $F1
        "hex_dollar":           { "order":  440, "handler": Tokenizer.defaultHandler , "type": TokenTypes.HEX_DOLLAR,  "expression": "(?i)HEX\$"  }, # f
        "locate":               { "order":  450, "handler": Tokenizer.defaultHandler , "type": TokenTypes.LOCATE,      "expression": "(?i)LOCATE" },
        "movspr":               { "order":  460, "handler": Tokenizer.defaultHandler , "type": TokenTypes.MOVSPR,      "expression": "(?i)MOVSPR" }, # s $fe $06
        "record":               { "order":  470, "handler": Tokenizer.defaultHandler , "type": TokenTypes.RECORD,      "expression": "(?i)RECORD" }, # s v4 $CF v7 $FE $12
        "rename":               { "order":  480, "handler": Tokenizer.defaultHandler , "type": TokenTypes.RENAME,      "expression": "(?i)RENAME" },
        "resume":               { "order":  490, "handler": Tokenizer.defaultHandler , "type": TokenTypes.RESUME,      "expression": "(?i)RESUME" }, # s $d6
        "rsppos":               { "order":  500, "handler": Tokenizer.defaultHandler , "type": TokenTypes.RSPPOS,      "expression": "(?i)RSPPOS" }, # f $ce $05
        "scnclr":               { "order":  510, "handler": Tokenizer.defaultHandler , "type": TokenTypes.SCNCLR,      "expression": "(?i)SCNCLR" }, # s $e8
        "sprdef":               { "order":  520, "handler": Tokenizer.defaultHandler , "type": TokenTypes.SPRDEF,      "expression": "(?i)SPRDEF" }, # s $fe $1d
        "sprite":               { "order":  530, "handler": Tokenizer.defaultHandler , "type": TokenTypes.SPRITE,      "expression": "(?i)SPRITE" }, # s $fe $07
        "sprsav":               { "order":  540, "handler": Tokenizer.defaultHandler , "type": TokenTypes.SPRSAV,      "expression": "(?i)SPRSAV" }, # s $fe $16
        "sshape":               { "order":  550, "handler": Tokenizer.defaultHandler , "type": TokenTypes.SSHAPE,      "expression": "(?i)SSHAPE" }, # s $e4
        "window":               { "order":  560, "handler": Tokenizer.defaultHandler , "type": TokenTypes.WINDOW,      "expression": "(?i)WINDOW" },
        "popups":               { "order":  570, "handler": Tokenizer.defaultHandler , "type": TokenTypes.POPUPS,      "expression": "(?i)POPUPS" },
        "volume":               { "order":  580, "handler": Tokenizer.defaultHandler , "type": TokenTypes.VOLUME,      "expression": "(?i)VOLUME" },
        "status":               { "order":  590, "handler": Tokenizer.defaultHandler , "type": TokenTypes.STATUS,      "expression": "(?i)STATUS" }, # s
        "return":               { "order":  600, "handler": Tokenizer.defaultHandler , "type": TokenTypes.RETURN,      "expression": "(?i)RETURN" }, # s $8E
        "verify":               { "order":  610, "handler": Tokenizer.defaultHandler , "type": TokenTypes.VERIFY,      "expression": "(?i)VERIFY" }, # s
        "input_sharp":          { "order":  620, "handler": Tokenizer.defaultHandler , "type": TokenTypes.INPUT_SHARP, "expression": "(?i)INPUT#" }, # s $84
        "print_sharp":          { "order":  630, "handler": Tokenizer.defaultHandler , "type": TokenTypes.PRINT_SHARP, "expression": "(?i)PRINT#" }, # s $98
        "left_dollar":          { "order":  640, "handler": Tokenizer.defaultHandler , "type": TokenTypes.LEFT_DOLLAR, "expression": "(?i)LEFT\$" }, # f $C8
        "pudef":                { "order":  650, "handler": Tokenizer.defaultHandler , "type": TokenTypes.PUDEF,       "expression": "(?i)PUDEF" },
        "off":                  { "order":  660, "handler": Tokenizer.defaultHandler , "type": TokenTypes.OFF,         "expression": "(?i)(OFF)" }, # s $fe $24
        "bload":                { "order":  670, "handler": Tokenizer.defaultHandler , "type": TokenTypes.BLOAD,       "expression": "(?i)BLOAD" }, # s $FE $0B 
        "bsave":                { "order":  680, "handler": Tokenizer.defaultHandler , "type": TokenTypes.BSAVE,       "expression": "(?i)BSAVE" }, # s $FE $10
        "dload":                { "order":  690, "handler": Tokenizer.defaultHandler , "type": TokenTypes.DLOAD,       "expression": "(?i)DLOAD" }, # s v4 $D6 v35 v7 $F0
        "dopen":                { "order":  700, "handler": Tokenizer.defaultHandler , "type": TokenTypes.DOPEN,       "expression": "(?i)DOPEN" },
        "ds_dollar":            { "order":  710, "handler": Tokenizer.defaultHandler , "type": TokenTypes.DS_DOLLAR,   "expression": "(?i)DS\$"  }, # s
        "dsave":                { "order":  720, "handler": Tokenizer.defaultHandler , "type": TokenTypes.DSAVE,       "expression": "(?i)DSAVE" }, # s v4 $D5 v35 v7 $EF
        "fetch":                { "order":  730, "handler": Tokenizer.defaultHandler , "type": TokenTypes.FETCH,       "expression": "(?i)FETCH" },
        "instr":                { "order":  740, "handler": Tokenizer.defaultHandler , "type": TokenTypes.INSTR,       "expression": "(?i)INSTR" }, # f $d4
        "paint":                { "order":  750, "handler": Tokenizer.defaultHandler , "type": TokenTypes.PAINT,       "expression": "(?i)PAINT" },
        "read_sharp":           { "order":  760, "handler": Tokenizer.defaultHandler , "type": TokenTypes.READ_SHARP,  "expression": "(?i)READ#" },
        "scale":                { "order":  770, "handler": Tokenizer.defaultHandler , "type": TokenTypes.SCALE,       "expression": "(?i)SCALE" },
        "sleep":                { "order":  780, "handler": Tokenizer.defaultHandler , "type": TokenTypes.SLEEP,       "expression": "(?i)SLEEP" }, # s $FE $0B
        "sound":                { "order":  790, "handler": Tokenizer.defaultHandler , "type": TokenTypes.SOUND,       "expression": "(?i)SOUND" },
        "stash":                { "order":  800, "handler": Tokenizer.defaultHandler , "type": TokenTypes.STASH,       "expression": "(?i)STASH" },
        "tempo":                { "order":  810, "handler": Tokenizer.defaultHandler , "type": TokenTypes.TEMPO,       "expression": "(?i)TEMPO" },
        "troff":                { "order":  820, "handler": Tokenizer.defaultHandler , "type": TokenTypes.TROFF,       "expression": "(?i)TROFF" },
        "using":                { "order":  830, "handler": Tokenizer.defaultHandler , "type": TokenTypes.USING,       "expression": "(?i)USING" },
        "while":                { "order":  840, "handler": Tokenizer.defaultHandler , "type": TokenTypes.WHILE,       "expression": "(?i)WHILE" },
        "width":                { "order":  850, "handler": Tokenizer.defaultHandler , "type": TokenTypes.WIDTH,       "expression": "(?i)WIDTH" }, # s $fe $1c
        "until":                { "order":  860, "handler": Tokenizer.defaultHandler , "type": TokenTypes.UNTIL,       "expression": "(?i)UNTIL" },
        "print":                { "order":  870, "handler": Tokenizer.defaultHandler , "type": TokenTypes.PRINT,       "expression": "(?i)PRINT" }, # s $99
        "gosub":                { "order":  880, "handler": Tokenizer.defaultHandler , "type": TokenTypes.GOSUB,       "expression": "(?i)GOSUB" }, # s $8D
        "input":                { "order":  890, "handler": Tokenizer.defaultHandler , "type": TokenTypes.INPUT,       "expression": "(?i)INPUT" }, # s $85
        "close":                { "order":  900, "handler": Tokenizer.defaultHandler , "type": TokenTypes.CLOSE,       "expression": "(?i)CLOSE" }, # s $A0
        "chr_dollar":           { "order":  910, "handler": Tokenizer.defaultHandler , "type": TokenTypes.CHR_DOLLAR,  "expression": "(?i)CHR\$" }, # f  $C7
        "mid_dollar":           { "order":  920, "handler": Tokenizer.defaultHandler , "type": TokenTypes.MID_DOLLAR,  "expression": "(?i)MID\$" }, # f $CA
        "str_dollar":           { "order":  930, "handler": Tokenizer.defaultHandler , "type": TokenTypes.STR_DOLLAR,  "expression": "(?i)STR\$" }, # f $C4
        "err_dollar":           { "order":  940, "handler": Tokenizer.defaultHandler , "type": TokenTypes.ERR_DOLLAR,  "expression": "(?i)ERR\$" }, # f $d3
        "color":                { "order":  950, "handler": Tokenizer.defaultHandler , "type": TokenTypes.COLOR,       "expression": "(?i)COLOR" }, # s
        "begin":                { "order":  960, "handler": Tokenizer.defaultHandler , "type": TokenTypes.BEGIN,       "expression": "(?i)BEGIN" }, # s $FE $18
        "auto":                 { "order":  970, "handler": Tokenizer.defaultHandler , "type": TokenTypes.AUTO,        "expression": "(?i)AUTO" }, # s $DC
        "bank":                 { "order":  980, "handler": Tokenizer.defaultHandler , "type": TokenTypes.BANK,        "expression": "(?i)BANK" }, # s $FE $02
        "pisign":               { "order":  990, "handler": Tokenizer.defaultHandler , "type": TokenTypes.PISIGN,      "expression": "(?i)π" },
        "bend":                 { "order": 1000, "handler": Tokenizer.defaultHandler , "type": TokenTypes.BEND,        "expression": "(?i)BEND" }, # s $FE $19
        "boot":                 { "order": 1010, "handler": Tokenizer.defaultHandler , "type": TokenTypes.BOOT,        "expression": "(?i)BOOT" }, # s $FE $1B
        "bump":                 { "order": 1020, "handler": Tokenizer.defaultHandler , "type": TokenTypes.BUMP,        "expression": "(?i)BUMP" }, # s $CE $03
        "char":                 { "order": 1030, "handler": Tokenizer.defaultHandler , "type": TokenTypes.CHAR,        "expression": "(?i)CHAR" }, # s $E0
        "copy":                 { "order": 1040, "handler": Tokenizer.defaultHandler , "type": TokenTypes.COPY,        "expression": "(?i)COPY" }, # s v4 $D3 v35 v7 $F4
        "draw":                 { "order": 1050, "handler": Tokenizer.defaultHandler , "type": TokenTypes.DRAW,        "expression": "(?i)DRAW" }, # s
        "else":                 { "order": 1060, "handler": Tokenizer.defaultHandler , "type": TokenTypes.ELSE,        "expression": "(?i)ELSE" }, # s $d5
        "exit":                 { "order": 1070, "handler": Tokenizer.defaultHandler , "type": TokenTypes.EXIT,        "expression": "(?i)EXIT" }, # s $ed
        "fast":                 { "order": 1080, "handler": Tokenizer.defaultHandler , "type": TokenTypes.FAST,        "expression": "(?i)FAST" }, # s $fe $25
        "go64":                 { "order": 1090, "handler": Tokenizer.defaultHandler , "type": TokenTypes.GO64,        "expression": "(?i)GO64" }, # s $CB
        "help":                 { "order": 1100, "handler": Tokenizer.defaultHandler , "type": TokenTypes.HELP,        "expression": "(?i)HELP" }, # s
        "loop":                 { "order": 1110, "handler": Tokenizer.defaultHandler , "type": TokenTypes.LOOP,        "expression": "(?i)LOOP" },
        "play":                 { "order": 1120, "handler": Tokenizer.defaultHandler , "type": TokenTypes.PLAY,        "expression": "(?i)PLAY" },
        "rclr":                 { "order": 1130, "handler": Tokenizer.defaultHandler , "type": TokenTypes.RCLR,        "expression": "(?i)RCLR" },
        "rdot":                 { "order": 1140, "handler": Tokenizer.defaultHandler , "type": TokenTypes.RDOT,        "expression": "(?i)RDOT" }, # f $d0
        "rreg":                 { "order": 1150, "handler": Tokenizer.defaultHandler , "type": TokenTypes.RREG,        "expression": "(?i)RREG" },
        "step":                 { "order": 1160, "handler": Tokenizer.defaultHandler , "type": TokenTypes.STEP,        "expression": "(?i)STEP" }, # s $A9
        "swap":                 { "order": 1170, "handler": Tokenizer.defaultHandler , "type": TokenTypes.SWAP,        "expression": "(?i)SWAP" },
        "then":                 { "order": 1180, "handler": Tokenizer.defaultHandler , "type": TokenTypes.THEN,        "expression": "(?i)THEN" }, # s $A7
        "trap":                 { "order": 1190, "handler": Tokenizer.defaultHandler , "type": TokenTypes.TRAP,        "expression": "(?i)TRAP" }, # s $D7
        "tron":                 { "order": 1200, "handler": Tokenizer.defaultHandler , "type": TokenTypes.TRON,        "expression": "(?i)TRON" },
        "user":                 { "order": 1210, "handler": Tokenizer.defaultHandler , "type": TokenTypes.USER,        "expression": "(?i)USER" },
        "rlum":                 { "order": 1220, "handler": Tokenizer.defaultHandler , "type": TokenTypes.RLUM,        "expression": "(?i)RLUM" },
        "time":                 { "order": 1230, "handler": Tokenizer.defaultHandler , "type": TokenTypes.TIME,        "expression": "(?i)TIME" }, # s
        "goto":                 { "order": 1260, "handler": Tokenizer.defaultHandler , "type": TokenTypes.GOTO,        "expression": "(?i)GO[\\s]*TO" }, # s $89
        "go_to":                { "order": 1261, "handler": Tokenizer.defaultHandler , "type": TokenTypes.GOTO,        "expression": "(?i)GO TO" }, # s $89
        "read":                 { "order": 1270, "handler": Tokenizer.defaultHandler , "type": TokenTypes.READ,        "expression": "(?i)READ" }, # s $87
        "open":                 { "order": 1280, "handler": Tokenizer.defaultHandler , "type": TokenTypes.OPEN,        "expression": "(?i)OPEN" }, # s 9F
        "peek":                 { "order": 1290, "handler": Tokenizer.defaultHandler , "type": TokenTypes.PEEK,        "expression": "(?i)PEEK" }, # f $C2
        "poke":                 { "order": 1300, "handler": Tokenizer.defaultHandler , "type": TokenTypes.POKE,        "expression": "(?i)POKE" }, # s $97
        "list":                 { "order": 1310, "handler": Tokenizer.defaultHandler , "type": TokenTypes.LIST,        "expression": "(?i)LIST" }, # s $9B
        "load":                 { "order": 1320, "handler": Tokenizer.defaultHandler , "type": TokenTypes.LOAD,        "expression": "(?i)LOAD" }, # s $93
        "next":                 { "order": 1330, "handler": Tokenizer.defaultHandler , "type": TokenTypes.NEXT,        "expression": "(?i)NEXT" }, # s $82
        "save":                 { "order": 1340, "handler": Tokenizer.defaultHandler , "type": TokenTypes.SAVE,        "expression": "(?i)SAVE" }, # s $94
        "stop":                 { "order": 1350, "handler": Tokenizer.defaultHandler , "type": TokenTypes.STOP,        "expression": "(?i)STOP" }, # s $90
        "data":                 { "order": 1360, "handler": Tokenizer.defaultHandler , "type": TokenTypes.DATA,        "expression": "(?i)DATA" }, # s $83
        "slow":                 { "order": 1370, "handler": Tokenizer.defaultHandler , "type": TokenTypes.SLOW,        "expression": "(?i)SLOW" }, # s $fe $26
        "wait":                 { "order": 1380, "handler": Tokenizer.defaultHandler , "type": TokenTypes.WAIT,        "expression": "(?i)WAIT" }, # s $92
        "cont":                 { "order": 1390, "handler": Tokenizer.defaultHandler , "type": TokenTypes.CONT,        "expression": "(?i)CONT" }, # s $9A
        "get_sharp":            { "order": 1400, "handler": Tokenizer.defaultHandler , "type": TokenTypes.GET_SHARP,   "expression": "(?i)GET#" }, # s $a1 $23
        "get":                  { "order": 1410, "handler": Tokenizer.defaultHandler , "type": TokenTypes.GET,         "expression": "(?i)GET" }, # s $A1
        "box":                  { "order": 1420, "handler": Tokenizer.defaultHandler , "type": TokenTypes.BOX,         "expression": "(?i)BOX" }, # s $DC
        "dec":                  { "order": 1430, "handler": Tokenizer.defaultHandler , "type": TokenTypes.DEC,         "expression": "(?i)DEC" }, # f $D1
        "def":                  { "order": 1440, "handler": Tokenizer.defaultHandler , "type": TokenTypes.DEF,         "expression": "(?i)DEF" }, # s $96
        "end":                  { "order": 1450, "handler": Tokenizer.defaultHandler , "type": TokenTypes.END,         "expression": "(?i)END" }, # s $80
        "esc":                  { "order": 1460, "handler": Tokenizer.defaultHandler , "type": TokenTypes.ESC,         "expression": "(?i)ESC" },
        "joy":                  { "order": 1470, "handler": Tokenizer.defaultHandler , "type": TokenTypes.JOY,         "expression": "(?i)JOY" }, # f $CF
        "key":                  { "order": 1480, "handler": Tokenizer.defaultHandler , "type": TokenTypes.KEY,         "expression": "(?i)KEY" },
        "pen":                  { "order": 1490, "handler": Tokenizer.defaultHandler , "type": TokenTypes.PEN,         "expression": "(?i)PEN" }, # f $CE $04
        "pot":                  { "order": 1500, "handler": Tokenizer.defaultHandler , "type": TokenTypes.POT,         "expression": "(?i)POT" }, # f $CE $02
        "rgr":                  { "order": 1510, "handler": Tokenizer.defaultHandler , "type": TokenTypes.RGR,         "expression": "(?i)RGR" },
        "vol":                  { "order": 1520, "handler": Tokenizer.defaultHandler , "type": TokenTypes.VOL,         "expression": "(?i)VOL" },
        "xor":                  { "order": 1530, "handler": Tokenizer.defaultHandler , "type": TokenTypes.XOR,         "expression": "(?i)XOR" },
        "usr":                  { "order": 1540, "handler": Tokenizer.defaultHandler , "type": TokenTypes.USR,         "expression": "(?i)USR" }, # f $B7
        "def":                  { "order": 1550, "handler": Tokenizer.defaultHandler , "type": TokenTypes.DEF,         "expression": "(?i)DEF" },
        "end":                  { "order": 1560, "handler": Tokenizer.defaultHandler , "type": TokenTypes.END,         "expression": "(?i)END" },
        "let":                  { "order": 1570, "handler": Tokenizer.ignoreHandler  , "type": TokenTypes.LET,         "expression": "(?i)LET" }, # s $88
        "abs":                  { "order": 1580, "handler": Tokenizer.defaultHandler , "type": TokenTypes.ABS,         "expression": "(?i)ABS" }, # f $B6
        "asc":                  { "order": 1590, "handler": Tokenizer.defaultHandler , "type": TokenTypes.ASC,         "expression": "(?i)ASC" }, # f $C6
        "atn":                  { "order": 1600, "handler": Tokenizer.defaultHandler , "type": TokenTypes.ATN,         "expression": "(?i)ATN" }, # f $C1
        "clr":                  { "order": 1610, "handler": Tokenizer.defaultHandler , "type": TokenTypes.CLR,         "expression": "(?i)CLR" }, # s $9C
        "cmd":                  { "order": 1620, "handler": Tokenizer.defaultHandler , "type": TokenTypes.CMD,         "expression": "(?i)CMD" }, # ?
        "int":                  { "order": 1630, "handler": Tokenizer.defaultHandler , "type": TokenTypes.INT,         "expression": "(?i)INT" }, # f $B5
        "cos":                  { "order": 1640, "handler": Tokenizer.defaultHandler , "type": TokenTypes.COS,         "expression": "(?i)COS" }, # f $BE 
        "exp":                  { "order": 1650, "handler": Tokenizer.defaultHandler , "type": TokenTypes.EXP,         "expression": "(?i)EXP" }, # s $BD
        "for":                  { "order": 1660, "handler": Tokenizer.defaultHandler , "type": TokenTypes.FOR,         "expression": "(?i)FOR" }, # s $81
        "fre":                  { "order": 1670, "handler": Tokenizer.defaultHandler , "type": TokenTypes.FRE,         "expression": "(?i)FRE" }, # f $B8
        "len":                  { "order": 1680, "handler": Tokenizer.defaultHandler , "type": TokenTypes.LEN,         "expression": "(?i)LEN" }, # f $C3
        "log":                  { "order": 1690, "handler": Tokenizer.defaultHandler , "type": TokenTypes.LOG,         "expression": "(?i)LOG" }, # f $BC
        "new":                  { "order": 1700, "handler": Tokenizer.defaultHandler , "type": TokenTypes.NEW,         "expression": "(?i)NEW" }, # s $A2
        "pos":                  { "order": 1710, "handler": Tokenizer.defaultHandler , "type": TokenTypes.POS,         "expression": "(?i)POS" }, # f $B9
        "rnd":                  { "order": 1730, "handler": Tokenizer.defaultHandler , "type": TokenTypes.RND,         "expression": "(?i)RND" }, # f $BB
        "run":                  { "order": 1740, "handler": Tokenizer.defaultHandler , "type": TokenTypes.RUN,         "expression": "(?i)RUN" }, # s
        "sgn":                  { "order": 1750, "handler": Tokenizer.defaultHandler , "type": TokenTypes.SGN,         "expression": "(?i)SGN" }, # f $B4
        "sin":                  { "order": 1760, "handler": Tokenizer.defaultHandler , "type": TokenTypes.SIN,         "expression": "(?i)SIN" }, # f $BF
        "spc":                  { "order": 1770, "handler": Tokenizer.defaultHandler , "type": TokenTypes.SPC,         "expression": "(?i)SPC" }, # f $A6
        "sqr":                  { "order": 1780, "handler": Tokenizer.defaultHandler , "type": TokenTypes.RESUME,      "expression": "(?i)RESUME" }, # s $d6
        "rsppos":               { "order":  500, "handler": Tokenizer.defaultHandler , "type": TokenTypes.RSPPOS,      "expression": "(?i)RSPPOS" }, # f $ce $05
        "scnclr":               { "order":  510, "handler": Tokenizer.defaultHandler , "type": TokenTypes.SCNCLR,      "expression": "(?i)SCNCLR" }, # s $e8
        "sprdef":               { "order":  520, "handler": Tokenizer.defaultHandler , "type": TokenTypes.SQR,         "expression": "(?i)SQR" }, # f $BA
        "sys":                  { "order": 1790, "handler": Tokenizer.defaultHandler , "type": TokenTypes.SYS,         "expression": "(?i)SYS" }, # s $9E
        "tab":                  { "order": 1800, "handler": Tokenizer.defaultHandler , "type": TokenTypes.TAB,         "expression": "(?i)TAB" }, # f $A3
        "tan":                  { "order": 1810, "handler": Tokenizer.defaultHandler , "type": TokenTypes.TAN,         "expression": "(?i)TAN" }, # f $C0
        "val":                  { "order": 1820, "handler": Tokenizer.defaultHandler , "type": TokenTypes.VAL,         "expression": "(?i)VAL" }, # f $C5
        "dim":                  { "order": 1830, "handler": Tokenizer.defaultHandler , "type": TokenTypes.DIM,         "expression": "(?i)DIM" }, # s $86
        "logicAnd":             { "order": 1840, "handler": Tokenizer.defaultHandler , "type": TokenTypes.AND,         "expression": "(?i)AND" }, # s $AF
        "logicNot":             { "order": 1850, "handler": Tokenizer.defaultHandler , "type": TokenTypes.NOT,         "expression": "(?i)NOT" }, # s $A8
        "ti_dollar":            { "order": 1870, "handler": Tokenizer.defaultHandler , "type": TokenTypes.TI_DOLLAR,   "expression": "(?i)TI\$" },
        "ti":                   { "order": 1880, "handler": Tokenizer.defaultHandler , "type": TokenTypes.TI,          "expression": "(?i)TI" },
        "to":                   { "order": 1890, "handler": Tokenizer.defaultHandler , "type": TokenTypes.TO,          "expression": "(?i)TO" }, # s $A4
        "fn":                   { "order": 1900, "handler": Tokenizer.defaultHandler , "type": TokenTypes.FN,          "expression": "(?i)FN" }, # s
        "do":                   { "order": 1910, "handler": Tokenizer.defaultHandler , "type": TokenTypes.DO,          "expression": "(?i)DO" }, # s
        "ds":                   { "order": 1920, "handler": Tokenizer.defaultHandler , "type": TokenTypes.DS,          "expression": "(?i)DS" }, # s
        "el":                   { "order": 1930, "handler": Tokenizer.defaultHandler , "type": TokenTypes.EL,          "expression": "(?i)EL" }, # s
        "er":                   { "order": 1940, "handler": Tokenizer.defaultHandler , "type": TokenTypes.ER,          "expression": "(?i)ER" }, # s
        "go":                   { "order": 1950, "handler": Tokenizer.defaultHandler , "type": TokenTypes.GO,          "expression": "(?i)GO" }, # s $CB
        "st":                   { "order": 1960, "handler": Tokenizer.defaultHandler , "type": TokenTypes.ST,          "expression": "(?i)ST" },
        "pi":                   { "order": 1970, "handler": Tokenizer.defaultHandler , "type": TokenTypes.PI,          "expression": "(?i)PI" }, # s $FF
        "if":                   { "order": 2000, "handler": Tokenizer.defaultHandler , "type": TokenTypes.IF,          "expression": "(?i)IF" }, # s $8B
        "on":                   { "order": 2010, "handler": Tokenizer.defaultHandler , "type": TokenTypes.ON,          "expression": "(?i)ON" }, # s $91
        "logicOr":              { "order": 2020, "handler": Tokenizer.defaultHandler , "type": TokenTypes.OR,          "expression": "(?i)OR" }, # s $B0
        "arithmeticAdd":        { "order": 3000, "handler": Tokenizer.defaultHandler , "type": TokenTypes.ADD,         "expression": "(?i)\\+" },
        "arithmeticMinus":      { "order": 3010, "handler": Tokenizer.defaultHandler , "type": TokenTypes.MINUS,       "expression": "(?i)\\-" },
        "arithmeticMul":        { "order": 3020, "handler": Tokenizer.defaultHandler , "type": TokenTypes.MUL,         "expression": "(?i)\\*" },
        "arithmeticDiv":        { "order": 3030, "handler": Tokenizer.defaultHandler , "type": TokenTypes.DIV,         "expression": "(?i)\\/" },
        "arithmeticExponent":   { "order": 3040, "handler": Tokenizer.defaultHandler , "type": TokenTypes.EXPONENTIAL, "expression": "(?i)\\^" },
        "compareNeq":           { "order": 3050, "handler": Tokenizer.defaultHandler , "type": TokenTypes.NEQ,         "expression": "(?i)\\<>" },
        "compareLessEqual":     { "order": 3060, "handler": Tokenizer.defaultHandler , "type": TokenTypes.LE,          "expression": "(?i)\\<=" },
        "compareGraterEqual":   { "order": 3070, "handler": Tokenizer.defaultHandler , "type": TokenTypes.GE,          "expression": "(?i)\\>=" },
        "compareLess":          { "order": 3080, "handler": Tokenizer.defaultHandler , "type": TokenTypes.LESS,        "expression": "(?i)\\<" },
        "compareGreater":       { "order": 3090, "handler": Tokenizer.defaultHandler , "type": TokenTypes.MORE,        "expression": "(?i)\\>" },
        "curlyopen":            { "order": 3100, "handler": Tokenizer.defaultHandler , "type": TokenTypes.CURLYOPEN,   "expression": "(?i)\\{" },
        "curlyclose":           { "order": 3110, "handler": Tokenizer.defaultHandler , "type": TokenTypes.CURLYCLOSE,  "expression": "(?i)\\}" },
        "roundopen":            { "order": 3120, "handler": Tokenizer.defaultHandler , "type": TokenTypes.ROUNDOPEN,   "expression": "(?i)\\(" },
        "roundclose":           { "order": 3130, "handler": Tokenizer.defaultHandler , "type": TokenTypes.ROUNDCLOSE,  "expression": "(?i)\\)" },
        "semicolon":            { "order": 3140, "handler": Tokenizer.defaultHandler , "type": TokenTypes.SEMICOLON,   "expression": "(?i)\\;" },
        "colon":                { "order": 3150, "handler": Tokenizer.defaultHandler , "type": TokenTypes.COLON,       "expression": "(?i)\\:" },
        "eq":                   { "order": 3160, "handler": Tokenizer.defaultHandler , "type": TokenTypes.EQ,          "expression": "(?i)\\=" },
        "assignment":           { "order": 3161, "handler": Tokenizer.defaultHandler , "type": TokenTypes.ASSIGNMENT,  "expression": "(?i)\\=" },
        "comma":                { "order": 3170, "handler": Tokenizer.defaultHandler , "type": TokenTypes.COMMA,       "expression": "(?i)\\," },
        "identifier":           { "order": 3180, "handler": Tokenizer.defaultHandler , "type": TokenTypes.IDENTIFIER,  "expression": "(?i)[a-z]{1}[a-z0-9]*[$]?[%$]{0,1}" },
        "whitespace":           { "order": 3190, "handler": Tokenizer.ignoreHandler  , "type": TokenTypes.WHITESPACE,  "expression": "[\\s]" },
        "envelope":             { "order":  140, "handler": Tokenizer.defaultHandler , "type": TokenTypes.ENVELOPE,    "expression": "(?i)ENVELOPE" },

        "endofline":            { "order": 9999, "handler": Tokenizer.defaultHandler , "type": TokenTypes.EOF,    "expression": "" }

    }
    
    Matrix = {
        # ------------------------------------------------------------------
        #                         AR    PP    V2    v3.5  v3.6  v4    v4+   v7    v10
        # ------------------------------------------------------------------
        "endofline":            [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],

        "lineNumber":           [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "literalSientific":     [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "literalFloat":         [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "literalInt":           [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "literalString":        [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "literalBoolean":       [ 0,    1,    0,    0,    0,    0,    0,    0,    0    ],

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
        "chr_dollar":           [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
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
        "ds_dollar":            [ 0,    0,    0,    1,    1,    1,    1,    1,    1    ],
        "dsave":                [ 0,    0,    0,    1,    1,    1,    1,    1,    1    ],
        "dverify":              [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "el":                   [ 0,    0,    0,    1,    1,    0,    1,    1,    1    ],
        "else":                 [ 0,    0,    0,    1,    1,    0,    1,    1,    1    ],
        "end":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "envelope":             [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "er":                   [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "err_dollar":           [ 0,    0,    0,    1,    1,    0,    1,    1,    1    ],
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
        "get_sharp":            [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "getkey":               [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "go":                   [ 0,    0,    0,    0,    0,    1,    1,    0,    0    ],
        "go64":                 [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "gosub":                [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "goto":                 [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "go_to":                [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "graphic":              [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "gshape":               [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "header":               [ 0,    0,    0,    1,    1,    1,    1,    1,    1    ],
        "help":                 [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "hex_dollar":           [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "if":                   [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "input":                [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "input_sharp":          [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "instr":                [ 0,    0,    0,    1,    0,    0,    1,    1,    1    ],
        "int":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        # ------------------------------------------------------------------
        #                         AR    PP    V2    v3.5  v3.6  v4    v4+   v7    v10
        # ------------------------------------------------------------------
        "joy":                  [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "key":                  [ 0,    0,    0,    1,    1,    0,    1,    1,    1    ],
        "left_dollar":          [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "len":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "let":                  [ 0,    0,    1,    0,    0,    0,    0,    0,    0    ],
        "list":                 [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "load":                 [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "locate":               [ 0,    0,    0,    1,    0,    0,    0,    1,    1    ],
        "log":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "loop":                 [ 0,    0,    0,    1,    0,    0,    0,    1,    1    ],
        "mid_dollar":           [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
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
        "pisign":               [ 0,    0,    0,    0,    1,    0,    0,    0,    0    ],
        "play":                 [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "pointer":              [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "poke":                 [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "popups":               [ 0,    0,    0,    0,    1,    0,    0,    0,    0    ],
        "pos":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "pot":                  [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "print":                [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "print_sharp":          [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "printUsing":           [ 0,    0,    0,    1,    1,    0,    1,    1,    1    ],
        "pudef":                [ 0,    0,    0,    1,    1,    0,    1,    1,    1    ],
        "quit":                 [ 0,    0,    0,    0,    0,    0,    0,    1,    1    ],
        "rclr":                 [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "rdot":                 [ 0,    0,    0,    1,    1,    0,    0,    1,    1    ],
        "read":                 [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "read_sharp":           [ 0,    0,    0,    0,    0,    1,    1,    0,    0    ],
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
        "right_dollar":         [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
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
        "str_dollar":           [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "swap":                 [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "sys":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "tab":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "tan":                  [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "tempo":                [ 0,    0,    0,    0,    1,    0,    0,    1,    1    ],
        "then":                 [ 0,    0,    1,    0,    1,    1,    1,    1,    1    ],
        "ti":                   [ 0,    0,    1,    0,    1,    1,    0,    1,    1    ],
        "ti_dollar":            [ 0,    0,    1,    0,    1,    1,    1,    1,    1    ],
        "time":                 [ 0,    0,    1,    0,    0,    0,    0,    0,    0    ],
        "time_dollar":          [ 0,    0,    1,    0,    0,    0,    0,    0,    0    ],
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
        "pisign":               [ 0,    0,    1,    0,    0,    0,    0,    0,    0    ],
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
        "assignment":           [ 0,    0,    1,    1,    1,    1,    1,    1,    1    ],
        "comma":                [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "identifier":           [ 0,    1,    1,    1,    1,    1,    1,    1,    1    ],
        "whitespace":           [ 1,    1,    1,    1,    1,    1,    1,    1,    1    ]

    }

