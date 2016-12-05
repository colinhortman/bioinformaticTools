
from fastaReader import FastAreader # To read fastA files

# Bring in BioPython!
from pubTRNAInfo import pubmedRefined, pmidTermFind
from Bio import Entrez
from Bio.Entrez import efetch, read
from Bio.Seq import Seq

from parseTfa import Header # Bring in the fastA cleaner that breaks down fasta headers into a list of search terms

numHits = 3 # Maximum number of printed ID/Title/Year/Abstract
xLines = 4
reldate = 18250 # 50 years
#def fetch_abstract(pmid):
#    '''
#    This method was originally written by Karol.  Colin Hortman added the try/except block to handle articles that
#    abstracts were not found
#    http://stackoverflow.com/questions/17409107/obtaining-data-from-pubmed-using-python
#
#    :param pmid: PubMed ID
#    :return: Abstract ( will return as StringElement but behaves mostly like a string )
#    '''
#    handle = efetch(db='pubmed', id=pmid, retmode='xml')
#    xml_data = read(handle)[0]
#    try:
#        article = xml_data['MedlineCitation']['Article']
#        try:
#            abstract = article['Abstract']['AbstractText'][0]
#            return abstract
#        except KeyError:
#            #print('No Abstract found for PMID: ', pmid)
#            return None
#    except IndexError:
#        return None

#def fetch_titleYear(pmid):
#    '''
#    Take in a PMID, and return the title and year.
#
#    Based on the fetch_abstract method which was taken and editted from stackoverflow's answer by Karol.  See
#    fetch_abstract for more details.
#
#    If either, or both, the title or the year are not found, they will return as None.
#    :param pmid: PubMed ID number, if searched on PubMed will bring you straight to article
#    :return: title, year ( if none found, will return string 'No year/title found.')
#    '''
#    handle = efetch(db='pubmed', id=pmid, retmode='xml')
#    xml_data = read(handle)[0]
#    try: # If there is no article hit to the pmid, return None for title and year
#        article = xml_data['MedlineCitation']['Article']
#        try: # Try to find the title
#            title = article['ArticleTitle'] # If found keep it
#        except KeyError: # If no title, title becomes none
#            #print('No Abstract found for PMID: ', pmid)
#            title = 'No title found.'
#        try:  # Try to find the year
#            year = xml_data['MedlineCitation']['Article']['ArticleDate'][0]['Year']
#            #return title, year
#        except: # Try to find the year in a different location
#            try:
#                year = xml_data['MedlineCitation']['DateCreated']['Year']
#            except: # If no year in either location, return None for year
#                pass
#                year = 'No year found.'
#        return title, year
#    except IndexError: # If there is no article hit to the pmid, return None for title and year
#        title = 'No title found.'
#        try:  # Try to find the year
#            year = xml_data['MedlineCitation']['Article']['ArticleDate'][0]['Year']
#            #return title, year
#        except: # Try to find the year in a different location
#            try:
#                year = xml_data['MedlineCitation']['DateCreated']['Year']
#            except: # If no year in either location, return None for year
#                pass
#                year = 'No year found.'
#
#    return title, year
import sys
sys.maxunicode

myReader = FastAreader() # Leave unspecified to read COMMANDLINE STDIN (<FILE.txt)
for head, seq in myReader.readFasta():
    cleanHead = Header(head) # Create Header class that will break apart fastA header
    mySearchList = cleanHead.b # searchList created by Header class
    myPubSearcher = pubmedRefined(mySearchList) # Create pubMed searcher that has original attribute of the search list
    oneOrMoreIDs = myPubSearcher.findOne() # list of pmids (search will self broaden, until hits, by popping last item in search list)
    # If there are not enough hits for the user to be happy, oneOrMoreIDs will have at least one good ID to handle.




    idOne = oneOrMoreIDs[0] # Keep the first id so you will have at least one paper to deal with later, could/will change
    releIDlist = [] # Relevent list of hits
    if len(oneOrMoreIDs) >= numHits: # If there are at least numHits in list keep numIDlist with numHit number of IDs
        releIDlist = oneOrMoreIDs[0:numHits]

    firstX = myPubSearcher.firstXlines(oneOrMoreIDs, xLines) #firstXlines will return a list (pmids containing search terms in first X lines of abstract) or a string 'None found'

    if type(firstX) == list: # If firstX found hits, they are more likely to be specific.
        idOne = firstX[0] # Change idOne to be the first of firstX, same reason as above.
        if  len(firstX) >= numHits: # If firstX returned enough IDs for the user's liking, change the relevent list
            releIDlist = firstX[0:numHits]


    if len(releIDlist) > 0:
        print('>' + head)
        print(myPubSearcher.combineTerms())

        for id in releIDlist:
            myPMIDtermFinder = pmidTermFind(id)  #
            myFirstAb = myPMIDtermFinder.fetch_abstract()
            title, year = myPMIDtermFinder.fetch_titleYear()

            print(id, end='\t')
            print(year, end='\t')
            print(title, end='\t')
            print(myFirstAb.encode("utf-8", errors = 'ignore')) #.encode("utf-8")

    else:
        myPMIDtermFinder = pmidTermFind(idOne) #
        myFirstAb = myPMIDtermFinder.fetch_abstract()
        title, year = myPMIDtermFinder.fetch_titleYear()
        #print(title, year)

        print('>'+head)
        print(myPubSearcher.combineTerms())
        print(idOne, end='\t')
        print(year, end='\t')
        print(title, end='\t')
        print(myFirstAb.encode("utf-8", errors='ignore')) #.encode("utf-8", error = 'ignore')


    '''
    chars_per_line = 80
    for i in range(0, len(myFirstAb), chars_per_line): # Code stolen from Joel Cornett :http://stackoverflow.com/questions/14349814/print-only-a-certain-number-of-characters-in-python
        print (myFirstAb[i:i + chars_per_line])
    #sumSearch= Entrez.esummary(db='pubmed', id= idOne)
    #record = Entrez.read(sumSearch)
    #print(record[0]['abstract'])
    print('loooooooooooooooooop')
    '''


