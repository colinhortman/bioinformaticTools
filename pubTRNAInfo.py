

# A Program dedicated to doing research.
# By: Kyle Lee Kaminski & Colin James Hortman


# This program will utilize three classes.
# One class is simply a FastAreader, original written by David Bernick, that has been edited to make a new file that is
#  adds an additional line of PubMed indices related to said FastA file.
# The second class (2 classes) is a bioPython class capable of doing two things; breaking up a FastA file into component parts, and
#  The 2B class will be doing a search across PubMed, more in the future, for related articles.
# The third class is quite special.  Max Hauseler, a researcher at UCSC, has graciously worked with us to develop a
#  system by which code is sent, via a pipeline developed at UCSC, in a file that starts with a species name and is
#  followed by a FastA file.  Dr. Hauseler's code aims to take in the species' name, scan across several databases to
#  return a list of ranked hits.
# pubTRNAInfo is a class that utilizes the final products of the search writen by Dr. Hauseler with the search results
#  of the more basic PubMed search.  These results are then printed back into a file that contains: headers, same as
#  fastA format, and PubMed IDs.

# A hopeful goal of this program is then to take the results and create a heat map of the tRNA isotypes based on the
#  number of entry hits to each isotype.


# Can't tell you how excited I am to finally be starting this code.  It has been one hell of a quarter. - 5/16 CJH
'''

'
reldate set to 365

only last year of publications will return.
'

'''

from Bio import Entrez
from Bio.Entrez import efetch
Entrez.email = "kkaminsk@ucsc.edu"

