# -*- coding: <utf-16> -*- 
unicode = True
import codecs

def lengthofcommonprefix (s1, s2):
	length = len(s1)
	if length > len(s2):
		length = len(s2)
	for i in range(length):
		if s1[i] != s2[i]:
			return i
	return length

 
def findcommonsuffix (s1, s2):
	#length is the length of the shorter of the two strings
	length = len(s1)
	if length > len(s2):
		length = len(s2)
	for i in range(-1,-1*length-1,-1):
		if s1[i] != s2[i]:
			return s1[i+1:]
	return s1[-1*length:]
 
#--------------------------------------------------------------------##
#		Main program begins on line 174
#--------------------------------------------------------------------##

import time
import datetime
import operator
import sys
import os
import codecs # for utf8
import string
import copy
from collections import defaultdict
 

#--------------------------------------------------------------------##
#		user modified variables
#--------------------------------------------------------------------##
g_encoding =  "asci"  # "utf8"
 


short_filename 		= "french"
out_short_filename 	= "french"
language		= "french"

short_filename 		= "swahili"
out_short_filename 	= "swahili"
language		= "swahili"

short_filename 		= "english2"
out_short_filename 	= "english2"
language		= "english"


datafolder    		= "../../data/" 
outfolder     		= datafolder + language + "/lxa/"
infolder 		= datafolder + language + '/dx1/'	

infilename 			= infolder  + short_filename     + ".dx1"
stemfilename 			= infolder  + short_filename     + "_stems.txt"
outfile_FSA_name		= outfolder + out_short_filename + "_FSA.txt"
outfile_FSA_graphics_name	= outfolder + out_short_filename + "_FSA_graphics.png"
outfile_log_name 		= outfolder + out_short_filename + "_log.txt"
 
outfile_SF_name 		= outfolder + out_short_filename + "_SF.txt"
outfile_trieLtoR_name 		= outfolder + out_short_filename + "_trieLtoR.txt"
 
outfile_trieRtoL_name 		= outfolder + out_short_filename + "_trieRtoL.txt"
outfile_PF_name 		= outfolder + out_short_filename + "_PF.txt"

if g_encoding == "utf8":
	print "yes utf8"
else:
	FSA_outfile = open (outfile_FSA_name, mode = 'w')
	trieLtoR_outfile = open (outfile_trieLtoR_name, mode = 'w')
	trieRtoL_outfile = open (outfile_trieRtoL_name, mode = 'w')
	SF_outfile =  open (outfile_SF_name, mode = 'w')
	PF_outfile =  open (outfile_PF_name, mode = 'w')
log_file = open(outfile_log_name, "w")


if len(sys.argv) > 1:
	print sys.argv[1]
	infilename = sys.argv[1] 
if not os.path.isfile(infilename):
	print "Warning: ", infilename, " does not exist."
if g_encoding == "utf8":
	infile = codecs.open(infilename, g_encoding = 'utf-8')
else:
	infile = open(infilename) 


#----------------------------------------------------------#
 
SFthreshold = 3

MinimumStemLength 	= 4
MaximumAffixLength 	= 3
MinimumNumberofSigUses 	= 10

print >>log_file, "Language: ", language
print >>log_file, "Minimum Stem Length", MinimumStemLength, "\nMaximum Affix Length", MaximumAffixLength, "\n Minimum Number of Signature uses: ", MinimumNumberofSigUses
print >>log_file, "Date:", 

#--------------------------------------------------------------------##
#		read wordlist (dx1)
#--------------------------------------------------------------------##

filelines= infile.readlines()
WordCounts={}


for line in filelines:
	pieces = line.split()
	word=pieces[0] 	
	if word == '#':
		continue
	word = word.lower()		 
	if (len(pieces)>1):
		WordCounts[word] = int( pieces[1] )
	else:
		WordCounts[word]=1

	 
wordlist = WordCounts.keys()
wordlist.sort()
reversedwordlist = list()

