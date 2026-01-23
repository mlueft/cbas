import cbas.Preprocessor.Preprocessor

Preprocessor = cbas.Preprocessor.Preprocessor.Preprocessor

def main():
    
    inputFile = r"/home/work/cbas/examples/main.bas"
    outputFolder = r"/home/work/cbas/obj"
    libFolder = [
        r"/home/work/cbas/lib"
    ]
        
    pp = Preprocessor( outputFolder, libFolder)
    
    pp.process(inputFile)
    
main()