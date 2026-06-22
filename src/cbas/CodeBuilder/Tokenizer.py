import cbas.Lexer.TokenTypes
#import cbas.CodeBuilder.BasicBuilder
import cbas.CodeBuilder.Petscii

TokenTypes = cbas.Lexer.TokenTypes.TokenTypes
#BasicBuilder = cbas.CodeBuilder.BasicBuilder.BasicBuilder
Petscii = cbas.CodeBuilder.Petscii.Petscii

class Tokenizer():

    def __init__(self, configIndex):
        
        self.configIndex = configIndex

        # Keywords and symbols are converted to these tokens.
        self.basicTokens = {
            #                              BASIC         V2        V35     V4     V7   
            TokenTypes.MINUS:            [ [b"-"      ], [171],              ],
            TokenTypes.MUL:              [ [b"*"      ], [172],              ],
            TokenTypes.DIV:              [ [b"/"      ], [173],              ],
            TokenTypes.NEQ:              [ [b"<>"     ], [179,177],          ],
            TokenTypes.LESS:             [ [b"<"      ], [179],              ],
            TokenTypes.EQ:               [ [b"="      ], [178],              ],
            TokenTypes.ADD:              [ [b"+"      ], [170],              ],
            TokenTypes.MORE:             [ [b">"      ], [177],              ],
            "↑":                         [ [b"*"      ], [174],              ],
            TokenTypes.ABS:              [ [b"abs"    ], [182],              ],
            TokenTypes.AND:              [ [b"and"    ], [175],              ],
            TokenTypes.ASC:              [ [b"asc"    ], [198],              ],
            TokenTypes.ATN:              [ [b"atn"    ], [193],              ],
            TokenTypes.CHR_DOLLAR:       [ [b"chr$"   ], [199],              ],
            TokenTypes.CLOSE:            [ [b"close"  ], [160],              ],
            TokenTypes.CLR:              [ [b"clr"    ], [156],              ],
            TokenTypes.CMD:              [ [b"cmd"    ], [157],              ],
            TokenTypes.CONT:             [ [b"cont"   ], [154],              ],
            TokenTypes.COS:              [ [b"cos"    ], [190],              ],
            TokenTypes.DATA:             [ [b"data"   ], [131],              ],
            TokenTypes.DEF:              [ [b"def"    ], [150],              ],
            TokenTypes.DIM:              [ [b"dim"    ], [134],              ],
            TokenTypes.END:              [ [b"end"    ], [128],              ],
            TokenTypes.EXP:              [ [b"exp"    ], [189],              ],
            TokenTypes.FN:               [ [b"fn"     ], [165],              ],
            TokenTypes.FOR:              [ [b"for"    ], [129],              ],
            TokenTypes.FRE:              [ [b"fre"    ], [184],              ],
            TokenTypes.GET:              [ [b"get"    ], [161],              ],
            TokenTypes.GET_SHARP:        [ [b"get#"   ], [161,35],           ],
            TokenTypes.GO:               [ [b"go"     ], [203],              ],
            TokenTypes.GOSUB:            [ [b"gosub"  ], [141],              ],
            TokenTypes.GOTO:             [ [b"goto"   ], [137],              ],
            TokenTypes.IF:               [ [b"if"     ], [139],              ],
            TokenTypes.INPUT:            [ [b"input"  ], [133],              ],
            TokenTypes.INPUT_SHARP:      [ [b"input#" ], [132],              ],
            TokenTypes.INT:              [ [b"int"    ], [181],              ],
            TokenTypes.LEFT_DOLLAR:      [ [b"left$"  ], [200],              ],
            TokenTypes.LEN:              [ [b"len"    ], [195],              ],
            TokenTypes.LET:              [ [b"let"    ], [136],              ],
            TokenTypes.LIST:             [ [b"list"   ], [155],              ],
            TokenTypes.LOAD:             [ [b"load"   ], [147],              ],
            TokenTypes.LOG:              [ [b"log"    ], [188],              ],
            TokenTypes.MID_DOLLAR:       [ [b"mid$"   ], [202],              ],
            TokenTypes.NEW:              [ [b"new"    ], [162],              ],
            TokenTypes.NEXT:             [ [b"next"   ], [130],              ],
            TokenTypes.NOT:              [ [b"not"    ], [168],              ],
            TokenTypes.ON:               [ [b"on"     ], [145],              ],
            TokenTypes.OPEN:             [ [b"open"   ], [159],              ],
            TokenTypes.OR:               [ [b"or"     ], [176],              ],
            TokenTypes.PEEK:             [ [b"peek"   ], [194],              ],
            TokenTypes.POKE:             [ [b"poke"   ], [151],              ],
            TokenTypes.POS:              [ [b"pos"    ], [185],              ],
            TokenTypes.PRINT:            [ [b"print"  ], [153],              ],
            TokenTypes.PRINT_SHARP:      [ [b"print#" ], [152],              ],
            TokenTypes.READ:             [ [b"read"   ], [135],              ],
            TokenTypes.RESTORE:          [ [b"restore"], [140],              ],
            TokenTypes.RETURN:           [ [b"return" ], [142],              ],
            TokenTypes.RIGHT_DOLLAR:     [ [b"right$" ], [201],              ],
            TokenTypes.RND:              [ [b"rnd"    ], [187],              ],
            TokenTypes.RUN:              [ [b"run"    ], [138],              ],
            TokenTypes.SAVE:             [ [b"save"   ], [148],              ],
            TokenTypes.SGN:              [ [b"sgn"    ], [180],              ],
            TokenTypes.SIN:              [ [b"sin"    ], [191],              ],
            TokenTypes.SPC:              [ [b"spc"    ], [166],              ],
            TokenTypes.SQR:              [ [b"sqr"    ], [186],              ],
            TokenTypes.STEP:             [ [b"step"   ], [169],              ],
            TokenTypes.STOP:             [ [b"stop"   ], [144],              ],
            TokenTypes.STR_DOLLAR:       [ [b"str$"   ], [196],              ],
            TokenTypes.SYS:              [ [b"sys"    ], [158],              ],
            TokenTypes.TAB:              [ [b"tab"    ], [163],              ],
            TokenTypes.TAN:              [ [b"tan"    ], [192],              ],
            TokenTypes.THEN:             [ [b"then"   ], [167],              ],
            TokenTypes.TO:               [ [b"to"     ], [164],              ],
            TokenTypes.USR:              [ [b"usr"    ], [183],              ],
            TokenTypes.VAL:              [ [b"val"    ], [197],              ],
            TokenTypes.VERIFY:           [ [b"verify" ], [149],              ],
            TokenTypes.WAIT:             [ [b"wait"   ], [146],              ],
            TokenTypes.ST:               [ [b"st"     ], [83,84]             ],
            TokenTypes.STATUS:           [ [b"status" ], [83,84,65,84,85,83] ],
            TokenTypes.TI:               [ [b"ti"     ], [84,73]             ],
            TokenTypes.TI_DOLLAR:        [ [b"ti$"    ], [84,73,36]          ],
            TokenTypes.TIME:             [ [b"time"   ], [84,73,77,69]       ],
            TokenTypes.TIME_DOLLAR:      [ [b"time$"  ], [84,73,77,69,36]    ],
            TokenTypes.APPEND:           [ [b""       ], []                  ],
            TokenTypes.AUTO:             [ [b""       ], []                  ],
            TokenTypes.BACKUP:           [ [b""       ], []                  ],
            TokenTypes.BANK:             [ [b""       ], []                  ],
            TokenTypes.BEGIN:            [ [b""       ], []                  ],
            TokenTypes.BEND:             [ [b""       ], []                  ],
            TokenTypes.BLOAD:            [ [b""       ], []                  ],
            TokenTypes.BOOT:             [ [b""       ], []                  ],
            TokenTypes.BOX:              [ [b""       ], []                  ],
            TokenTypes.BSAVE:            [ [b""       ], []                  ],
            TokenTypes.BUMP:             [ [b""       ], []                  ],
            TokenTypes.CATALOG:          [ [b""       ], []                  ],
            TokenTypes.CHAR:             [ [b""       ], []                  ],
            TokenTypes.CIRCLE:           [ [b""       ], []                  ],
            TokenTypes.COLLECT:          [ [b""       ], []                  ],
            TokenTypes.COLLISION:        [ [b""       ], []                  ],
            TokenTypes.COLOR:            [ [b""       ], []                  ],
            TokenTypes.CONCAT:           [ [b""       ], []                  ],
            TokenTypes.COPY:             [ [b""       ], []                  ],
            TokenTypes.DECLARE:          [ [b""       ], []                  ],
            TokenTypes.DCLOSE:           [ [b""       ], []                  ],
            TokenTypes.DEC:              [ [b""       ], []                  ],
            TokenTypes.DELETE:           [ [b""       ], []                  ],
            TokenTypes.DIRECTORY:        [ [b""       ], []                  ],
            TokenTypes.DLOAD:            [ [b""       ], []                  ],
            TokenTypes.DO:               [ [b""       ], []                  ],
            TokenTypes.DOPEN:            [ [b""       ], []                  ],
            TokenTypes.DRAW:             [ [b""       ], []                  ],
            TokenTypes.DSAVE:            [ [b""       ], []                  ],
            TokenTypes.DVERIFY:          [ [b""       ], []                  ],
            TokenTypes.ELSE:             [ [b""       ], []                  ],
            TokenTypes.ENVELOPE:         [ [b""       ], []                  ],
            TokenTypes.ERR_DOLLAR:       [ [b""       ], []                  ],
            TokenTypes.EXIT:             [ [b""       ], []                  ],
            TokenTypes.FAST:             [ [b""       ], []                  ],
            TokenTypes.FETCH:            [ [b""       ], []                  ],
            TokenTypes.FILTER:           [ [b""       ], []                  ],
            TokenTypes.GRAPHIC:          [ [b""       ], []                  ],
            TokenTypes.GSHAPE:           [ [b""       ], []                  ],
            TokenTypes.HEADER:           [ [b""       ], []                  ],
            TokenTypes.HELP:             [ [b""       ], []                  ],
            TokenTypes.HEX_DOLLAR:       [ [b""       ], []                  ],
            TokenTypes.INSTR:            [ [b""       ], []                  ],
            TokenTypes.JOY:              [ [b""       ], []                  ],
            TokenTypes.KEY:              [ [b""       ], []                  ],
            TokenTypes.LOCATE:           [ [b""       ], []                  ],
            TokenTypes.LOOP:             [ [b""       ], []                  ],
            TokenTypes.MONITOR:          [ [b""       ], []                  ],
            TokenTypes.MOVSPR:           [ [b""       ], []                  ],
            TokenTypes.OFF:              [ [b""       ], []                  ],
            TokenTypes.PAINT:            [ [b""       ], []                  ],
            TokenTypes.PEN:              [ [b""       ], []                  ],
            TokenTypes.PLAY:             [ [b""       ], []                  ],
            TokenTypes.POINTER:          [ [b""       ], []                  ],
            TokenTypes.POT:              [ [b""       ], []                  ],
            TokenTypes.PUDEF:            [ [b""       ], []                  ],
            TokenTypes.QUIT:             [ [b""       ], []                  ],
            TokenTypes.RCLR:             [ [b""       ], []                  ],
            TokenTypes.RDOT:             [ [b""       ], []                  ],
            TokenTypes.RECORD:           [ [b""       ], []                  ],
            TokenTypes.RENAME:           [ [b""       ], []                  ],
            TokenTypes.RENUMBER:         [ [b""       ], []                  ],
            TokenTypes.RESUME:           [ [b""       ], []                  ],
            TokenTypes.RGR:              [ [b""       ], []                  ],
            TokenTypes.RLUM:             [ [b""       ], []                  ],
            TokenTypes.RREG:             [ [b""       ], []                  ],
            TokenTypes.RSPCOLOR:         [ [b""       ], []                  ],
            TokenTypes.RSPPOS:           [ [b""       ], []                  ],
            TokenTypes.RSSPRITE:         [ [b""       ], []                  ],
            TokenTypes.RWINDOW:          [ [b""       ], []                  ],
            TokenTypes.SCALE:            [ [b""       ], []                  ],
            TokenTypes.SCNCLR:           [ [b""       ], []                  ],
            TokenTypes.SCRATCH:          [ [b""       ], []                  ],
            #TokenTypes.shift:            [ [b""       ], []                  ],
            #TokenTypes.shift:            [ [b""       ], []                  ],
            TokenTypes.SLEEP:            [ [b""       ], []                  ],
            TokenTypes.SLOW:             [ [b""       ], []                  ],
            TokenTypes.SOUND:            [ [b""       ], []                  ],
            TokenTypes.SPRCOLOR:         [ [b""       ], []                  ],
            TokenTypes.SPRDEF:           [ [b""       ], []                  ],
            TokenTypes.SPRITE:           [ [b""       ], []                  ],
            TokenTypes.SPRSAV:           [ [b""       ], []                  ],
            TokenTypes.SSHAPE:           [ [b""       ], []                  ],
            TokenTypes.STASH:            [ [b""       ], []                  ],
            TokenTypes.SWAP:             [ [b""       ], []                  ],
            TokenTypes.TEMPO:            [ [b""       ], []                  ],
            TokenTypes.TRAP:             [ [b""       ], []                  ],
            TokenTypes.TROFF:            [ [b""       ], []                  ],
            TokenTypes.TRON:             [ [b""       ], []                  ],
            TokenTypes.UNTIL:            [ [b""       ], []                  ],
            TokenTypes.USING:            [ [b""       ], []                  ],
            TokenTypes.VOL:              [ [b""       ], []                  ],
            TokenTypes.WHILE:            [ [b""       ], []                  ],
            TokenTypes.WIDTH:            [ [b""       ], []                  ],
            TokenTypes.WINDOW:           [ [b""       ], []                  ],
            TokenTypes.XOR:              [ [b""       ], []                  ],
            TokenTypes.COMMA:            [ [b","      ], [44]                ],
            TokenTypes.SEMICOLON:        [ [b";"      ], [59]                ],
            TokenTypes.COLON:            [ [b":"      ], [58]                ],
            TokenTypes.ROUNDOPEN:        [ [b"("      ], [40]                ],
            TokenTypes.ROUNDCLOSE:       [ [b")"      ], [41]                ],
            TokenTypes.PISIGN:           [ [b"{pi}"   ], [255]               ]
        }

        # Values of these types are unchanged.
        # All other values are tokenized
        self.valueTokens = [
            TokenTypes.IDENTIFIER,
            TokenTypes.LABEL
        ]

    def __tokenizeLiteral(self,tag,value):
        result = bytearray()
        
        if self.configIndex == 1:
            data = str(value)
            result = Petscii.toPetscii(data)

        else:
            # String for basic file
            result = bytearray(str(value), "ascii")
            
        return result

    def tokenize(self, tokenType, value=None):

        #
        # Key word tokens
        #
        if tokenType in self.basicTokens:
            result = bytearray()
            _bytes = self.basicTokens[tokenType][self.configIndex]
            for b in _bytes:
                if type(b) == type(1):
                    # We got numbers from tokens and convert into bytes.
                    #b1 = bytes(str(b),"ascii")
                    b1 = b.to_bytes(length=1, byteorder='little')
                    result += b1
                else:
                    # We got bytes direktly from tokens
                    result += b

            return result

        #
        # For some Tokens the value remains unchanged.
        #
        for t in self.valueTokens:
            if tokenType == t:
                return bytearray(str(value), "ascii")

        #
        # literals
        #
        if tokenType in [ TokenTypes.STRING, TokenTypes.INTEGER, TokenTypes.FLOAT, TokenTypes.BOOLEAN ]:
            return self.__tokenizeLiteral(tokenType, value)
        
        raise ValueError("Unknown tag: {}".format(tokenType))