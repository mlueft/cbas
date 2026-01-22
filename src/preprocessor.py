import cbas.Preprocessor.Preprocessor as pp

def main():
    
    inputFile = r"/home/work/cbas/examples/main.bas"
    outputFolder = r"/home/work/cbas/obj"
    libFolder = [
        r"/home/work/cbas/lib"
    ]
        
    processor = pp.Preprocessor( outputFolder, libFolder)
    
    processor.process(inputFile)
    
main()