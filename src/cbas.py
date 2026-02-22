import re

import cbas.Compiler.Compiler

Compiler = cbas.Compiler.Compiler.Compiler

def main():
    configFile  = "/home/work/cbas/config/config.json"
    inputFile   = "/home/work/cbas/examples/main2.bas"
    #inputFile   = "/home/work/cbas/examples/arithmetic.bas"

    compiler = Compiler()
 
    
    log = []

    if False:
        tests = [
            ["1",1],
            ["1+1",2],
            ["2-1",1],
            ["10/2",5],
            ["10*2",20],
            ["1+10/2", 6],
            ["1+10/2+1", 7],
            ["1+10/2+1+10/2",12],
            ["1+10/2+1+(10/2)", 12],
            ["1+10/2+1/(10/2)", 6.2],
            ["-5-4",-9],
            ["-5 - -3",-2],
            ["-5 - (-2-1)",-2],
            ["-5 -(1+1)-1",-8],
            ["-5 -(((1)+(1)))-(1)",-8],

            ["0.5*2",1]

            ["true",True],
            ["false",False],

            ["true = true",True],
            ["false = false",True],
            ["true = false",False],

            ["4 = 4",True],
            ["4 = 5",False],

            ["4 <> 5",True],
            ["5 <> 5",False],

            ["4 < 5",True],
            ["5 < 4",False],

            ["5 > 4",True],
            ["4 > 5",False],

            ["4 <= 5",True],
            ["4 <= 4",True],
            ["4 <= 3",False],

            ["6 >= 5",True],
            ["5 >= 5",True],
            ["4 >= 5",False]
        ]

        for t in tests:
            term  = t[0]
            shall = t[1]

            result = compiler.compileExpression(term,1).statements[0].value
            if shall != result:
                log.append( "{}={} != {}".format(term,result,shall) )

    if True:
        compiler.compileFile( inputFile, 1 )

    print("==================")
    if len(log)==0:
        print("perfekt")

    for l in log:
        print(l)

main()
