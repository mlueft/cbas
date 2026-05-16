import getopt, sys

import cbas
import cbas.Compiler.Compiler

Compiler = cbas.Compiler.Compiler.Compiler

# -s Source file to compile.
# -o Output folder. Compiled files are stored in this folder.
# -v Output version.
# -t Object folder.

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

    cbas.debug = False
    
    inputFile    = "./obj/a"
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
    options = "hbs:o:v:t:l:a:"
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

    #
    # Run Compiler
    #
    runCompiler( basicVersion, inputFile, outputFolder, objectFolder, lineNumberStart, lineNumberStep, basicStartAddress, beautify )



main()