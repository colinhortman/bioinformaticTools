# This is a class that will take in a variant isec file and return annotations based on reference genes.
# isec is a BCFtool that can be found here:
#
# The goal of this program is to help identify the proteins that are common among several samples.
#
#
#  Use a redirect of standard out to create a text file.  This file will be used by countVariances.py
#
#Example $py annotateVcfWithNCBI.py >annotationSample1.txt
#
# Written By: Colin Hortman
#  Please comment or add changes where you see necessary.  This was not designed to be a robust program but was a tool
#    that I made for the lab I am working in.
#  Future additions could include: Commandline for inFiles, gather more 'important information', combining this with countVairances
#
#  Warning: This program is memory intensive and may require you to split the annotation text file from NCBI.  My tests
#   could only handle around 200,000 lines.  A good solution to this is parsing through the file in a different way.
#   For my purpose (one species), this was fine.  If you need to do this on many species, it may require some reworking.

import re  # Importing to find numbers in a string.

class getImportant():
    '''
    This class will pull the protein, gene and position of all genes contained within the string.
    '''
    def __init__(self, myString, startPos, endPos):
        self.myString = myString  # String should be concatenated from list of lines following an identification.
        self.myGene = self.getGene()
        self.myProduct = self.getProduct()  # Product = Protein
        self.startPos = startPos
        self.endPos = endPos

    def getGene(self):
        '''
        Method to pull gene from string of
        :return:
        '''
        try:
            geneFirst = self.myString.split('/gene="')
            myGene = geneFirst[1][0:4]
            #TEST# print('Found gene : ' + myGene)
            return myGene
        except:
            return ' '  # Return blank string to not cause errors.

    def getProduct(self):
        try:
            prodSpltList = self.myString.split('/product="')
            myProd = prodSpltList[1][0:-2].replace('"', "") #TEST#print('Found prod : ' + myProd)
            myProd = myProd.split('\n')[0]
            return myProd
        except:
            return ' '

    def meMe(self):
        return [self.startPos, self.endPos, self.myProduct, self.myGene]
    def printMe(self):
        #print('large str:' + self.myString)
        print('Prod: '+self.myProduct)
        print('gene: '+self.myGene)

#MAIN#

with open('sampleCross.txt') as f:  # Open the cross file that you need annotated.
    # sampleCross is the format that comes when an intersection call is created by using the isec bcftool on 2 or more files
    #  Replace this file name with your intersection file
    fileString = f.readlines()  # Create a list from the lines
    print('There were '+str(len(fileString))+ ' lines in the variation file.')
    variantPos = set()
    for item in fileString:  # Count each unique (name or description) line, or start a count, and put in dictionary.
        variantPos.add(item.split()[1])
    f.close()  # Close the file to prevent errors.
print('# positions: ' + str(len(variantPos)) + ' (if not same as number of lines, may cause errors)')

# variantPos contains each posistion of variant.
with open('LAcetotoGenesAndSuch2.txt') as f:  # Read in annotation text file from NCBI. See below for more detail.
    # The file should be replaced with the name of the file you want to
    # An example of the kind of file that can be handled would be the text between "Features" and "ORIGIN" found here: https://www.ncbi.nlm.nih.gov/nuccore/NZ_AP014808.1
    # This text is a complete annotation of the genome.
    # The annotation captures important information about the genes in the genome and predicts hypothetical proteins.

    #fileString = f.readline() # Create a list from the lines
    geneRecord = {} #key: posisiton (list of two numbers) value: getImportant object
    fileList = f.readlines()

    i = 0
    for line in fileList:
        if 'gene' in line and any(char.isdigit() for char in line):
            myGeneLocL = line.split()
            if 'if' in line:
                break
            try:  # Method below inspired by: http://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
                getNumbsFromLine = line.split('..')
                num1 = re.findall(r'\d+', getNumbsFromLine[0])
                try:
                    num2 = re.findall(r'\d+',getNumbsFromLine[1])
                except IndexError:
                    print('Error in '+getNumbsFromLine)
                #TEST#print('numb1 = ' + str(num1)) #print('numb2 = ' + str(num2))
                smallList = fileList[i:i+21]
                largestrSmallList = ''.join(smallList) #TEST#print(largestrSmallList)
                startPos = num1
                endPos = num2
                importInfo = getImportant(largestrSmallList, startPos, endPos)
                #TEST#importInfo.printMe()
                geneRecord[int(num1[0])] = importInfo.meMe()
            except:
                print("ERROR: Skipping 'gene' ID: "+ str(myGeneLocL))
        i+=1
    f.close() # Close the file to prevent errors.

print('Gene Record Made, we have liftoff.\n' )
#variantPos is set of variant posisitions

for startPos in sorted(geneRecord.keys()): #TEST# print(startPos)
    for item in list(variantPos):
        if int(item) < int(geneRecord[startPos][1][0]) and int(item) >  int(geneRecord[startPos][0][0]):
            #print('Well hot damn, we have at least one ID for a gene!')
            print('Mutated Spot: '+item )
            print(str(geneRecord[startPos][0][0])+':'+str(item)+':'+str(geneRecord[startPos][1][0]))
            print('Mutated product: '+geneRecord[startPos][2])
            print('Mutated gene: '+ geneRecord[startPos][3] + '\n')

print('annotateVcfWithNCBI completed with no errors.')  # Tell the user that the program has completed without errors