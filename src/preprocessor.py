import cbas.Preprocessor.Preprocessor
import cbas.Config.Config

Preprocessor = cbas.Preprocessor.Preprocessor.Preprocessor
Config = cbas.Config.Config.Config

def main():
    
    inputFile = r"/home/work/cbas/examples/main.bas"
    outputFolder = r"/home/work/cbas/obj"
    libFolders = [
        r"/home/work/cbas/lib"
    ]
        

    pp = Preprocessor( outputFolder, libFolders)
    
    #inputFile   = "/home/work/cbas/examples/pp_macros.bas"
    #pp.process(inputFile)
    
    inputFile   = "/home/work/cbas/examples/pp_arithmetics.bas"
    inputFile   = "/home/work/cbas/examples/pp_include.bas"
    pp.process(inputFile)
    


main()