#this weird stuff is here because python changes the underlying string unless you make a deep copy
TempReversedWords = list()
for word in wordlist:
	wordcopy = word[:]
	wordcopy = wordcopy[::-1]
	TempReversedWords.append(wordcopy)
TempReversedWords.sort()
for word in TempReversedWords:
	wordcopy = word[:]
	wordcopy = wordcopy[::-1]
	reversedwordlist.append(wordcopy)
			


WordsBrokenLtoR=dict()
WordsBrokenRtoL=dict()
bl_LtoR = dict() #breaklist
bl_RtoL = dict() #breaklist
for i in range(len(wordlist)):
	bl_LtoR[i]=set()
	bl_RtoL[i]=set()
FoundPrefixes = dict()
FoundSuffixes = dict()
 
 
#--------------------------------------------------------------------##
#		Find breaks in words: L to R
#--------------------------------------------------------------------##

previousword = wordlist[0]
for i in range(1,len(wordlist)):
	thisword= wordlist[i]	 
	thislength = len(thisword)
	m=lengthofcommonprefix(previousword,thisword)
		
	if m < MinimumStemLength:
		previousword=thisword
		continue
	commonprefix = thisword[:m]

	if commonprefix in FoundPrefixes:
		previousword=thisword
		continue	
	else: 
		for j in range(i-1,0,-1):
			if wordlist[j][:m] == commonprefix and m>=MinimumStemLength:
				bl_LtoR[j].add(m)
			else:
				break
		for j in range(i,len(wordlist)):
			if wordlist[j][:m] == commonprefix and m>=MinimumStemLength:
				bl_LtoR[j].add(m)
			else:
				break
	 	FoundPrefixes[commonprefix] = 1
	previousword=thisword
#--------------------------------------------------------------------##
#		Find breaks in words:R to L
#--------------------------------------------------------------------##


if (True):
	
	

	for i in range(1,len(reversedwordlist)):
		thisword= reversedwordlist[i]	 
		thislength = len(thisword)

		commonsuffix = findcommonsuffix(previousword,thisword)
		
		csl= len(commonsuffix)
		if csl < MinimumStemLength:
			previousword=thisword		
			continue

		if commonsuffix in FoundSuffixes:
			previousword=thisword
			continue	
		else: 
			for j in range(i-1,0,-1):
				if reversedwordlist[j].endswith(commonsuffix):
					prefixlength = len(reversedwordlist[j])-csl
					bl_RtoL[j].add(prefixlength)
				else:
					break
			for j in range(i,len(reversedwordlist)):
				if reversedwordlist[j].endswith(commonsuffix):
					prefixlength = len(reversedwordlist[j])-csl
					bl_RtoL[j].add(prefixlength)
				else:
					break
			 	FoundSuffixes[commonsuffix] = 1
		previousword=thisword
		#print
#--------------------------------------------------------------------##
#		Break up each word L to R
#--------------------------------------------------------------------##

maxnumberofpiecesLtoR = 0
for i in range(len(wordlist)):
	thisword= wordlist[i]
	WordsBrokenLtoR[thisword]=list()
	bl_LtoR[i] = list(bl_LtoR[i])
	bl_LtoR[i].sort()
	output = ""
	if len(bl_LtoR[i])==0:
		WordsBrokenLtoR[thisword].append(thisword)
	elif len(bl_LtoR[i]) >  0:
		thispiece=""
		for x in  range(len(thisword)):
			output+=thisword[x] 
			thispiece += thisword[x]
			if x+1 in bl_LtoR[i]:
				output += " "
				WordsBrokenLtoR[thisword].append(thispiece)
				thispiece=""
		if len(thispiece)>0:
			WordsBrokenLtoR[thisword].append(thispiece)
	if len(WordsBrokenLtoR[thisword]) > maxnumberofpiecesLtoR:
		maxnumberofpiecesLtoR = len(WordsBrokenLtoR[thisword])
 
		

