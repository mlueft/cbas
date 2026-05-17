import getopt, sys

import cbas.Preprocessor.Preprocessor
#import cbas.Config.Config

Preprocessor = cbas.Preprocessor.Preprocessor.Preprocessor
#Config = cbas.Config.Config.Config


# -s Source file to process.
# -o Output folder. Processed files are stored in this folder.
# -l Library folder. Is used to look for include files.

def showHelp():
    print( "Cbas preprocessor" )
    print( "" )
    print( "-s    - Source file." )
    print( "-o    - Output folder the processed file is stored in." )
    print( "-l    - Adds a lib folder. One -l for each folder." )
    print( "" )
    print( "" )
    

def runPreProcessor(inputFile, outputFolder, libFolders):
    preprocessor = Preprocessor( outputFolder, libFolders)
    preprocessor.process(inputFile)

def main():
    
    inputFile    = r"./examples/a"
    outputFolder = r"/home/work/cbas/obj"
    libFolders   = [
        r"/home/work/cbas/lib"
    ]

    #inputFile    = None
    #outputFolder = None
    libFolders   = []

    #
    # Check CLI-Parameters
    #
    args = sys.argv[1:]
    options = "s:o:l:h"
    long_options = []

    try:
        arguments, values = getopt.getopt(args, options, long_options)
        for currentArg, currentVal in arguments:

            if currentArg in ("-s"):
                inputFile = currentVal

            elif currentArg in ("-o"):
                outputFolder = currentVal

            elif currentArg in ("-l"):
                libFolders.append(currentVal)

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
        print( "libFolders        : {}".format( libFolders ))
        print( "outputFolder      : {}".format( outputFolder ))


    #
    # Run preprocessor
    #
    runPreProcessor( inputFile, outputFolder, libFolders )
    


main()