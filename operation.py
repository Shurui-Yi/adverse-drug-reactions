# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 17:54:30 2021

@author: yiysy003
"""
## DO NOT RUN THE WHOLE FILE, RUN BY PART OR LINE
################################################################################################################################################
#               PART 1: indexing
################################################################################################################################################
#initial lucene VM
JVM_DLL_PATH = 'C:/Program Files/AdoptOpenJDK/jdk-8.0.275.1-hotspot/jre/bin/server'

# Ensure paths are correct to find the jvm.dll for lucene
import os
path = os.environ['Path'].split(os.pathsep)
path.append(JVM_DLL_PATH)
os.environ['Path'] = os.pathsep.join(path)
#install pylucene from http://lucene.apache.org/pylucene/




#import lucene packages
import sys
import lucene
# import os
from java.io import File
from java.nio.file import Paths

from lucene import JavaError

from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.document import Document, Field, TextField, FieldType
from org.apache.lucene.search import FuzzyQuery, MultiTermQuery, IndexSearcher, TermQuery
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader, FieldInfo, IndexOptions,MultiReader, Term
from org.apache.lucene.store import RAMDirectory, SimpleFSDirectory, MMapDirectory
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.search.spans import SpanNearQuery, SpanQuery, SpanTermQuery, SpanMultiTermQueryWrapper
from org.apache.lucene.queryparser.classic import MultiFieldQueryParser, QueryParser
#import libs/functions
import string, random
#import defined functions
from Indexer import *
from functions import *

from TypoSimulation import *
from TypoSearcher import *

from SynsSimulation import *
from SynsSearcher import *
#### intitialize lucene VM (COMMENT THIS LINE ONCE THE VM HAS RAN)
lucene.initVM(vmargs=['-Djava.awt.headless=true'])
#set analyzer and directory
fsDir = MMapDirectory(Paths.get('index'))
analyzer = StandardAnalyzer()
#Indexing
pt_list= Indexer(fsDir, analyzer)
#get syns dictionary
syns_dic=getSyns(pt_list, analyzer)

################################################################################################################################################
#               PART 2: basline (maxEdits = 0 , 1, 2) input is the orginal preferred terms stored in pt.csv
################################################################################################################################################
###add max edits in Fuzzy query
### maxEdits = 0 ########################################################################################
typoSearcherBase_0edit = TypoSearcher(fsDir, analyzer,'pt.csv')
matchingResBase_0edit= typoSearcherBase_0edit.fuzzySearcherWithMaxEdits(0)
# write in csv
# there is no items in wrong returned terms in top 5 match, 
#i.e. only 1st match or no return in results
# write all terms which does not have return in csv file
writeDicttoCSVFile(matchingResBase_0edit[5],"Baseline_0edit_NoReturnTerms.csv")

writeStatisticHeadertoCSVFile2()
writeStatisticResDicttoCSVFile2(matchingResBase_0edit[6])

# error analysis
# No csv files

# maxEdits = 1 ########################################################################################
typoSearcherBase_1edit = TypoSearcher(fsDir, analyzer,'pt.csv')
matchingResBase_1edit= typoSearcherBase_1edit.fuzzySearcherWithMaxEdits(1)
# write the top 5 unmtached terms 
writeDicttoCSVFile(matchingResBase_1edit[0],"Baseline_1edit_1stUnmatchedPairs.csv")
writeDicttoCSVFile(matchingResBase_1edit[1],"Baseline_1edit_2ndUnmatchedPairs.csv")
writeDicttoCSVFile(matchingResBase_1edit[2],"Baseline_1edit_3rdUnmatchedPairs.csv")
writeDicttoCSVFile(matchingResBase_1edit[3],"Baseline_1edit_4thUnmatchedPairs.csv")
writeDicttoCSVFile(matchingResBase_1edit[4],"Baseline_1edit_5thUnmatchedPairs.csv")
writeDicttoCSVFile(matchingResBase_1edit[5],"Baseline_1edit_NoReturnTerms.csv")

writeStatisticResDicttoCSVFile2(matchingResBase_1edit[6])
# error analysis
# write all unmatched terms which having the same length as returned terms, but some tokens are replaced
Baseline_1edit_difference=typoSearcherBase_1edit.produceAllTop5UnmatchedPaires(matchingResBase_1edit)

writeDftoCSVFile(Baseline_1edit_difference[0],"Baseline_1edit_1stUnmatchedTokens.csv",True)
writeDftoCSVFile(Baseline_1edit_difference[1],"Baseline_1edit_2ndUnmatchedTokens.csv",True)
writeDftoCSVFile(Baseline_1edit_difference[2],"Baseline_1edit_3rdUnmatchedTokens.csv",True)
writeDftoCSVFile(Baseline_1edit_difference[3],"Baseline_1edit_4thUnmatchedTokens.csv",True)
writeDftoCSVFile(Baseline_1edit_difference[4],"Baseline_1edit_5thUnmatchedTokens.csv",True)

# return all returned terms which contains some other tokens not in original pt, (i.e. returned term is longer than the pt)
# it is empty 
Baseline_1edit_longReturnedTerm=typoSearcherBase_1edit.produceAllTop5UnmatchedPairesLongReturn(matchingResBase_1edit)

### baseline
#maxEdits = 2 (default value) ########################################################################################
typoSearcherBase = TypoSearcher(fsDir, analyzer,'pt.csv')
matchingResBase= typoSearcherBase.fuzzySearcher()
# write in csv
writeDicttoCSVFile(matchingResBase[0],"Baseline_1stUnmatchedPairs.csv")
writeDicttoCSVFile(matchingResBase[1],"Baseline_2ndUnmatchedPairs.csv")
writeDicttoCSVFile(matchingResBase[2],"Baseline_3rdUnmatchedPairs.csv")
writeDicttoCSVFile(matchingResBase[3],"Baseline_4thUnmatchedPairs.csv")
writeDicttoCSVFile(matchingResBase[4],"Baseline_5thUnmatchedPairs.csv")
writeDicttoCSVFile(matchingResBase[5],"Baseline_NoReturnTerms.csv")

writeStatisticHeadertoCSVFile()
writeStatisticResDicttoCSVFile(matchingResBase[6])

# error analysis
matchingResBase_difference=typoSearcherBase.produceAllTop5UnmatchedPaires(matchingResBase)
writeDftoCSVFile(matchingResBase_difference[0],"Baseline_1stUnmatchedTokens.csv",True)
writeDftoCSVFile(matchingResBase_difference[1],"Baseline_2ndUnmatchedTokens.csv",True)
writeDftoCSVFile(matchingResBase_difference[2],"Baseline_3rdUnmatchedTokens.csv",True)
writeDftoCSVFile(matchingResBase_difference[3],"Baseline_4thUnmatchedTokens.csv",True)
writeDftoCSVFile(matchingResBase_difference[4],"Baseline_5thUnmatchedTokens.csv",True)

################################################################################################################################################
#      PART 3 : Simulate spelling errors (error rate = 0.125, 0.17, 0.25)
################################################################################################################################################

simulation_types = ["TYPO_MIXING","SYNS_ONE","SYNS_TWO"]
# STEP 1: create simulated datset###########################################

# ##create TypoSimulation objects
# Typing errors rate 0.125 (1 error per 8 chars) for 5 round
typoSimulation125 = TypoSimulation(pt_list,fsDir, analyzer,"TYPO_MIXING",5,0.125)
# Typing errors rate 0.17 (1 error per 6 chars) for 5 round
typoSimulation17 = TypoSimulation(pt_list,fsDir, analyzer,"TYPO_MIXING",5,0.17)
# Typing errors rate 0.25 (1 error per 4 chars) for 5 round
typoSimulation25 = TypoSimulation(pt_list,fsDir, analyzer,"TYPO_MIXING",5,0.25)


# # Simulated errors
typoDataset125_df = typoSimulation125.modifyNpPerWord()
typoDataset17_df = typoSimulation17.modifyNpPerWord()
typoDataset25_df = typoSimulation25.modifyNpPerWord()

# STEP2: check if all modification is valid ########################################
# # check if all simulated data is valid (i.e. eidit distance (the sum edits of tokens) must more than the number of modification)
print("All modification is valid?",checkValidModification(typoDataset125_df))
print("All modification is valid?",checkValidModification(typoDataset17_df))
print("All modification is valid?",checkValidModification(typoDataset25_df))
# if flase check what is the term, its modificantion and edits
# co=checkValidModification(typoDataset17_df)
# for index, num in enumerate(co):
#     if num==1:
#         print(index)
#         print(typoDataset17_df.iloc[index])

# STEP 3: write to csv file ############################################################
# # write to csv file
typoDataset125_df.to_csv('TypoSimulatedDataset0.125.csv', index=False)
typoDataset17_df.to_csv('TypoSimulatedDataset0.17.csv', index=False)
typoDataset25_df.to_csv('TypoSimulatedDataset0.25.csv', index=False)


################################################################################################################################################
#      PART 4 : Searching simulated datasets
################################################################################################################################################        
#(i) error rate = 0.125
# read csv and searching by FuzzyQuery
typoSearcher125 = TypoSearcher(fsDir, analyzer,'TypoSimulatedDataset0.125.csv')
typoResSummary125= typoSearcher125.fuzzySearcher()
# write in csv
writeDicttoCSVFile(typoResSummary125[0],"Typo125_1stUnmatchedPairs.csv")
writeDicttoCSVFile(typoResSummary125[1],"Typo125_2ndUnmatchedPairs.csv")
writeDicttoCSVFile(typoResSummary125[2],"Typo125_3rdUnmatchedPairs.csv")
writeDicttoCSVFile(typoResSummary125[3],"Typo125_4thUnmatchedPairs.csv")
writeDicttoCSVFile(typoResSummary125[4],"Typo125_5thUnmatchedPairs.csv")
writeDicttoCSVFile(typoResSummary125[5],"Typo125_NoReturnTerms.csv")

writeStatisticResDicttoCSVFile(typoResSummary125[6])
# error analysis
# same length but some token is replaced at the same position
typoRes125_difference=typoSearcher125.produceAllTop5UnmatchedPaires(typoResSummary125)

writeDftoCSVFile(typoRes125_difference[0],"Typo125_1stUnmatchedTokens.csv",True)
writeDftoCSVFile(typoRes125_difference[1],"Typo125_2ndUnmatchedTokens.csv",True)
writeDftoCSVFile(typoRes125_difference[2],"Typo125_3rdUnmatchedTokens.csv",True)
writeDftoCSVFile(typoRes125_difference[3],"Typo125_4thUnmatchedTokens.csv",True)
writeDftoCSVFile(typoRes125_difference[4],"Typo125_5thUnmatchedTokens.csv",True)

#returned terms contains some other tokens not in original pt
typoRes125_longReturn=typoSearcher125.produceAllTop5UnmatchedPairesLongReturn(typoResSummary125)

writeDftoCSVFile(typoRes125_longReturn[0],"Typo125_1stReturnMoreTokens.csv",False)
writeDftoCSVFile(typoRes125_longReturn[1],"Typo125_2ndReturnMoreTokens.csv",False)
writeDftoCSVFile(typoRes125_longReturn[2],"Typo125_3rdReturnMoreTokens.csv",False)
writeDftoCSVFile(typoRes125_longReturn[3],"Typo125_4thReturnMoreTokens.csv",False)
writeDftoCSVFile(typoRes125_longReturn[4],"Typo125_5thReturnMoreTokens.csv",False)



#(ii) error rate = 0.17 #######################################################################################
typoSearcher17 = TypoSearcher(fsDir, analyzer,'TypoSimulatedDataset0.17.csv')
typoResSummary17 = typoSearcher17.fuzzySearcher()
# write in csv
writeDicttoCSVFile(typoResSummary17[0],"Typo17_1stUnmatchedPairs.csv")
writeDicttoCSVFile(typoResSummary17[1],"Typo17_2ndUnmatchedPairs.csv")
writeDicttoCSVFile(typoResSummary17[2],"Typo17_3rdUnmatchedPairs.csv")
writeDicttoCSVFile(typoResSummary17[3],"Typo17_4thUnmatchedPairs.csv")
writeDicttoCSVFile(typoResSummary17[4],"Typo17_5thUnmatchedPairs.csv")
writeDicttoCSVFile(typoResSummary17[5],"Typo17_NoReturnTerms.csv")

writeStatisticResDicttoCSVFile(typoResSummary17[6])
# error analysis
typoRes17_difference=typoSearcher17.produceAllTop5UnmatchedPaires(typoResSummary17)

writeDftoCSVFile(typoRes17_difference[0],"Typo17_1stUnmatchedTokens.csv",True)
writeDftoCSVFile(typoRes17_difference[1],"Typo17_2ndUnmatchedTokens.csv",True)
writeDftoCSVFile(typoRes17_difference[2],"Typo17_3rdUnmatchedTokens.csv",True)
writeDftoCSVFile(typoRes17_difference[3],"Typo17_4thUnmatchedTokens.csv",True)
writeDftoCSVFile(typoRes17_difference[4],"Typo17_5thUnmatchedTokens.csv",True)

#returned terms contains some other tokens not in original pt
typoRes17_longReturn=typoSearcher17.produceAllTop5UnmatchedPairesLongReturn(typoResSummary17)
writeDftoCSVFile(typoRes17_longReturn[0],"Typo17_1stReturnMoreTokens.csv",False)
writeDftoCSVFile(typoRes17_longReturn[1],"Typo17_2ndReturnMoreTokens.csv",False)
writeDftoCSVFile(typoRes17_longReturn[2],"Typo17_3rdReturnMoreTokens.csv",False)
writeDftoCSVFile(typoRes17_longReturn[3],"Typo17_4thReturnMoreTokens.csv",False)
writeDftoCSVFile(typoRes17_longReturn[4],"Typo17_5thReturnMoreTokens.csv",False)



#(iii) error rate = 0.25  #######################################################################################
typoSearcher25 = TypoSearcher(fsDir, analyzer,'TypoSimulatedDataset0.25.csv')
typoResSummary25 = typoSearcher25.fuzzySearcher()
# write in csv
writeDicttoCSVFile(typoResSummary25[0],"Typo25_1stUnmatchedPairs.csv")
writeDicttoCSVFile(typoResSummary25[1],"Typo25_2ndUnmatchedPairs.csv")
writeDicttoCSVFile(typoResSummary25[2],"Typo25_3rdUnmatchedPairs.csv")
writeDicttoCSVFile(typoResSummary25[3],"Typo25_4thUnmatchedPairs.csv")
writeDicttoCSVFile(typoResSummary25[4],"Typo25_5thUnmatchedPairs.csv")
writeDicttoCSVFile(typoResSummary25[5],"Typo25_NoReturnTerms.csv")

writeStatisticResDicttoCSVFile(typoResSummary25[6])
# error analysis
typoRes25_difference=typoSearcher25.produceAllTop5UnmatchedPaires(typoResSummary25)
writeDftoCSVFile(typoRes25_difference[0],"Typo25_1stUnmatchedTokens.csv",True)
writeDftoCSVFile(typoRes25_difference[1],"Typo25_2ndUnmatchedTokens.csv",True)
writeDftoCSVFile(typoRes25_difference[2],"Typo25_3rdUnmatchedTokens.csv",True)
writeDftoCSVFile(typoRes25_difference[3],"Typo25_4thUnmatchedTokens.csv",True)
writeDftoCSVFile(typoRes25_difference[4],"Typo25_5thUnmatchedTokens.csv",True)

#returned terms contains some other tokens not in original pt
typoRes25_longReturn=typoSearcher25.produceAllTop5UnmatchedPairesLongReturn(typoResSummary25)

writeDftoCSVFile(typoRes25_longReturn[0],"Typo25_1stReturnMoreTokens.csv",False)
writeDftoCSVFile(typoRes25_longReturn[1],"Typo25_2ndReturnMoreTokens.csv",False)
writeDftoCSVFile(typoRes25_longReturn[2],"Typo25_3rdReturnMoreTokens.csv",False)
writeDftoCSVFile(typoRes25_longReturn[3],"Typo25_4thReturnMoreTokens.csv",False)
writeDftoCSVFile(typoRes25_longReturn[4],"Typo25_5thReturnMoreTokens.csv",False)

#(ii) calculate the max length of tokens in all terms which have no return
#read all noreturn csv file and store data in dataframe
## REMEMBER CHANGE THE OS PATH

pt_df= pandas.DataFrame({"MRA_term":pt_list,"Modified_term":pt_list})
len_maxPT_list = getMaxLengthOfTokenPerTerm(pt_df,analyzer,0)[0]
len_maxPT_list_5round = [num * 5 for num in len_maxPT_list]

os.chdir("C:/Users/shurui/Desktop/AdverseDrugReactions/Results/Typo125")
typoRes125noreturn_df=pandas.read_csv("Typo125_NoReturnTerms.csv")
len_max125_list = getMaxLengthOfTokenPerTerm(typoRes125noreturn_df,analyzer,0.125)[0]

os.chdir("C:/Users/shurui/Desktop/AdverseDrugReactions/Results/Typo17")
typoRes17noreturn_df=pandas.read_csv("Typo17_NoReturnTerms.csv")
len_max17_list = getMaxLengthOfTokenPerTerm(typoRes17noreturn_df,analyzer,0.17)[0]

os.chdir("C:/Users/shurui/Desktop/AdverseDrugReactions/Results/Typo25")
typoRes25noreturn_df=pandas.read_csv("Typo25_NoReturnTerms.csv")
len_max25_list = getMaxLengthOfTokenPerTerm(typoRes25noreturn_df,analyzer,0.25)[0]

noreturn_df=pandas.DataFrame({"CONTROL GROUP": len_maxPT_list_5round,"Typo125_NoReturnTerms.csv" : len_max125_list,"Typo17_NoReturnTerms.csv":len_max17_list,"Typo25_NoReturnTerms.csv": len_max25_list})
noreturn_df.to_csv("MaxLengthOfToken_noreturn.csv", index = True)




################################################################################################################################################
#      PART 5 : Simulate Synonyms datasets
################################################################################################################################################        

##create SynsSimulation objects
synsSimulation1=SynsSimulation(pt_list,fsDir, analyzer,syns_dic,"SYNS_ONE")
synsDataset1_df=synsSimulation1.replace1WordWithSyn()

synsDataset1_df.to_csv('SynsSimulatedDataset1.csv', index=False)
# ##create searcher objects
# (i) not switch back
synsSearcher1_unreplaced = SynsSearcher(fsDir, analyzer,'SynsSimulatedDataset1.csv',syns_dic,False)
synsResSummary1_unreplaced = synsSearcher1_unreplaced.fuzzySearcher()

# write to csv
writeDicttoCSVFile(synsResSummary1_unreplaced[0],"Syns1_unreplaced_1stUnmatchedPairs.csv")
writeDicttoCSVFile(synsResSummary1_unreplaced[1],"Syns1_unreplaced_2ndUnmatchedPairs.csv")
writeDicttoCSVFile(synsResSummary1_unreplaced[2],"Syns1_unreplaced_3rdUnmatchedPairs.csv")
writeDicttoCSVFile(synsResSummary1_unreplaced[3],"Syns1_unreplaced_4thUnmatchedPairs.csv")
writeDicttoCSVFile(synsResSummary1_unreplaced[4],"Syns1_unreplaced_5thUnmatchedPairs.csv")
writeDicttoCSVFile(synsResSummary1_unreplaced[5],"Syns1_unreplaced_NoReturnTerms.csv")

writeStatisticResDicttoCSVFile(synsResSummary1_unreplaced[6])
# error analysis
synsRes1_unreplaced_difference=synsSearcher1_unreplaced.produceAllTop5UnmatchedPaires(synsResSummary1_unreplaced)
writeDftoCSVFile(synsRes1_unreplaced_difference[0],"Syns1_unreplaced_1stUnmatchedTokens.csv",True)
writeDftoCSVFile(synsRes1_unreplaced_difference[1],"Syns1_unreplaced_2ndUnmatchedTokens.csv",True)
writeDftoCSVFile(synsRes1_unreplaced_difference[2],"Syns1_unreplaced_3rdUnmatchedTokens.csv",True)
writeDftoCSVFile(synsRes1_unreplaced_difference[3],"Syns1_unreplaced_4thUnmatchedTokens.csv",True)
writeDftoCSVFile(synsRes1_unreplaced_difference[4],"Syns1_unreplaced_5thUnmatchedTokens.csv",True)


# (ii) switch back
synsSearcher1_replaced = SynsSearcher(fsDir, analyzer,'SynsSimulatedDataset1.csv',syns_dic,True)
synsResSummary1_replaced = synsSearcher1_replaced.fuzzySearcher()
  
# write to csv
writeDicttoCSVFile(synsResSummary1_replaced[0],"Syns1_replaced_1stUnmatchedPairs.csv")
writeDicttoCSVFile(synsResSummary1_replaced[1],"Syns1_replaced_2ndUnmatchedPairs.csv")
writeDicttoCSVFile(synsResSummary1_replaced[2],"Syns1_replaced_3rdUnmatchedPairs.csv")
writeDicttoCSVFile(synsResSummary1_replaced[3],"Syns1_replaced_4thUnmatchedPairs.csv")
writeDicttoCSVFile(synsResSummary1_replaced[4],"Syns1_replaced_5thUnmatchedPairs.csv")
writeDicttoCSVFile(synsResSummary1_replaced[5],"Syns1_replaced_NoReturnTerms.csv")

writeStatisticResDicttoCSVFile(synsResSummary1_replaced[6])
# error analysis
synsRes1_replaced_difference=synsSearcher1_replaced.produceAllTop5UnmatchedPaires(synsResSummary1_replaced)
writeDftoCSVFile(synsRes1_replaced_difference[0],"Syns1_replaced_1stUnmatchedTokens.csv",True)
writeDftoCSVFile(synsRes1_replaced_difference[1],"Syns1_replaced_2ndUnmatchedTokens.csv",True)
writeDftoCSVFile(synsRes1_replaced_difference[2],"Syns1_replaced_3rdUnmatchedTokens.csv",True)
writeDftoCSVFile(synsRes1_replaced_difference[3],"Syns1_replaced_4thUnmatchedTokens.csv",True)
writeDftoCSVFile(synsRes1_replaced_difference[4],"Syns1_replaced_5thUnmatchedTokens.csv",True)


# ####### REPLACE TWO SYNS############################################################################# 


##create SynsSimulation objects
synsSimulation2=SynsSimulation(pt_list,fsDir, analyzer,syns_dic,"SYNS_TWO")
synsDataset2_df=synsSimulation2.replace2WordsWithSyn()
# calculate how many combinations
synsSimulation2.calculateCombinations(2)
synsDataset2_df.to_csv('SynsSimulatedDataset2.csv', index=False)



# ##create searcher objects
# (i) not switch back
synsSearcher2_unreplaced = SynsSearcher(fsDir, analyzer,'SynsSimulatedDataset2.csv',syns_dic,False)
synsResSummary2_unreplaced = synsSearcher2_unreplaced.fuzzySearcher()

# write to csv
writeDicttoCSVFile(synsResSummary2_unreplaced[0],"Syns2_unreplaced_1stUnmatchedPairs.csv")
writeDicttoCSVFile(synsResSummary2_unreplaced[1],"Syns2_unreplaced_2ndUnmatchedPairs.csv")
writeDicttoCSVFile(synsResSummary2_unreplaced[2],"Syns2_unreplaced_3rdUnmatchedPairs.csv")
writeDicttoCSVFile(synsResSummary2_unreplaced[3],"Syns2_unreplaced_4thUnmatchedPairs.csv")
writeDicttoCSVFile(synsResSummary2_unreplaced[4],"Syns2_unreplaced_5thUnmatchedPairs.csv")
writeDicttoCSVFile(synsResSummary2_unreplaced[5],"Syns2_unreplaced_NoReturnTerms.csv")

writeStatisticResDicttoCSVFile(synsResSummary2_unreplaced[6])
# error analysis
synsRes2_unreplaced_difference=synsSearcher2_unreplaced.produceAllTop5UnmatchedPaires(synsResSummary2_unreplaced)
writeDftoCSVFile(synsRes2_unreplaced_difference[0],"Syns2_unreplaced_1stUnmatchedTokens.csv",True)
writeDftoCSVFile(synsRes2_unreplaced_difference[1],"Syns2_unreplaced_2ndUnmatchedTokens.csv",True)
writeDftoCSVFile(synsRes2_unreplaced_difference[2],"Syns2_unreplaced_3rdUnmatchedTokens.csv",True)
writeDftoCSVFile(synsRes2_unreplaced_difference[3],"Syns2_unreplaced_4thUnmatchedTokens.csv",True)
writeDftoCSVFile(synsRes2_unreplaced_difference[4],"Syns2_unreplaced_5thUnmatchedTokens.csv",True)


# (ii) switch back
synsSearcher2_replaced = SynsSearcher(fsDir, analyzer,'SynsSimulatedDataset2.csv',syns_dic,True)
synsResSummary2_replaced = synsSearcher2_replaced.fuzzySearcher()
  
# write to csv
writeDicttoCSVFile(synsResSummary2_replaced[0],"Syns2_replaced_1stUnmatchedPairs.csv")
writeDicttoCSVFile(synsResSummary2_replaced[1],"Syns2_replaced_2ndUnmatchedPairs.csv")
writeDicttoCSVFile(synsResSummary2_replaced[2],"Syns2_replaced_3rdUnmatchedPairs.csv")
writeDicttoCSVFile(synsResSummary2_replaced[3],"Syns2_replaced_4thUnmatchedPairs.csv")
writeDicttoCSVFile(synsResSummary2_replaced[4],"Syns2_replaced_5thUnmatchedPairs.csv")
writeDicttoCSVFile(synsResSummary2_replaced[5],"Syns2_replaced_NoReturnTerms.csv")

writeStatisticResDicttoCSVFile(synsResSummary2_replaced[6])
# error analysis
synsRes2_replaced_difference=synsSearcher2_replaced.produceAllTop5UnmatchedPaires(synsResSummary2_replaced)
writeDftoCSVFile(synsRes2_replaced_difference[0],"Syns2_replaced_1stUnmatchedTokens.csv",True)
writeDftoCSVFile(synsRes2_replaced_difference[1],"Syns2_replaced_2ndUnmatchedTokens.csv",True)
writeDftoCSVFile(synsRes2_replaced_difference[2],"Syns2_replaced_3rdUnmatchedTokens.csv",True)
writeDftoCSVFile(synsRes2_replaced_difference[3],"Syns2_replaced_4thUnmatchedTokens.csv",True)
writeDftoCSVFile(synsRes2_replaced_difference[4],"Syns2_replaced_5thUnmatchedTokens.csv",True)




