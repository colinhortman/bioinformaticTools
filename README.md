# bioinformaticTools
This is a collection of tools that I created during my time at UCSC.  Many tools were assignments so they will not be listed on this page.  For this folder, the two places I wrote the programs for are: final project for class BME160 (Programming for Biology: Python) and Nader Pourmand lab.  There is no research data attached to the files or samples. The are occasionally test files attached but have been made very small or changed in significant ways as to not give away research.  I hope you find these tools helpful, although they are probably for niche tests and research. Enjoy!

## BME160 Final Project - Research on FastA file
### Co-programming assignmen: Colin Hortman and Kyle Kaminski 
Todd Lowe’s GtRNAdb (genomic tRNA database) is one of the world’s leading research collections for tRNA’s. A vast number of researchers and scientists use the GtRNAdb as a reliable source for specific tRNA gene location, gene sequence, etc. For our final project for BME 160 ‘Biology Research Programming’, we ( Kyle Kaminski and Colin Hortman) worked in collaboration with Todd Lowe to try and improve the GtRNAdb. Currently, there is no presented connections between a tRNA present in the GtRNAdb and research involving that specific tRNA (specific to a particular species). We set out to create a research connection to GtRNAdb tRNA’s under the guidance of Todd Lowe (to the extent of working in his undergraduate research group: the Genome Corps). We have designed a python program that takes in fastA files from the GtRNAdb and searches for relevant research for a specific tRNA of a specific species. Eventually, we hope that there is a clickable button in the GtRNAdb to provide the user with a list of links to relevant PubMed cited research literature. What we have developed is a program that takes in GtRNA fastA file and outputs a list of PubMed research articles including: the PubMed article title, the PubMed ID, and the PubMed article abstract in a separate .txt file. 

## annotateVcfFromNCBI.py
 This is a class that will take in a variant isec file and return annotations based on reference genes.
 isec is a BCFtool that can be found here: https://samtools.github.io/bcftools/bcftools-man.html#isec
### The goal of this program is to help identify the proteins that are common among several samples.
  Use a redirect of standard out to create a text file.  This file will be used by countVariances.py
Example $py annotateVcfWithNCBI.py >annotationSample1.txt
###  Warning: 
This program is memory intensive and may require you to split the annotation text file from NCBI.  My tests could only handle around 200,000 lines.  A good solution to this is parsing through the file in a different way.  For my purpose (one species), this was fine.  If you need to do this on many species, it may require some reworking.

## countVariances.py
The purpose of variCount is to count the products that are reported from annotateVcfWithNCBI.py
 Input: File created by annotateVcfWithNCBI.py
 Output: Counts of mutated proteins.
 Note: I hope this set of programs are useful to you, or can be easily modified to do so. Additionally, this program was not built with the intention of being robust, but was a quick script.  I will edit it if I use it again.
 Future directions: Commandline inFiles,

