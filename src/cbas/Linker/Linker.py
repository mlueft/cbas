import re

class Linker():

    def __init__(self):
        self.lineNumber = None
        self.lineStep = None
        self.resetLineNumber()

    def resetLineNumber(self):
        self.lineNumber = 1
        self.lineStep = 1

    def main(self,lines):
        
        self.resetLineNumber()

        result = []

        labels={}

        #
        # We scan for label definitions
        #
        for line in lines:
            nextLineNumber = self.lineNumber+self.lineStep
            pattern = re.compile("^@label_[0-9]{5}")
            matches = pattern.findall(line)
            for match in matches:
                labels[match]=nextLineNumber
                pass
            self.lineNumber = nextLineNumber


        self.resetLineNumber()

        for line in lines:
            
            # Is the line labeldefinition
            pattern = re.compile("^@label_[0-9]{5}")
            matches = pattern.findall(line)
            if len(matches) > 0:
                for match in matches:
                    #line = "rem {}".format(match)
                    line = None

            else:
                # replace labels in references
                for k,v in labels.items():
                    line = line.replace(k,str(v))

            if line is not None:
                result.append( "{} {}".format(self.lineNumber,line) )
            
            self.lineNumber += self.lineStep

        return result