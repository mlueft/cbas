import io

class FileCleaner():

    def __init__(self):
        self.outputFolder = None
        self.stringDelimiter = "\""

    ##
    #
    #
    def main(self, inputFile, outputFile):
        
        
        # Creates a file object for the input file.
        with io.open(inputFile, "r", encoding="utf-8") as inputfile:

            # Creates a file object for the output file.
            with io.open(outputFile, "w", encoding="utf-8") as outputfile:

                # Runs the preprocessor for the input file.
                self.__main(inputfile,outputfile)

    ##
    #  1. Remove empty lines.
    #  2. Remove single line comments.
    #  3. Remove multi line comments. not yet
    #  4. Concatenate lines ending with underline.
    #
    def __main(self, inputStream, outputStream):

            lines = inputStream.readlines()

            lines = self.removeLineBreak(lines)

            lines = self.removeEmptyLines(lines)

            lines = self.removeComments(lines)

            lines = self.removeEmptyLines(lines)

            lines = self.concatenateLines(lines)

            lines = self.removeEmptyLines(lines)

            #lines = self.__readLines(inputStream)

            for line in lines:
                outputStream.write( line +"\n" )


    ##
    #
    #
    def concatenateLines(self,lines):

        linenr = len(lines)-1
        newLine = ""
        while linenr > 0:

            line = lines[linenr]
            
            line = line.strip()

            if line[-1:] == "_":

                lines[linenr] = lines[linenr].rstrip()

                lines[linenr] = lines[linenr].rstrip("_")

                lines[linenr] += lines[linenr+1].strip()

                lines[linenr+1] = ""

            linenr -= 1


        return lines

    ##
    #
    #
    def removeComments(self,lines):

        result = []
        #ex: a= "remember the string" rem this is a comment
        #        --- this is no comment

        #
        # Single line comments
        #
        for line in lines:
            pos = 0
            res=""
            while pos < len(line):
                
                c = line[pos]

                # We read a string till it's end.
                if line[pos:pos+1] == "\"":

                    # We read till the end of the string
                    while True:
                        res += line[pos]
                        pos += 1
                        if line[pos:pos+1] == "\"":
                            # string end reached.
                            res += line[pos]
                            break

                else:

                    # single line comment starts here
                    if line[pos:pos+3] == "rem" or line[pos:pos+2] == "//":
                        # The rest of the line is a comment.
                        # we are finished
                        pos = len(line)
                    
                    else:
                        # we are in code and add char to result
                        res += line[pos]
                
                pos += 1

            result.append(res)


        lines = result
        result = []

        isComment = False

        #
        # Multi line comments
        #
        linenr = 0
        newLine = ""
        while linenr < len(lines):

            pos = 0
            line = lines[linenr]
            while pos < len(line):
                c = line[pos]

                if line[pos:pos+2] == "/*":
                    isComment = True

                if line[pos-1:pos+1] == "*/" :
                    isComment = False
                    c = ""

                if not isComment:
                    newLine += c
                
                pos += 1

            result.append(newLine)
            newLine = ""
            linenr += 1


        return result    

    ##
    #
    #
    def removeEmptyLines(self, lines):
        result = []
        for line in lines:
            if line.strip() != "":
                result.append(line)
        return result
     
    ##
    #
    #
    def removeLineBreak(self, lines):
        result = []
        for line in lines:
            line = line.rstrip("\n")
            result.append(line)
        return result

    ##
    #
    #
    def ___readLines(self,inputStream):
        
        result = ""


        #
        # EOF?
        #
        if line == "":
            return line
        

        #
        # We remove single line comments
        #
        line = self.__removeSingleLineComments(line)

        # The line was a comment, so we take the next one.
        if line is None:
            line = self.___readLines(inputStream)

        line = line.rstrip()

        if line[-1:] != "_":
            return line

        #
        # We concatenate the next line.
        #
        line = line.strip()
        line = line.rstrip("_")
        result += line

        line = self.___readLines(inputStream)
        result += line

        return result
    


