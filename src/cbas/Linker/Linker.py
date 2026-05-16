import re

class Linker():

    def __init__(self, prg=True):
        self.lineNumber = None
        self.prg = prg
        self.lineNumberStart = 1
        self.lineNumberStep = 1
        self.basicStartAddress = 2049

        if not self.prg:
            self.prittifier = b" "
        else:
            self.prittifier = b""

        self.currentAddress = self.basicStartAddress

        self.resetLineNumber()

    def resetLineNumber(self):
        self.lineNumber = self.lineNumberStart
        self.currentAddress = self.basicStartAddress+1

    def main(self,lines):
        
        self.resetLineNumber()

        result = []

        
        #
        # We write the startAddress
        #
        if self.prg:
            result.append( self.basicStartAddress.to_bytes(length=2, byteorder='little') )

        labels={}

        #
        # We scan for label definitions
        #
        for line in lines:
            nextLineNumber = self.lineNumber+self.lineNumberStep
            pattern = re.compile(b"^@label_[0-9]{5}")
            matches = pattern.findall(line)
            for match in matches:
                labels[match]=nextLineNumber
                pass
            self.lineNumber = nextLineNumber


        self.resetLineNumber()

        for line in lines:
            
            # Is the line labeldefinition
            pattern = re.compile(b"^@label_[0-9]{5}")
            matches = pattern.findall(line)
            if len(matches) > 0:
                for match in matches:
                    #line = "rem {}".format(match)
                    line = None

            else:
                # replace labels in references
                for k,v in labels.items():
                    if self.prg:
                        line = line.replace(k,bytearray(str(v),encoding="ascii"))
                    else:
                        line = line.replace(k,bytearray(str(v),encoding="ascii"))

            if line is not None:
                l = bytearray()

                #
                # Place holder for address of next line
                #
                if self.prg:
                    l += (0).to_bytes(length=2, byteorder='little')

                # line number
                if self.prg:
                    bLow = self.lineNumber&255
                    bHigh = (self.lineNumber>>8)&255
                    l += bytes([bLow,bHigh])
                else:
                    tmp = bytes(str(self.lineNumber),"ascii") 
                    l += tmp
                
                # line
                l += self.prittifier+line
                
                # EOL
                if self.prg:
                    l += bytes([0])

                result.append(l)
            
            #
            # Set Address of next line
            #
            if self.prg:
                self.currentAddress += len(l)
                l[0] = self.currentAddress&255
                l[1] = (self.currentAddress>>8)&255
            
            self.lineNumber += self.lineNumberStep

        # EOF
        if self.prg:
            l += bytes([0,0])

        return result