class pubmedRefined:

    terms_pmids_HISTORY = {} # How can I make this into a db?

    def __init__(self, searchTerms = ['CANTFINDINPUBMED', 'THISISCRAYCRAY']):
        self.searchTerms = searchTerms

        #self.reldate = myReldate

    def numSearch(self, searchString):  # 18250 means the defult search last 50 years (50*365)
        if frozenset(self.searchTerms) in pubmedRefined.terms_pmids_HISTORY:
            return len(pubmedRefined.terms_pmids_HISTORY[frozenset(self.searchTerms)])
        myTerm = searchString
        data = Entrez.esearch(db="pubmed", term=myTerm)
        res = Entrez.read(data)
        pmids = res["IdList"]
        pubmedRefined.terms_pmids_HISTORY[frozenset(self.searchTerms)] = pmids
        return len(pmids)

    def doSearch(self, searchString):
        if frozenset(self.searchTerms) in pubmedRefined.terms_pmids_HISTORY:
            return pubmedRefined.terms_pmids_HISTORY[frozenset(self.searchTerms)]

        myTerm = searchString
        Entrez.email = "kkaminsk@ucsc.edu"
        data = Entrez.esearch(db="pubmed", term=myTerm)
        res = Entrez.read(data)
        pmids = res["IdList"]
        pubmedRefined.terms_pmids_HISTORY[frozenset(self.searchTerms)] = pmids
        return (pmids)

    def combineTerms(self):
        mysearchString = ''
        for aTerm in self.searchTerms:
            mysearchString += aTerm+' '
        return mysearchString

    def broaden(self):
        self.searchTerms.pop()

    def findOne(self):
        '''
        self.searchTerms is the most up to date list of search terms.
        :return: list of PMIDs
        '''
        stringSearch = self.combineTerms()
        PMIDcounter = self.numSearch(stringSearch) # Do an initial narrow search to see if any results are found.
        while PMIDcounter < 1:
            self.broaden()
            stringSearch = self.combineTerms()
            PMIDcounter = self.numSearch(stringSearch)
            #if PMIDcounter > 0:
            #    print('num of PMIDs found with search: "{0}" = {1}'.format(stringSearch, PMIDcounter))

        return self.doSearch(stringSearch) #returns list of PMIDs with stringSearch as kywrds

    def firstXlines(self, IDList, xLines ,unique=True):

        def fetch_abstract(pmid):
            '''
            This method was originally written by Karol.  Colin Hortman added the try/except block to handle articles that
            abstracts were not found
            http://stackoverflow.com/questions/17409107/obtaining-data-from-pubmed-using-python

            :param pmid: PubMed ID
            :return: Abstract ( will return as StringElement but behaves mostly like a string )
            '''
            handle = efetch(db='pubmed', id=pmid, retmode='xml')
            xml_data = Entrez.read(handle)[0]
            try:
                article = xml_data['MedlineCitation']['Article']
                try:
                    abstract = article['Abstract']['AbstractText'][0]
                    return abstract
                except KeyError:
                    pass
                    #print('No Abstract found for PMID: ', pmid)
            except IndexError:
                return None
            return None
        '''
        The input findOneStr should be the list of search terms stringSearch returned in findOne()
        findOne() should have been run already.

        This method sorts the abstracts returned from the list of PMIDs from findOne().
        It splits the abstract into sentences.

        It will answer the question: are findOneStr (search terms) in the first xLines
        of the abstract.
        It will answer with a list of PMIDs that contain the inputed search terms in
        the first xLines of the abstract
        :param findOneStr:
        :return:
        '''
        myTexts = []
        #print('I made it to this IDlist1234:',IDList)
        for id in IDList:
            myAb = fetch_abstract(id)
            try:
                sentList = myAb.split('.')
            except:
                break
            foundTerm = False

            for sent in sentList[0:xLines]: # For each sentance
                sent = sent.upper()
                for term in self.searchTerms: # Look for one of terms
                    term = term.upper()
                    if 'OR' in term:
                        myOrList = term.replace(' ','')
                        myOrList = myOrList.split('OR')
                        myOrList[0] = myOrList[0][1:]
                        myOrList[-1] = myOrList[-1][:-1]
                        #print('orList:',myOrList)
                        for miniTerm in myOrList:
                            if miniTerm in sent:  # If you find a term
                                foundTerm = True  # The abstract is a keeper.
                                if foundTerm: break  # Get out of this mess!

                    if term in sent: # If you find a term
                        foundTerm = True # The abstract is a keeper.
                        if foundTerm: break #Get out of this mess!
                if foundTerm:
                    break # You found a term!

            if foundTerm:
                myTexts.append(id)
            else:
                pass

        if len(myTexts) > 0:
            return myTexts
        else:
            return 'None Found'
        '''
        if unique: myTexts = set(myTexts) # Delete all identical abstracts, they are not specific.

        myTexts = list(myTexts)
        print(myTexts)
        splitTexts = [] #list[ [ab1 [abstract1Sent1], [abstractSent2].... ] ]
        for abstract in myTexts:
            splitTexts.append([abstract.split('.')])

        foundTerm = False
        top5 = []
        for abstract in splitTexts:
            for sent in abstract[0:xLines]:
                self.searchTerms #list of searchTerms
                for term in self.searchTerms:
                    if term in sent
                        foundTerm = True
                        if foundTerm: break

                if foundTerm: break

            if foundTerm:
                top5.append()
                break



        print(splitTexts)

        return (splitTexts)
        '''

    #def findTitle(self, pmid):
    #    handle = Entrez.efetch("pubmed", id=pmid, retmode="xml")
    #    record = Entrez.parse(handle)
    #    handle.close()
    #    title = record['MedlineCitation']['Article']['ArticleTitle']
    #    year = record['MedlineCitation']['Article']['ArticleTitle']
    #    return title

