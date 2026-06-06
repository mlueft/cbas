import getopt, sys, os, shutil

import cbas.Preprocessor.Preprocessor


Preprocessor = cbas.Preprocessor.Preprocessor.Preprocessor


# -s Source file to process.
# -o Output folder. Processed files are stored in this folder.
# -l Library folder. Is used to look for include files.

## Shows the help for console.
#
#
def showHelp():
    print( "Cbas preprocessor" )
    print( "" )
    print( "-s    - Source file." )
    print( "-o    - Output folder the processed file is stored in." )
    print( "-l    - Adds a lib folder. One -l for each folder." )
    print( "" )
    print( "" )
    

## Runs the preprocessor for the input file.
#
#
def runPreProcessor(inputFile, outputFolder, libFolders):
    preprocessor = Preprocessor()
    preprocessor.outputFolder = outputFolder
    preprocessor.libFolders = libFolders
    return preprocessor.main(inputFile)

##
#
#
def main():

    libFolders   = []
    inputFile    = None
    outputFolder = None

    # Debug parameters    
    inputFile    = r"./examples/testapp.bas"
    #inputFile    = r"./examples/basic_V2.bas"
    #inputFile    = r"./examples/pp_include.bas"
    outputFolder = r"./obj"
    libFolders   = [
        r"./lib"
    ]


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

    #
    # Create folder
    #
    try:
        os.mkdir(outputFolder)
    except FileExistsError:
        pass
    

    #
    # Run preprocessor
    #
    outputFile = runPreProcessor( inputFile, outputFolder, libFolders )
    
    #
    # We need the processed file to have the exact same name as the original one.
    #
    inputFile  = outputFile
    outputFile = outputFile[:-len(".pass1")]
    shutil.copyfile(inputFile,outputFile)


main()

try:
    pass#main()
except Exception as e:
    print( "Something went wrong while processing your file ..." )
    print( e )
