import getopt, sys, os

import cbas
import cbas.Compiler.Compiler

Compiler = cbas.Compiler.Compiler.Compiler

def showHelp():
    print( "Cbas Compiler" )
    print( "" )
    print( "-s    - Source file." )
    print( "-o    - Output folder the processed file is stored to." )
    print( "-v    - Basic version to generate." )
    print( "-t    - Temp folder to store files in." )
    print( "-l    - Line number start[,step]. Default 1,1" )
    print( "-a    - Address of BasicProgram. Default 2049" )
    print( "-b    - Beautify Basic Code. Uses Space to format basic code.")
    print( "-r    - Reuse variable names.")
    print( "" )

def runCompiler( version, inputFile, outputFolder, objectFolder, lineNumberStart, lineNumberStep, basicStartAddress, beautify):
    compiler = Compiler(version)
    compiler.objectFolder = objectFolder
    compiler.binFolder = outputFolder
    compiler.lineNumberStart = lineNumberStart
    compiler.lineNumberStep = lineNumberStep
    compiler.basicStartAddress = basicStartAddress
    compiler.beautify = beautify
    compiler.compileFile( inputFile )

def main():

    cbas.debug = True
    
    inputFile    = "./obj/testapp.bas"
    #inputFile    = "./obj/pp_include.bas"
    #inputFile    = r"./obj/basic_V2.bas"
    objectFolder = "/home/work/cbas/obj"
    outputFolder = "/home/work/cbas/bin"
    
    #inputFile       = None
    #objectFolder    = None
    #outputFolder    = None
    basicVersion    = 2
    lineNumberStart = 1
    lineNumberStep  = 1
    basicStartAddress = 2049
    beautify          = False

    #
    # Check CLI-Parameter
    #
    args = sys.argv[1:]
    options = "hbs:o:v:t:l:a:r"
    long_options = []

    try:
        arguments, values = getopt.getopt(args, options, long_options)
        for currentArg, currentVal in arguments:
            
            if currentArg in ("-s"):
                inputFile = currentVal

            elif currentArg in ("-o"):
                outputFolder = currentVal

            elif currentArg in ("-v"):
                basicVersion = int(currentVal)

            elif currentArg in ("-t"):
                objectFolder = currentVal

            elif currentArg in ("-l"):
                data = currentVal.split(",")
                lineNumberStart = int(data[0])
                if len(data) > 1:
                    lineNumberStep = int(data[1])

            elif currentArg in ("-a"):
                basicStartAddress = int(currentVal)

            elif currentArg in ("-b"):
                beautify = True

            elif currentArg in ("-r"):
                cbas.symbolTable.reuseVariables = True

            elif currentArg in ("-h"):
                showHelp()
                return

            else:
                showHelp()
                return

    except getopt.error as err:
        print(str(err))

    if False:
        print( "=====================================" )
        print( "inputFile         : {}".format( inputFile ))
        print( "objectFolder      : {}".format( objectFolder ))
        print( "outputFolder      : {}".format( outputFolder ))
        print( "basicVersion      : {}".format( basicVersion ))
        print( "lineNumberStart   : {}".format( lineNumberStart ))
        print( "lineNumberStep    : {}".format( lineNumberStep ))
        print( "basicStartAddress : {}".format( basicStartAddress ))
        print( "beautify          : {}".format( beautify ))
        print( "reuseVariables    : {}".format( cbas.symbolTable.reuseVariables ))


    #
    # Create folders
    #
    try:
        os.mkdir(objectFolder)
    except FileExistsError:
        pass
    
    try:
        os.mkdir(outputFolder)
    except FileExistsError:
        pass
    
    #
    # Run Compiler
    #
    runCompiler( basicVersion, inputFile, outputFolder, objectFolder, lineNumberStart, lineNumberStep, basicStartAddress, beautify )



main()

try:
    pass#main()
except Exception as e:
    print( "Something went wrong while processing your file ..." )
    print( e )