class pmidTermFind:

    pmid_xmlData_HISTORY = {}

    def __init__(self, pmid):
        self.pmid = pmid
        Entrez.email = 'kkaminsk@ucsc.edu'

        inCache = False
        if self.pmid in pmidTermFind.pmid_xmlData_HISTORY: # If ID in cache
            self.xml_data = pmidTermFind.pmid_xmlData_HISTORY[self.pmid]
            inCache = True

        if inCache == False:
            self.handle = efetch(db='pubmed', id=self.pmid, retmode='xml')
            self.xml_data = Entrez.read(self.handle)[0]
            pmidTermFind.pmid_xmlData_HISTORY[pmid] = self.xml_data

    def fetch_abstract(self):
        '''
        This method was originally written by Karol.  Colin Hortman added the try/except block to handle articles that
        abstracts were not found
        http://stackoverflow.com/questions/17409107/obtaining-data-from-pubmed-using-python

        :param pmid: PubMed ID
        :return: Abstract ( will return as StringElement but behaves mostly like a string )
        '''

        #try: # Try finding abstract in hash
        #    abstract = pmidTermFind.pmid_xmlData_HISTORY[self.pmid]
        #    return abstract
        #except:
        #    pass # Not in hash yet

        try:
            article = self.xml_data['MedlineCitation']['Article']
            try:
                abstract = article['Abstract']['AbstractText'][0]
                return abstract
            except KeyError:
                # print('No Abstract found for PMID: ', pmid)
                return 'No Abstract Found'
        except IndexError:
            return 'No Abstract Found'

    def fetch_titleYear(self):
        '''
        Take in a PMID, and return the title and year.

        Based on the fetch_abstract method which was taken and editted from stackoverflow's answer by Karol.  See
        fetch_abstract for more details.

        If either, or both, the title or the year are not found, they will return as None.
        :param pmid: PubMed ID number, if searched on PubMed will bring you straight to article
        :return: title, year ( if none found, will return string 'No year/title found.')
        '''


        try:  # If there is no article hit to the pmid, return None for title and year
            article = self.xml_data['MedlineCitation']['Article']
            try:  # Try to find the title
                title = article['ArticleTitle']  # If found keep it
            except KeyError:  # If no title, title becomes none
                # print('No Abstract found for PMID: ', pmid)
                title = 'No title found.'
            try:  # Try to find the year
                year = self.xml_data['MedlineCitation']['Article']['ArticleDate'][0]['Year']
                # return title, year
            except:  # Try to find the year in a different location
                try:
                    year = self.xml_data['MedlineCitation']['DateCreated']['Year']
                except:  # If no year in either location, return None for year
                    pass
                    year = 'No year found.'
            return title, year
        except IndexError:  # If there is no article hit to the pmid, return None for title and year
            title = 'No title found.'
            try:  # Try to find the year
                year = self.xml_data['MedlineCitation']['Article']['ArticleDate'][0]['Year']
                # return title, year
            except:  # Try to find the year in a different location
                try:
                    year = self.xml_data['MedlineCitation']['DateCreated']['Year']
                except:  # If no year in either location, return None for year
                    pass
                    year = 'No year found.'

        return title, year





# Get a list that is in this order from Kyle
#mySearchList = ['HOMO SAPIENS', 'TRNA', 'LEU', 'AAG', '6-1', 'TRNASCAN', 'SEID:CHR20.TRNA1', 'CHR20:48952342-48952423']
#
#myPubSearcher = pubmedRefined(mySearchList)
#oneOrMoreIDs = myPubSearcher.findOne()
#print(oneOrMoreIDs)

#print('Done')

'''
# Do an initial narrow search to see if any results are found.
myPubSearcher = pubmedRefined(mySearchTerms)
simpleSearch = myPubSearcher.combineTerms()
PMIDcounter = myPubSearcher.numSearch(simpleSearch)
print('num of PMIDs found in "{0}" = {1}'.format(simpleSearch, PMIDcounter))

# Create a while loop that keeps broadening search until at least on entry found.

while PMIDcounter < 1:
    myPubSearcher.broaden()
    simpleSearch = myPubSearcher.combineTerms()
    PMIDcounter = myPubSearcher.numSearch(simpleSearch)
    print('num of PMIDs found with search: "{0}" = {1}'.format(simpleSearch, PMIDcounter))
'''

'''
myPubSearcher.broaden()
simpleSearch = myPubSearcher.combineTerms()
PMIDcounter = myPubSearcher.numSearch(simpleSearch)
print('num of PMIDs found with search: "{0}" = {1}'.format(simpleSearch, PMIDcounter))


myPubSearcher.broaden()
simpleSearch = myPubSearcher.combineTerms()
PMIDcounter = myPubSearcher.numSearch(simpleSearch)
print('num of PMIDs found in "{0}" = {1}'.format(simpleSearch, PMIDcounter))
'''

'''
Program idea:
Let there be a list of search terms x,y,z,q. x being most neccessary, q being least
Add x,y,z,q togther into one string.
Do a search, if there are more than 100 results, do this:
             if there are no results, delete q. (lst.pop)
Repeat search, 100+ do this:
               no results, delete next (lst.pop)
When search results found, print them
'''

'''
A pubmed PMID search and print example:

Entrez.email = "kkaminsk@ucsc.edu"
keywords = ['Gln', 'TTG']

data = Entrez.esearch(db='pubmed', term=['tRNA TTG homo'])
res = Entrez.read(data)
pmids = res['IdList']
print('PMIDS for TTG Gln:',pmids)
'''

'''
from fastaReader import FastAreader

myreader = FastAreader()
for head, seq in myreader.readFasta():
    print(head, seq)

print('I can import Entrez from Bio.')
'''