print
#--------------------------------------------------------------------##
#		Break up each word R to L
#--------------------------------------------------------------------##
if (True):
	maxnumberofpiecesRtoL = 0
	for i in range(len(reversedwordlist)):
		thisword= reversedwordlist[i]	
		WordsBrokenRtoL[thisword]=list()
		thisbreaklist = list(bl_RtoL[i])
		thislength= len(thisbreaklist)
		thisbreaklist.sort()
		output = ""
		if len(thisbreaklist) >  0:
			thispiece=""
			for x in range(len(thisword)):
				output +=thisword[x]  
				thispiece += thisword[x]  
				if x+1 in thisbreaklist:
					output += " "
					WordsBrokenRtoL[thisword].append(thispiece)
					thispiece=""
			if len(thispiece)>0:
				WordsBrokenRtoL[thisword].append(thispiece)
		if len(WordsBrokenRtoL[thisword]) > maxnumberofpiecesRtoL:
			maxnumberofpiecesRtoL = len(WordsBrokenRtoL[thisword])
		

print
#---------------------------------------------------------------------------------#	
#	Calculate successor frequency
#---------------------------------------------------------------------------------# 
successors=dict()
for i in range(len(wordlist)):	
	wordbeginning = ""	
	thisword= wordlist[i]
	thiswordparsed=WordsBrokenLtoR[thisword]
	thiswordnumberofpieces = len(thiswordparsed)

	if len(WordsBrokenLtoR[thisword])==0:
		successors[thisword]=set()
		successors[thisword].add("NULL")
		continue
	wordbeginning = thiswordparsed[0]
	if wordbeginning not in successors:
		successors[wordbeginning]=set()
	for j in range(1,thiswordnumberofpieces):
		newpiece = thiswordparsed[j]
		if wordbeginning not in successors:
			successors[wordbeginning]=set()
		successors[wordbeginning].add(newpiece) 
		wordbeginning += newpiece
	if wordbeginning not in successors: #whole word, now
			successors[wordbeginning]=set()
	successors[wordbeginning].add("NULL")
 

stemlist =  sorted(successors)
width = 15 
suffixwidth = 4
for word  in stemlist:
	suffixlist = ""
	if len(successors[word]) == 1 and "NULL" in successors[word]: 
		continue
	if len(successors[word]) < SFthreshold:
		continue
	for suffix in successors[word]:  
		suffixlist += suffix + " "*(width-len(suffix))
	sflength = len(successors[word])
	print >>SF_outfile, word + " "*(width - len(word)) +  \
				str(sflength) + " "*(suffixwidth-len(str(sflength)))  + suffixlist
#---------------------------------------------------------------------------------#	
#	Calculate predecessor frequency
#---------------------------------------------------------------------------------# 
preceders=dict()
if (True):
	for i in range(len(reversedwordlist)):	
		wordend = ""	
		thisword= reversedwordlist[i]
		thiswordparsed=WordsBrokenRtoL[thisword]
		thiswordnumberofpieces = len(thiswordparsed)
		 
		if thiswordnumberofpieces==0:
			preceders[thisword]=set()
			preceders[thisword].add("NULL")
			continue
		wordend = thiswordparsed[-1]
		if wordend not in preceders:
			preceders[wordend]=set()
		if thiswordnumberofpieces == 0:
			preceders[wordend].add("NULL")
		
		else:
			for j in range(thiswordnumberofpieces-2,-1,-1):
				newpiece = WordsBrokenRtoL[thisword][j]
				if wordend not in preceders:
					preceders[wordend]=set()
				preceders[wordend].add(newpiece) 
				wordend  = newpiece + wordend
			if wordend not in preceders: #whole word, now
					preceders[wordend]=set()
			preceders[wordend].add("NULL")
		

	TempReversedStems = list()
	for morph in preceders:
		morphcopy = morph[:]
		morphcopy = morphcopy[::-1]
		TempReversedStems.append(morphcopy)
	TempReversedStems.sort()
	for morph in TempReversedStems:
		morphcopy = morph[:]
		morphcopy = morphcopy[::-1]
		stemlist.append(morphcopy)

	width = 15 
	prefixwidth = 4
	for word  in stemlist:
		prefixlist = ""
		if word not in preceders:
			continue
		if len(preceders[word]) == 1 and "NULL" in preceders[word]: 
			continue
		if len(preceders[word]) < SFthreshold:
			continue
		for prefix in preceders[word]:  
			prefixlist += prefix + " "*(width-len(prefix))
		pflength = len(preceders[word])
		print >>PF_outfile, word + " "*(width - len(word)) +  \
					str(pflength) + " "*(prefixwidth-len(str(pflength)))  + prefixlist


