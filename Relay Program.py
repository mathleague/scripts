import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
# retrives the credentials from the creds json file
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds) # authenticate with Google

roundNum = input("Enter the round you want to look at: ")
fileName = "relay"+roundNum+".tex"
file = open(fileName,"r")
def printData(questions,answers,realAnswers):
    sheetName = "Copy of Mathleague Assembly Sheet"
    relaySheet = client.open(sheetName).worksheet('Relay')
    for i in range(len(questions)):
        cells = ['A','B','C','H','K']
        for j in range(len(cells)):
            cells[j] += str(i+2) # start on second row
        relaySheet.update_acell(cells[0],roundNum)
        relayRound = int((i+3)/3)
        questionNum = i%3+1
        relaySheet.update_acell(cells[1],"Relay")
        relaySheet.update_acell(cells[2],str(relayRound)+"-"+str(questionNum))
        relaySheet.update_acell(cells[3],questions[i])
        relaySheet.update_acell(cells[4],str(answers[i])+" & (K = "+str(realAnswers[i])+")")

def cleanString(string):
    lastInd = 0
    string = string[16+len(numbers[i]):] 
    while string.count("\n") > 0:
        ind1 = string.index("\n",lastInd)
        string = string[:ind1]+string[ind1+1:]
        lastInd = ind1
    lastInd = 0
    while string.count("\t") > 0:
        ind1 = string.index("\t",lastInd)
        string = string[:ind1]+string[ind1+1:]
        lastInd = ind1
    for j in range(len(string)-1):
        if string[j:j+1] == " " and string[j+1:j+2] == " ":
            string = string[:j]+string[j+1:]
    return string[:len(string)-1] # gets rid of the last }

fileLines = []
numbers = ["one","two","three","four","five","six","seven","eight","nine","ten"]
numbers.append("eleven")
numbers.append("twelve")
numbers.append("thirteen")
numbers.append("fourteen")
numbers.append("fifteen")
for line in file:
    if line.count("DON'T CHANGE ANYTHING BELOW HERE!") > 0:
        break
    fileLines.append(line)

stopIndices = []
questions = []
answers = []
realAnswers = []
lastStop = 0
#for i in range(len(fileLines)):
#    print(fileLines[i])
questionTexts = ["" for i in range(15)] # holds all the questions
answerTexts = ["" for i in range(15)] # holds all the answers
realAnswerTexts = ["" for i in range(15)] # holds all the real answers
for i in range(len(numbers)):
    ind1,ind2,ind3 = -1,-1,-1
    for j in range(lastStop,len(fileLines)):
        if fileLines[j].count("newcommand{") > 0 and fileLines[j].count("q"+numbers[i]) > 0:
            ind1 = j
        if fileLines[j].count("newcommand{") > 0 and fileLines[j].count("a"+numbers[i]) > 0:
            ind2 = j
        if fileLines[j].count("newcommand{") > 0 and fileLines[j].count("k"+numbers[i]) > 0:
            ind3 = j
        if ind1 > -1 and ind2 > -1 and ind3 > -1:
            break
    if ind1 > -1 and ind2 > -1 and ind3 > -1:
        lastStop = ind3+1
        print("found %d %d %d at %d" %(ind1,ind2,ind3,i))       
        questions.append(ind1)
        answers.append(ind2)
        realAnswers.append(ind3)    
    else:
        print("error at %d: %d %d %d" %(i,ind1,ind2,ind3))   
        exit()

questions.append(len(fileLines)) # last line it can look until       
for i in range(15):
    for j in range(questions[i],answers[i]):
        questionTexts[i] += fileLines[j]
    for j in range(answers[i],realAnswers[i]):
        answerTexts[i] += fileLines[j]
    for j in range(realAnswers[i],questions[i+1]):
        realAnswerTexts[i] += fileLines[j]

for i in range(len(numbers)):
    lastInd = 0
    questionTexts[i] = cleanString(questionTexts[i])
    answerTexts[i] = cleanString(answerTexts[i])
    realAnswerTexts[i] = cleanString(realAnswerTexts[i])
    
print(questionTexts[0])
print(questionTexts[0].count("\n"))
print(realAnswerTexts[14])
outputFile = open("writer.txt","w")
printData(questionTexts,answerTexts,realAnswerTexts)
for i in range(len(numbers)):
    outputFile.write(questionTexts[i]+"\n")
file.close()
outputFile.close()

