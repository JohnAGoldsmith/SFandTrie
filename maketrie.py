# -*- coding: <utf-16> -*- 
unicode = True
import codecs
#import pygraphviz as pgv

side = "suffix" 

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
			if s1.endswith("ught"):
				print "a", s1, s2, s1[i+1:], length
			return s1[i+1:]
	if s1.endswith("ught"):
		print "b", s1,s2,s1[-1*length:], length
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
 
SFthreshold = 4

short_filename 		= "english"
out_short_filename 	= "english"
language		= "english"

short_filename 		= "french"
out_short_filename 	= "french"
language		= "french"

short_filename 		= "swahili"
out_short_filename 	= "swahili"
language		= "swahili"


datafolder    		= "../../data/" 
outfolder     		= datafolder + language + "/lxa/"
infolder 		= datafolder + language + '/dx1/'	

infilename 			= infolder  + short_filename     + ".dx1"
stemfilename 			= infolder  + short_filename     + "_stems.txt"
outfile_FSA_name		= outfolder + out_short_filename + "_FSA.txt"
outfile_FSA_graphics_name	= outfolder + out_short_filename + "_FSA_graphics.png"
outfile_log_name 		= outfolder + out_short_filename + "_log.txt"
outfile_trie_name 		= outfolder + out_short_filename + "_trie.txt"
outfile_SF_name 		= outfolder + out_short_filename + "_SF.txt"
if g_encoding == "utf8":
	print "yes utf8"
else:
	FSA_outfile = open (outfile_FSA_name, mode = 'w')
	trie_outfile = open (outfile_trie_name, mode = 'w')
	SF_outfile =  open (outfile_SF_name, mode = 'w')
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
 

  
MinimumStemLength 	= 5
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




WordsBroken=dict()
bl = dict() #breaklist
for i in range(len(wordlist)):
	bl[i]=set()
FoundPrefixes = dict()
FoundSuffixes = dict()
ReversedWords = list()
if side == "prefix":
	reversedWords = list()
	for word in wordlist:
		ReversedWords.append(word[::-1])
	ReversedWords.sort()
	wordlist = list()
	for word in ReversedWords:
		wordlist.append(word[::-1])
previousword = wordlist[0]
for i in range(1,len(wordlist)):
	thisword= wordlist[i]	 
	thislength = len(thisword)
	if side == "suffix":
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
				if wordlist[j][:m] == commonprefix:
					bl[j].add(m)
				else:
					break
			for j in range(i,len(wordlist)):
				if wordlist[j][:m] == commonprefix:
					bl[j].add(m)
				else:
					break
	 	 	FoundPrefixes[commonprefix] = 1
		previousword=thisword
	elif side=="prefix":
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
				if wordlist[j].endswith(commonsuffix):
					prefixlength = len(wordlist[j])-csl
					bl[j].add(prefixlength)
				else:
					break
			for j in range(i,len(wordlist)):
				if wordlist[j].endswith(commonsuffix):
					prefixlength = len(wordlist[j])-csl
					bl[j].add(prefixlength)
				else:
					break
	 	 	FoundSuffixes[commonsuffix] = 1
		previousword=thisword


maxnumberofpieces = 0
for i in range(len(wordlist)):
	thisword= wordlist[i]
	WordsBroken[thisword]=list()
	bl[i] = list(bl[i])
	bl[i].sort()
	output = ""
	if len(bl[i]) >  0:
		thispiece=""
		for x in  range(len(thisword)):
			output+=thisword[x] 
			thispiece += thisword[x]
			if x+1 in bl[i]:
				output += " "
				WordsBroken[thisword].append(thispiece)
				thispiece=""
		if len(thispiece)>0:
			WordsBroken[thisword].append(thispiece)
	if len(WordsBroken[thisword]) > maxnumberofpieces:
		maxnumberofpieces = len(WordsBroken[thisword])
 
		

print
#---------------------------------------------------------------------------------#	
#	Calculate successor frequency
#---------------------------------------------------------------------------------# 
successors=dict()
for i in range(len(wordlist)):	
	wordbeginning = ""	
	thisword= wordlist[i]
	thiswordparsed=WordsBroken[thisword]
	thiswordnumberofpieces = len(thiswordparsed)
	if side == "suffix":
		if len(WordsBroken[thisword])==0:
			successors[thisword]=set()
			successors[thisword].add("NULL")
			continue
		wordbeginning = WordsBroken[thisword][0]
		if wordbeginning not in successors:
			successors[wordbeginning]=set()
		if thiswordnumberofpieces == 0:
			successors[wordbeginning].add("NULL")
		else:
			for j in range(1,thiswordnumberofpieces):
				newpiece = WordsBroken[thisword][j]
				if wordbeginning not in successors:
					successors[wordbeginning]=set()
				successors[wordbeginning].add(newpiece) 
				wordbeginning += WordsBroken[thisword][j]
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
#	Formatting
#---------------------------------------------------------------------------------# 
  
maxlength = 0
maxlengthdict= dict()
for columnno in range(maxnumberofpieces):
	maxlengthdict[columnno] = 0

# find out how large each morpheme slot needs to be for all the words...
for i in range(len(wordlist)):	
	thisword= wordlist[i]
	thiswordparsed=WordsBroken[thisword]
	thiswordnumberofpieces = len(thiswordparsed)
	if side == "suffix":
		for j in range(thiswordnumberofpieces):
			thispiece = thiswordparsed[j]
			if len(thispiece) > maxlengthdict[j]:
				maxlengthdict[j]= len(thispiece)
	elif side == "prefix":
		diff = maxnumberofpieces - len(thiswordparsed)
		for j in range(thiswordnumberofpieces):
			columnno = diff + j 
			thispiece = thiswordparsed[j]
			if len(thispiece) > maxlengthdict[columnno]:
				maxlengthdict[columnno]= len(thispiece)
		


print "Number of columns: ", maxnumberofpieces
print maxlengthdict
for i in range(len(wordlist)):
	thisword= wordlist[i]
	numberofpieces = len(WordsBroken[thisword])
	if numberofpieces == 0: 
		continue
	if side == "suffix":
		for j in range(len(WordsBroken[thisword])):
			thispiece = WordsBroken[thisword][j]
			print >>trie_outfile, thispiece," "*(maxlengthdict[j]-len(thispiece)),
		print >>trie_outfile
	elif side == "prefix":		
		diff = maxnumberofpieces - numberofpieces
		for columnno in range(maxnumberofpieces):
			if columnno < diff:
				thispiece = " "*maxlengthdict[columnno]
			else:
				thispiece = WordsBroken[thisword][columnno-diff]
			print >>trie_outfile, thispiece," "*(maxlengthdict[columnno]-len(thispiece)),
		print >>trie_outfile
		

 

#---------------------------------------------------------------------------------#	
#	Close output files
#---------------------------------------------------------------------------------# 
  
trie_outfile.close()
SF_outfile.close()
#---------------------------------------------------------------------------------#	
#	Logging information
#---------------------------------------------------------------------------------# 

localtime = time.asctime( time.localtime(time.time()) )
print "Local current time :", localtime

numberofwords = len(wordlist)
logfilename = outfolder + "logfile.txt"
logfile = open (logfilename,"a")


#--------------------------------------------------#
