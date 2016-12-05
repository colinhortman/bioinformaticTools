###
# The purpose of variCount is to count the products that are reported from annotateVcfWithNCBI.py
# Input: File created by annotateVcfWithNCBI.py
# Output: Counts of mutated proteins.
#
# Written by: Colin Hortman
# Note: I hope this set of programs are useful to you, or can be easily modified to do so. Additionally, this program
#  was not built with the intention of being robust, but was a quick script.  I will edit it if I use it again.
# Future directions: Commandline inFiles,
###

class variCount:
    '''
    Count proteins that are mutated.
    '''
    def __init__(self, file):
        self.file = file
        self.productDict = self.readCount()  # A dictionary of productDict[protein] = int(countOfMutationsToProtein)

    def readCount(self):
        with open(self.file) as f:
            fileList = f.readlines()  # Create a list from the lines
            print('There were ' + str(len(fileList)) + ' lines in the '+self.file+' file.')
            i=0
            prodSet = set()
            prodDict = {} #dictionary conatining prodDict[product] = count
            for line in fileList:
                if 'Mutated Spot' in line:
                    prod2 = fileList[i:i+4]
                    prod = fileList[i+2].split(':')[-1]
                    if prod in prodDict.keys():  # Add count if product is already in dictionary.
                        prior = prodDict[prod]
                        prodDict[prod] = prior + 1
                    if prod not in prodDict.keys():  # Add to dictionary if product(protein) not in dictionary.
                        prodDict[prod] = 1
                i+=1
            f.close()  # Close the file to prevent errors.
            return prodDict

# A Method for counting one file at a time: ##  myFile = 'myAnnotate5.txt'
# A Method for counting one file at a time: ##  countProductDict11 = variCount(myFile).productDict
# A Method for counting one file at a time: ##  mySortedList = sorted(countProductDict11.items(), key=lambda x: x[1])
# A Method for counting one file at a time: ##  for item in mySortedList:
# A Method for counting one file at a time: ##      print(item)
# A Method for counting one file at a time: ##  for item in sorted(countProductDict11):
# A Method for counting one file at a time: ##      print(item + str(countProductDict11[item]))

# Below is a method to count many files if your annotation has to be split into parts.
file1 = 'myAnnotate1.txt'
countProductDict1 = variCount(file1).productDict
file2 = 'myAnnotate2.txt'
countProductDict2 = variCount(file2).productDict
file3 = 'myAnnotate3.txt'
countProductDict3 = variCount(file3).productDict
file4 = 'myAnnotate4.txt'
countProductDict4 = variCount(file4).productDict
file5 = 'myAnnotate5.txt'
countProductDict5 = variCount(file5).productDict

finalCount = {} # finalCount[product] = count
listDicts = [countProductDict1, countProductDict2, countProductDict3, countProductDict4, countProductDict5]
for dict in listDicts:  # Join the dictionaries and sum the counts.
    for product in dict.keys():
        if product in finalCount.keys():
            prior = finalCount[product]
            finalCount[product] = prior + dict[product]
        if product not in finalCount.keys():
            finalCount[product] = dict[product]

mySortedList = sorted(finalCount.items(), key=lambda x: x[1])  # Sort the dictionary based on counts, then print.
for item in mySortedList:  # Print a list of the items sorted on the count of the products.
    print(item[0].strip() + ' : '  +str(item[1]))  # Strip the newline character and print a readable count.
# TEST to look at final count structure # print(finalCount)

