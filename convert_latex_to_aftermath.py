from num2words import num2words

# converts number to string
def convert_number_to_string(num):
    word = num2words(num)
    word = word.replace("-", "")
    return word.capitalize()
    
release = input("Release: ")
session = input("AfterMath Session: ")

file_name = release + "/" + release + session + " AfterMath Questions.txt"
file = open(file_name, "r")
lines = file.readlines()
output = open(release + "/" + session + "latex.txt", "w")

# print out the latex into the output file
for count in range(30):
    question = convert_number_to_string(count+1)
    text = lines[count][:-1]
    latex = "\\newcommand{\sprintQuestion" + question + "}{" + text + "}"
    print(latex)
    output.write(latex)
    output.write("\n")

file.close()
output.close()
