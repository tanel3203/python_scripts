
#####################################################
# 1. data import from file
# 2. data standardization
#   2.1. headings imported to array "headList"
#   2.1. content imported to array "contentList"
#####################################################

# \t - tab
# \s - space
# \n - newline



###  Read in file
myFile = open('C:/Python27/Scripts/andmed_mockup.tsv')
myDoc = myFile.read()
print "Started reading in the given file!"
print ""

###  Write TITLES to array
headList = []
print "Started heading separation..."
count = 1

while count == 1:
    
    # Check if time to end loop
    if "\t" not in myDoc:
        count = 2
        break

    # Get the first word out of string
    if myDoc.index("\t") > myDoc.index("\n"):
        currentHeading = myDoc.split("\n",1)[0]
        # Add the word to a new list
        headList.append(currentHeading)
        # Remove the first word from the initial list
        myDoc = myDoc[len(headList[-1])+1:]
        break
    
    else:
        currentHeading = myDoc.split("\t",1)[0]

    # Add the word to a new list
    headList.append(currentHeading)

        
    # Remove the first word from the initial list
    myDoc = myDoc[len(headList[-1])+1:]



print "Heading separation done"
print ""

###  Write CONTENT to array
contentList = []
print "Started content separation..."
count = 1

while count < 3:

    # Get the first word out of string
    if "\n" in myDoc:
        if myDoc.index("\t") > myDoc.index("\n"):
            currentWord = myDoc.split("\n",1)[0]
            
        elif myDoc.index("\t") < myDoc.index("\n"):
            currentWord = myDoc.split("\t",1)[0]
            
    elif "\t" in myDoc:
        currentWord = myDoc.split("\t",1)[0]
        
    else:
        currentWord = myDoc
        
    # Add the word to a new list
    contentList.append(currentWord)
    # Remove the first word from the initial list
    myDoc = myDoc[(len(contentList[-1])+1):]
    
    # Check if time to end loop
    if "\t" not in myDoc:
        count +=1

print "Content separation done"
print ""
print "File is processed!"
print " "
print "               ~~~~~~~~~~~~~~~~~~~~~~~~"
print "                ###### EXAMPLE ########"
print "               ~~~~~~~~~~~~~~~~~~~~~~~~"
print "Let's get data for a column in a seven column array: "
print " "
var = raw_input("Enter column (1-7): ")
prepared_var = int(var)-1
print headList[prepared_var]
print contentList[prepared_var::7]