#---------------------------------------------------------------------------------#	
#	Formatting
#---------------------------------------------------------------------------------# 
  

# ------------- Left to Right  ---------------------------------------------
maxlength = 0
maxlengthdict= dict()
for columnno in range(maxnumberofpiecesLtoR):
	maxlengthdict[columnno] = 0

# find out how large each morpheme slot needs to be for all the words...
for i in range(len(wordlist)):	
	thisword= wordlist[i]
	thiswordparsed=WordsBrokenLtoR[thisword]
	thiswordnumberofpieces = len(thiswordparsed)
	for j in range(thiswordnumberofpieces):
		thispiece = thiswordparsed[j]
		if len(thispiece) > maxlengthdict[j]:
			maxlengthdict[j]= len(thispiece)
	 
for i in range(len(wordlist)):
	thisword= wordlist[i]
	numberofpieces = len(WordsBrokenLtoR[thisword])
	if numberofpieces == 0:
		print >>trieLtoR_outfile, thisword, "number of pieces is zero."
	else:
		for j in range(len(WordsBrokenLtoR[thisword])):
			thispiece = WordsBrokenLtoR[thisword][j]
			print >>trieLtoR_outfile, thispiece," "*(maxlengthdict[j]-len(thispiece)),
		print >>trieLtoR_outfile
 		
#----------------- Right to Left --------------------------------------

if (True):
	# find out how large each morpheme slot needs to be for all the words...
	for i in range(len(reversedwordlist)):	
		thisword= wordlist[i]
		thiswordparsed=WordsBrokenRtoL[thisword]
		thiswordnumberofpieces = len(thiswordparsed)
		diff = maxnumberofpiecesRtoL - len(thiswordparsed)
		for j in range(thiswordnumberofpieces):
			columnno = diff + j 
			thispiece = thiswordparsed[j]
			if len(thispiece) > maxlengthdict[columnno]:
				maxlengthdict[columnno]= len(thispiece)
	 
	for i in range(len(reversedwordlist)):
		thisword= reversedwordlist[i]
		brokenword = WordsBrokenRtoL[thisword]
		numberofpieces = len( brokenword ) 

		diff = maxnumberofpiecesRtoL - numberofpieces
		for columnno in range(maxnumberofpiecesRtoL):
			if columnno < diff:
				thispiece = " "*maxlengthdict[columnno]
			else:
				thispiece = WordsBrokenRtoL[thisword][columnno-diff]
			if columnno == maxnumberofpiecesRtoL-1 and numberofpieces == 0:
				thispiece = thisword
			print >>trieRtoL_outfile, " "*(maxlengthdict[columnno]-len(thispiece)), thispiece,
		print >>trieRtoL_outfile
		



 

#---------------------------------------------------------------------------------#	
#	Close output files
#---------------------------------------------------------------------------------# 
trieRtoL_outfile.close()  
trieLtoR_outfile.close()
SF_outfile.close()
PF_outfile.close()
#---------------------------------------------------------------------------------#	
#	Logging information
#---------------------------------------------------------------------------------# 

localtime = time.asctime( time.localtime(time.time()) )
print "Local current time :", localtime

numberofwords = len(wordlist)
logfilename = outfolder + "logfile.txt"
logfile = open (logfilename,"a")


#--------------------------------------------------#

