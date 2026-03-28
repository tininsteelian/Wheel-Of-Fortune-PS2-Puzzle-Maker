import argparse
import math
import re

parser = argparse.ArgumentParser()
parser.add_argument("inputFile", help="The filepath for your custom puzzles file.")
parser.add_argument("outputFolder", help="The output folder for PUZZLES.BIN or PUZZLEB.BIN. This can be the Wheel of Fortune DATA folder if you want to directly overwrite the file there.")
args = parser.parse_args()

file = args.inputFile
outputFolder = args.outputFolder
if outputFolder[-1] != '/' and outputFolder[-1] != '\\':
    if outputFolder.count('/') > 0:
        outputFolder += '/'
    elif outputFolder.count('\\') > 0:
        outputFolder += '\\'

mode = 0 # 0 = normal, 1 = bonus
category = b'\x00'
output = bytearray(b'\x09\xC3\xAF\x68\x2F\x6C\x20\x72\x65\x63\x6F\x72\x64\x73\x20\x2B\x72\x65\x63\x6C\x65\x6E\x2B\x33\x37\x2B\x32\x20\x42\x59\x54\x45\x53\x00\x00\x00\x00\x00\x00\x00\x0D\x0A')
errorCount = 0
lineCount = 0

with open (file) as f:
    for line in f:
        lineCount += 1
        #get the category
        if line[0] == '!':
            line = line.lower()
            if lineCount == 1 and line.strip() == "!bonus":
                mode = 1
                output = bytearray(b'\x01\xF4\xAF\x68\x2F\x6C\x20\x72\x65\x63\x6F\x72\x64\x73\x20\x2B\x72\x65\x63\x6C\x65\x6E\x2B\x33\x37\x2B\x32\x20\x42\x59\x54\x45\x53\x00\x00\x00\x00\x00\x00\x00\x0D\x0A')
            elif line.strip() == "!phrase":
                category = b'\x00'
            elif line.strip() == "!person":
                category = b'\x01'
            elif line.strip() == "!people":
                category = b'\x02'
            elif line.strip() == "!title":
                category = b'\x03'
            elif line.strip() == "!landmark":
                category = b'\x04'
            elif line.strip() == "!place":
                category = b'\x05'
            elif line.strip() == "!thing":
                category = b'\x06'
            elif line.strip() == "!quotation":
                category = b'\x07'
            elif line.strip() == "!event":
                category = b'\x08'
            elif line.strip() == "!fictional character":
                category = b'\x09'
            elif line.strip() == "!star & role" or line.strip() == "!star and role":
                category = b'\x0C'
            elif line.strip() == "!occupation":
                category = b'\x0E'
            elif line.strip() == "!husband & wife" or line.strip() == "!husband and wife":
                category = b'\x0F'
            elif line.strip() == "!same name":
                category = b'\x10'
            elif line.strip() == "!before & after" or line.strip() == "!before and after":
                category = b'\x11'
            elif line.strip() == "!family":
                category = b'\x12'
            elif line.strip() == "!clue":
                category = b'\x13'
            elif line.strip() == "!artist / song" or line.strip() == "!artist/song":
                category = b'\x15'
            elif line.strip() == "!title / author" or line.strip() == "!title/author":
                category = b'\x16'
            elif line.strip() == "!the 60's" or line.strip() == "!the 60s":
                category = b'\x18'
            elif line.strip() == "!nickname":
                category = b'\x19'
            elif line.strip() == "!classic tv":
                category = b'\x1A'
            elif line.strip() == "!fictional characters":
                category = b'\x1B'
            elif line.strip() == "!fill in the blank":
                category = b'\x1C'
            elif line.strip() == "!next line please":
                category = b'\x1D'
            elif line.strip() == "!proper name":
                category = b'\x1E'
            elif line.strip() == "!show biz":
                category = b'\x20'
            elif line.strip() == "!slogan":
                category = b'\x21'
            elif line.strip() == "!the 70's" or line.strip() == "!the 70s":
                category = b'\x22'
            elif line.strip() == "!the 80's" or line.strip() == "!the 80s":
                category = b'\x23'
            elif line.strip() == "!the 90's" or line.strip() == "!the 90s":
                category = b'\x24'
            elif line.strip() == "!things":
                category = b'\x25'
            elif line.strip() == "!where are we?" or line.strip() == "!where are we":
                category = b'\x26'
            elif line.strip() == "!who is it?" or line.strip() == "!who is it":
                category = b'\x27'
            elif line.strip() == "!who said it?" or line.strip() == "!who said it":
                category = b'\x28'
            elif line.strip() == "!author / title" or line.strip() == "!author/title":
                category = b'\x29'
            elif line.strip() == "!around the house":
                category = b'\x2B'
            elif line.strip() == "!fill in the number":
                category = b'\x2C'
            elif line.strip() == "!on the map":
                category = b'\x2D'
            elif line.strip() == "!rhyme time":
                category = b'\x2E'
            elif line.strip() == "!headline":
                category = b'\x30'
            # unused categories
            elif line.strip() == "!fictional place":
                category = b'\x0A'
            elif line.strip() == "!places":
                category = b'\x0B'
            elif line.strip() == "!person / title" or line.strip() == "!person/title":
                category = b'\x0D'
            elif line.strip() == "!foreign word":
                category = b'\x14'
            elif line.strip() == "!slang":
                category = b'\x17'
            elif line.strip() == "!proper names":
                category = b'\x1F'
            elif line.strip() == "!song / artist" or line.strip() == "!song/artist":
                category = b'\x2A'
            elif line.strip() == "!events":
                category = b'\x2F'
            elif line.strip() == "!where are they?" or line.strip() == "!where are they":
                category = b'\x31'
            elif line.strip() == "!puzzler":
                category = b'\x32'
            elif line.strip() == "!surprise question":
                category = b'\x33'
            elif line.strip() == "!person or people":
                category = b'\x34'
            # default to 'phrase'
            else:
                category = b'\x00'
                print("error: invalid category: " + line.strip('\n') + " (line " + str(lineCount) + ")")
                errorCount += 1

        # puzzle
        elif len(line) > 1: #don't parse blank lines
            line = line.upper()
            line = line.strip('\n')
            choices = line.split('~')
            choices[0] = choices[0].replace('\x20', '\x00')

            # automatic line parser
            if len(choices[0]) > 14 and choices[0].count('|') == 0:
                finalLine = ""
                remainingLine = choices[0]
                numRows = 1
                while len(remainingLine) > 14 and numRows <= 5:
                    if numRows == 5:
                        print("error: can't fit this line on the board aaa: " + choices[0] + " (line " + str(lineCount) + ")")
                        errorCount += 1
                    for i in range(14):
                        if remainingLine[14 - i] == '\x00':
                            finalLine += remainingLine[:14 - i] + '|'
                            remainingLine = remainingLine[14 - i + 1:]
                            break
                    numRows += 1

                if numRows == 2:
                    finalLine += remainingLine

                # if there are 3 or more lines, we need to make sure the 1st and 4th lines have 12 characters or less, so we re-do the parse more fancily (AKA badly)
                if numRows == 3 or numRows == 4:
                    altAttempt = 0
                    finalLine = ""
                    remainingLine = choices[0]
                    # line 1
                    for i in range(12):
                        if remainingLine[12 - i] == '\x00':
                            finalLine += remainingLine[:12 - i] + '|'
                            remainingLine = remainingLine[12 - i + 1:]
                            break
                    if remainingLine == line:  # try for 3 lines with 13-14 characters on the first line
                        # line 1
                        altAttempt = 1
                        for i in range(14):
                            if remainingLine[14 - i] == '\x00':
                                finalLine += remainingLine[:14 - i] + '|'
                                remainingLine = remainingLine[14 - i + 1:]
                                break
                        # line 2
                        for i in range(14):
                            if remainingLine[14 - i] == '\x00':
                                finalLine += remainingLine[:14 - i] + '|'
                                remainingLine = remainingLine[14 - i + 1:]
                                break
                        # line 3
                        if len(remainingLine) > 12:
                            print("error: can't fit this line on the board bbb: " + choices[0] + " (line " + str(lineCount) + ")")
                            errorCount += 1
                        else:
                            finalLine += remainingLine
                    # line 2
                    if altAttempt == 0:
                        for i in range(14):
                            if remainingLine[14 - i] == '\x00':
                                finalLine += remainingLine[:14 - i] + '|'
                                remainingLine = remainingLine[14 - i + 1:]
                                break
                        # line 3
                        if len(remainingLine) > 14:
                            for i in range(14):
                                if remainingLine[14 - i] == '\x00':
                                    finalLine += remainingLine[:14 - i] + '|'
                                    remainingLine = remainingLine[14 - i + 1:]
                                    break
                            # line 4
                            if len(remainingLine) > 12:
                                print (remainingLine)
                                print("error: can't fit this line on the board ccc: " + choices[0] + " (line " + str(lineCount) + ")")
                                errorCount += 1
                            else:
                                finalLine += remainingLine
                        else:
                            finalLine += remainingLine

                lines = finalLine.split('|')
            else:
                lines = choices[0].split('|')

            line1ba = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
            line2ba = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
            line3ba = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
            line4ba = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
            longestLine = max(lines, key=len)

            if line.count('~') > 1:
                print("error: invalid line: " + line + " (line " + str(lineCount) + ")")
                errorCount += 1

            if line.count('~') == 0:
                if category == b'\x13' or category == b'\x1C' or category == b'\x1D' or category == b'\x21' or category == b'\x26' or category == b'\x27' or category == b'\x28' or category == b'\x2C':
                    print("error: the selected category for this line requires a multiple-choice question: " + line + " (line " + str(lineCount) + ")")
                    errorCount += 1

            for l in lines:
                if re.search(r'\d', l):
                    print("error: numbers are not supported: " + l + " (line " + str(lineCount) + ")")
                    errorCount += 1

                # supported special characters: #&-'.?
                if re.search(r'[^0-9a-zA-Z#&\-.\'?\x00]', l):
                    print("error: invalid special character: " + l + " (line " + str(lineCount) + ")")
                    errorCount += 1

            if len(lines) > 4:
                print("error: too many rows: " + line + " (line " + str(lineCount) + ")")
                errorCount += 1

            if len(choices) > 1:
                if choices[1].count('/') < 2:
                    print("error: not enough choices: " + choices[1] + " (line " + str(lineCount) + ")")
                    errorCount += 1

                if choices[1].count('/') > 2:
                    print("error: too many choices: " + choices[1] + " (line " + str(lineCount) + ")")
                    errorCount += 1

                if choices[1].count('*') < 1:
                    print("error: no correct answer marked: " + choices[1] + " (line " + str(lineCount) + ")")
                    errorCount += 1

                if choices[1].count('*') > 1:
                    print("error: too many correct answers marked: " + choices[1] + " (line " + str(lineCount) + ")")
                    errorCount += 1

                if choices[1].count('*') >= 1:
                    asteriskIndex = line.index("*")
                    if line[asteriskIndex - 1] != '~' and line[asteriskIndex - 1] != '/':
                        print("error: probably incorrect asterisk location: " + choices[1] + " (line " + str(lineCount) + ")")
                        errorCount += 1

                if len(choices[1]) > 120:
                    print("error: choices are too long: " + choices[1] + " (line " + str(lineCount) + ")")
                    errorCount += 1

            if len(lines) == 1:
                output += line1ba

                for i in range(math.ceil((14 - len(lines[0]))/2)):
                    output += b'\x00'
                output.extend(lines[0].encode("utf-8"))
                for i in range(math.floor((14 - len(lines[0]))/2)):
                    output += b'\x00'

                output += line3ba

                output += line4ba

                if len(lines[0]) > 14:
                    print("error: row too long: " + lines[0] + " (line " + str(lineCount) + ")")
                    errorCount += 1

            if len(lines) == 2:
                output += line1ba

                byteCount = 0
                for i in range(math.ceil((14 - len(longestLine))/2)):
                    output += b'\x00'
                    byteCount += 1
                output.extend(lines[0].encode("utf-8"))
                byteCount += len(lines[0])
                while byteCount < 14:
                    output += b'\x00'
                    byteCount += 1

                byteCount = 0
                for i in range(math.ceil((14 - len(longestLine)) / 2)):
                    output += b'\x00'
                    byteCount += 1
                output.extend(lines[1].encode("utf-8"))
                byteCount += len(lines[1])
                while byteCount < 14:
                    output += b'\x00'
                    byteCount += 1

                output += line4ba

                if len(lines[0]) > 14:
                    print("error: row too long: " + lines[0] + " (line " + str(lineCount) + ")")
                    errorCount += 1
                if len(lines[1]) > 14:
                    print("error: row too long: " + lines[1] + " (line " + str(lineCount) + ")")
                    errorCount += 1

            if len(lines) == 3:
                if len(lines[0]) == 13 or len(lines[0]) == 14:
                    output += line1ba

                    byteCount = 0
                    linePosition = 14
                    if len(longestLine) == 14 and len(lines[0]) < 14:
                        linePosition = 13
                    else:
                        linePosition = len(longestLine)
                    for i in range(math.ceil((14 - linePosition) / 2)):
                        output += b'\x00'
                        byteCount += 1
                    output.extend(lines[0].encode("utf-8"))
                    byteCount += len(lines[0])
                    while byteCount < 14:
                        output += b'\x00'
                        byteCount += 1

                    byteCount = 0
                    linePosition = 14
                    if len(longestLine) == 14 and len(lines[1]) < 14:
                        linePosition = 13
                    else:
                        linePosition = len(longestLine)
                    for i in range(math.ceil((14 - linePosition) / 2)):
                        output += b'\x00'
                        byteCount += 1
                    output.extend(lines[1].encode("utf-8"))
                    byteCount += len(lines[1])
                    while byteCount < 14:
                        output += b'\x00'
                        byteCount += 1

                    byteCount = 0
                    for i in range(math.ceil((12 - min(len(longestLine), 12)) / 2)):
                        output += b'\x00'
                        byteCount += 1
                    output.extend(lines[2].encode("utf-8"))
                    byteCount += len(lines[2])
                    while byteCount < 12:
                        output += b'\x00'
                        byteCount += 1

                    if len(lines[0]) > 14:
                        print("error: row too long: " + lines[0] + " (line " + str(lineCount) + ")")
                        errorCount += 1
                    if len(lines[1]) > 14:
                        print("error: row too long: " + lines[1] + " (line " + str(lineCount) + ")")
                        errorCount += 1
                    if len(lines[2]) > 12:
                        print("error: row too long: " + lines[2] + " (line " + str(lineCount) + ")")
                        errorCount += 1
                else:
                    byteCount = 0
                    for i in range(math.ceil((12 - min(len(longestLine),12)) / 2)):
                        output += b'\x00'
                        byteCount += 1
                    output.extend(lines[0].encode("utf-8"))
                    byteCount += len(lines[0])
                    while byteCount < 12:
                        output += b'\x00'
                        byteCount += 1

                    byteCount = 0
                    linePosition = 14
                    if len(longestLine) == 14 and len(lines[1]) < 14:
                        linePosition = 13
                    else:
                        linePosition = len(longestLine)
                    for i in range(math.ceil((14 - linePosition) / 2)):
                        output += b'\x00'
                        byteCount += 1
                    output.extend(lines[1].encode("utf-8"))
                    byteCount += len(lines[1])
                    while byteCount < 14:
                        output += b'\x00'
                        byteCount += 1

                    byteCount = 0
                    linePosition = 14
                    if len(longestLine) == 14 and len(lines[2]) < 14:
                        linePosition = 13
                    else:
                        linePosition = len(longestLine)
                    for i in range(math.ceil((14 - linePosition) / 2)):
                        output += b'\x00'
                        byteCount += 1
                    output.extend(lines[2].encode("utf-8"))
                    byteCount += len(lines[2])
                    while byteCount < 14:
                        output += b'\x00'
                        byteCount += 1

                    output += line4ba

                    if len(lines[0]) > 12:
                        print("error: row too long: " + lines[0] + " (line " + str(lineCount) + ")")
                        errorCount += 1
                    if len(lines[1]) > 14:
                        print("error: row too long: " + lines[1] + " (line " + str(lineCount) + ")")
                        errorCount += 1
                    if len(lines[2]) > 14:
                        print("error: row too long: " + lines[2] + " (line " + str(lineCount) + ")")
                        errorCount += 1

            if len(lines) == 4:
                byteCount = 0
                for i in range(math.ceil((12 - min(len(longestLine), 12)) / 2)):
                    output += b'\x00'
                    byteCount += 1
                output.extend(lines[0].encode("utf-8"))
                byteCount += len(lines[0])
                while byteCount < 12:
                    output += b'\x00'
                    byteCount += 1

                byteCount = 0
                linePosition = 14
                if len(longestLine) == 14 and len(lines[1]) < 14:
                    linePosition = 13
                else:
                    linePosition = len(longestLine)
                for i in range(math.ceil((14 - linePosition) / 2)):
                    output += b'\x00'
                    byteCount += 1
                output.extend(lines[1].encode("utf-8"))
                byteCount += len(lines[1])
                while byteCount < 14:
                    output += b'\x00'
                    byteCount += 1

                byteCount = 0
                linePosition = 14
                if len(longestLine) == 14 and len(lines[2]) < 14:
                    linePosition = 13
                else:
                    linePosition = len(longestLine)
                for i in range(math.ceil((14 - linePosition) / 2)):
                    output += b'\x00'
                    byteCount += 1
                output.extend(lines[2].encode("utf-8"))
                byteCount += len(lines[2])
                while byteCount < 14:
                    output += b'\x00'
                    byteCount += 1

                byteCount = 0
                for i in range(math.ceil((12 - min(len(longestLine), 12)) / 2)):
                    output += b'\x00'
                    byteCount += 1
                output.extend(lines[3].encode("utf-8"))
                byteCount += len(lines[3])
                while byteCount < 12:
                    output += b'\x00'
                    byteCount += 1

                if len(lines[0]) > 12:
                    print("error: row too long: " + lines[0] + " (line " + str(lineCount) + ")")
                    errorCount += 1
                if len(lines[1]) > 14:
                    print("error: row too long: " + lines[1] + " (line " + str(lineCount) + ")")
                    errorCount += 1
                if len(lines[2]) > 14:
                    print("error: row too long: " + lines[2] + " (line " + str(lineCount) + ")")
                    errorCount += 1
                if len(lines[3]) > 12:
                    print("error: row too long: " + lines[3] + " (line " + str(lineCount) + ")")
                    errorCount += 1

            output += category

            if len(choices) == 1:
                if mode == 1:
                    for i in range(120):
                        output += b'\x00'
                    output += b'\x0D\x0A'
                else:
                    for i in range(122):
                        output += b'\x00'
            else:
                output += choices[1].encode("utf=8")
                if mode == 1:
                    for i in range(120 - len(choices[1])):
                        output += b'\x00'
                    output += b'\x0D\x0A'
                else:
                    for i in range(122 - len(choices[1])):
                        output += b'\x00'

if mode == 0:
    output = output[:-2]

if errorCount == 0:
    if mode == 1:
        with open(outputFolder + "PUZZLEB.BIN", "wb") as binary_file:
            binary_file.write(output)
        print ("PUZZLEB.BIN created!")
    else:
        with open(outputFolder + "PUZZLES.BIN", "wb") as binary_file:
            binary_file.write(output)
        print ("PUZZLES.BIN created!")

else:
    print ("Fix the errors shown above, then run the program again.")