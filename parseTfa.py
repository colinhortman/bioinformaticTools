
import re # Regex is gonna make this cool and useful.

class Header :

    aa2Long = {
        'ALA': 'Alanine', 'GLY': 'Glycine', 'MET': 'Methionine', 'SER': 'Serine', 'CYS': 'Cystine',
        'HIS': 'Histidine', 'ASN': 'Asparagine', 'THR': 'Threonine', 'ASP': 'Aspartate', 'ILE': 'Isoleucine',
        'PRO': 'Proline', 'VAL': 'Valine', 'GLU': 'Glutamate', 'K': 'Lysine', 'GLN': 'Glutamine',
        'TRY': 'Tryptophan', 'PHE': 'Phenylalanine', 'LEU': 'Leucine', 'ARG': 'Arginine', 'TYR': 'Tyrosine'
    }
    rnaCodonTable = {
    # RNA codon table
    # U
    'UUU': 'F', 'UCU': 'S', 'UAU': 'Y', 'UGU': 'C',  # UxU
    'UUC': 'F', 'UCC': 'S', 'UAC': 'Y', 'UGC': 'C',  # UxC
    'UUA': 'L', 'UCA': 'S', 'UAA': '-', 'UGA': '-',  # UxA
    'UUG': 'L', 'UCG': 'S', 'UAG': '-', 'UGG': 'W',  # UxG
    # C
    'CUU': 'L', 'CCU': 'P', 'CAU': 'H', 'CGU': 'R',  # CxU
    'CUC': 'L', 'CCC': 'P', 'CAC': 'H', 'CGC': 'R',  # CxC
    'CUA': 'L', 'CCA': 'P', 'CAA': 'Q', 'CGA': 'R',  # CxA
    'CUG': 'L', 'CCG': 'P', 'CAG': 'Q', 'CGG': 'R',  # CxG
    # A
    'AUU': 'I', 'ACU': 'T', 'AAU': 'N', 'AGU': 'S',  # AxU
    'AUC': 'I', 'ACC': 'T', 'AAC': 'N', 'AGC': 'S',  # AxC
    'AUA': 'I', 'ACA': 'T', 'AAA': 'K', 'AGA': 'R',  # AxA
    'AUG': 'M', 'ACG': 'T', 'AAG': 'K', 'AGG': 'R',  # AxG
    # G
    'GUU': 'V', 'GCU': 'A', 'GAU': 'D', 'GGU': 'G',  # GxU
    'GUC': 'V', 'GCC': 'A', 'GAC': 'D', 'GGC': 'G',  # GxC
    'GUA': 'V', 'GCA': 'A', 'GAA': 'E', 'GGA': 'G',  # GxA
    'GUG': 'V', 'GCG': 'A', 'GAG': 'E', 'GGG': 'G'  # GxG
    }
    dnaCodonTable = {key.replace('U','T'):value for key, value in rnaCodonTable.items()}

    otherNameDictionary = {
    'HOMO SAPIENS' : '(HOMO SAPIEN OR HUMAN OR HOMO SAPIEN SAPIENS OR HOMO SAPIENS)',
    'MUS MUSCULUS' : '(MUS MUSCULUS OR MOUSE OR MICE)',
    'SACCHAROMYCES CEREVISIAE' : '(SACCHAROMYCES CEREVISIAE OR YEAST)',
    'ESCHERICHIA COLI STR K 12 SUBSTR MG1655' : '(ESCHERICHIA COLI STR K-12 SUBSTR MG1655 OR ESCHERICHIA COLI OR E. COLI)',
    'CAENORHABDITIS ELEGANS' : '(C. ELEGANS OR CAENORHABDITIS ELEGANS OR ROUNDWORM)',
    'DROSOPHILA MELANOGASTER' : '(DROSOPHILA MELANOGASTER OR FLY OR DROSOPHILA)'
    }

    def __init__(self, s):
        self.s = s
        self.f = ''.join(self.s).split()
        self.h = ''.join(self.f).upper()
        if 'DROSOPHILA' in self.h:
            if 'UND' in self.h:
                 self.b = self.makeHeaderListUndDros(self.h)
        if 'HALOFERAX' in self.h:
            self.b = self.makeHeaderListHalo(self.h)
        else:
            self.b = self.makeHeaderListNormal(self.h)
            
    def makeHeaderListHalo(self, str):
        signify = True
        c = str.replace('>','-')
        d = c.replace('_', '-')
        e = d.replace(')','-')
        f = e.replace('(','-')
        g = f.replace('+','-')
        h = g.split('-')
        h[0] = (h[0]+' '+ h[1] + ' ' +h[2])
        h.remove(h[1])
        h.remove(h[1])
        # Bundle the family-# naming system Dr. Lowe has invented. #See João Silva's answer at http://stackoverflow.com/questions/1450897/python-removing-characters-except-digits-from-st
        h[1] = 'TRNA'
        money = h[2][:3]
        honey = h[2][3:]
        h = list(filter(None, h)) #filters out any empty strings
        h.pop()
        h.pop()
        h.pop()
        heyThere = h.pop()
        i = h[5].split(':')
        reallyHeyThere = (heyThere + '-' + i[1])
        h.pop()
        h.pop()
        whatsUp = h.pop()
        h.pop()
        h.append(money)
        h.append(honey)
        h.append(whatsUp)
        h.append(reallyHeyThere)    
        h = self.orLong(h)
        h = self.orRNA(h)
        return h
        
    def makeHeaderListNormal(self, str):
        signify = True
        c = str.replace('>','-')
        d = c.replace('_', '-')
        e = d.replace(')','-')
        f = e.replace('(','-')
        g = f.replace('+','-')
        h = g.split('-')
        try:
            h.remove('NMT')
        except:
            pass
        if 'ESCHERICHIA' in h:
            h[0] = (h[0]+' '+ h[1] +' ' + h[2]+ ' '+ h[3] +' ' + h[4]+' '+ h[5] +' ' +h[6] )
            h[0] = Header.otherNameDictionary[h[0]]
            h.remove(h[1])
            h.remove(h[1])
            h.remove(h[1])
            h.remove(h[1])
            h.remove(h[1])
            h.remove(h[1])
        else:
            h[0] = (h[0]+' '+ h[1])
            try:
                h[0] = Header.otherNameDictionary[h[0]]
            except:
                pass
            h.remove(h[1])
        # Bundle the family-# naming system Dr. Lowe has invented. #See João Silva's answer at http://stackoverflow.com/questions/1450897/python-removing-characters-except-digits-from-string
        h[4] = (re.sub(r"\D", "", h[4])+'-'+h[5]) # re.sub(things) takes away anything but digits. The string 'chr' was found, this was a 'placeholder' according to Todd Lowe.
        h.remove(h[5])
        h.pop()
        h[7] = (h[7] +'-'+h[8]) #condense chromosome placement
        h.remove(h[8])
        h = list(filter(None, h))
        h.pop()
        h.pop()
        if h[5] == 'TRNASCAN':
            h.remove(h[5])
            g = h[5].split(':')
            h[5] =  g[1] #'TRNASCAN-SE ID: ' +
        if 'CHR' not in h[6]:
            h.remove(h[6])
        i = h[6].split(':')
        try:
            h[6] = i[1]
        except:
            pass
        
        if 'UNDET' in h:
            h[2] = '(UNDETERMINED OR UNDETERMINED AMINO ACID OR UNDETERMINED ANTICODON)'
            h.remove(h[3])
            signify = False
            
        if 'UND' in h and signify == True:
            h[2] = '(UNDETERMINED OR UNDETERMINED AMINO ACID OR UNDETERMINED ANTICODON)'
            h.remove(h[3])
            signify = False
            
        if 'UNDET???' in h and signify == True:
            h[2] = '(UNDETERMINED OR UNDETERMINED AMINO ACID OR UNDETERMINED ANTICODON)'
            h.remove(h[3])
            
        h = self.orLong(h)
        h = self.orRNA(h)
        return h
    
    def makeHeaderListUndDros(self, str):
        c = str.replace('>','-')
        d = c.replace('_', '-')
        e = d.replace(')','-')
        f = e.replace('(','-')
        g = f.replace('+','-')
        h = g.split('-')
        h[0] = (h[0]+' '+ h[1])
        h[0] = Header.otherNameDictionary[h[0]]
        h.remove(h[1])
        try:
            h.remove('NMT')
        except:
            pass
        # Bundle the family-# naming system Dr. Lowe has invented. #See João Silva's answer at http://stackoverflow.com/questions/1450897/python-removing-characters-except-digits-from-string
        h[2] = '(UNDETERMINED OR UNDETERMINED AMINO ACID OR UNDETERMINED ANTICODON)'
        h.remove(h[1])
        h.remove(h[3])
        l = h[3].split(':')
        try:
            h[3] = (l[1] + '-' + h[4])
        except:
            pass

        h = self.orLong(h)
        h = self.orRNA(h)
        h.pop()
        h.pop()
        h.pop()
        h.pop()
        h.pop()
        h.pop()
        
        return h
        
    
    def orLong(self, list):
        i=0
        for item in list:

            if item in Header.aa2Long.keys():
                list[i] = '('+item + ' OR ' +Header.aa2Long[item]+')'
                #list.insert(i,  'OR '+ Header.aa2Long[item])
            i += 1
        return list

    def orRNA(self, list):
        '''
        Converts a dnaSequnce into rna and also adds a reverse complement
        :param list: search term list
        :return: search tem list that replaced anticodon with codon with ' OR ' seperation
        '''
        #print("i made it to orRNA") # a test to see if orRNA is called or an error occurs before call
        i = 0
        for item in list:
            #print('Considering : ', item) # A test to see if orRNA was working, spec. if this loop was working
            try:
                doesItReallyWork = Header.rnaCodonTable[item]
                dnaItem = item.replace('U', 'T')
                complement = {'A': 'U', 'C': 'G', 'G': 'C', 'U': 'A'}
                seq = item
                revCo = "".join(complement.get(base, base) for base in reversed(seq))

                list[i] = '(' + item + ' OR ' + rnaItem + ' OR ' + revCo + ')'                

            except:
                pass
            try:
                # Rev Comp methods brought to you by: http://stackoverflow.com/questions/25188968/reverse-complement-of-dna-strand-using-python
                doesItWork = Header.dnaCodonTable[item]
                rnaItem = item.replace('T', 'U')
                complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
                seq = item
                revCo = "".join(complement.get(base, base) for base in reversed(seq))

                list[i] = '(' + item + ' OR ' + rnaItem + ' OR ' + revCo + ')'

            except:
                pass

            i+=1

        return list



