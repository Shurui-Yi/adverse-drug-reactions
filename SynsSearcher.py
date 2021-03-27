# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 12:57:24 2021

@author: yiysy003

read modified data file and matching
"""
import sys
import lucene
# import os
from java.io import File
from java.nio.file import Paths

from lucene import JavaError

from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.document import Document, Field, TextField, FieldType
from org.apache.lucene.search import FuzzyQuery, MultiTermQuery, IndexSearcher, TermQuery, BooleanQuery, BooleanClause
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader, FieldInfo, IndexOptions,MultiReader, Term
from org.apache.lucene.store import RAMDirectory, SimpleFSDirectory, MMapDirectory
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.search.spans import SpanNearQuery, SpanQuery, SpanTermQuery, SpanMultiTermQueryWrapper
from org.apache.lucene.queryparser.classic import MultiFieldQueryParser, QueryParser

import csv, datetime

from functions import *

class SynsSearcher:
    def __init__(self,fsDir, analyzer,input_fileName,synsDict,replacedBySyns):
        self.fsDir = fsDir
        self.analyzer = analyzer
        self.input_fileName = input_fileName
        self.replacedBySyns = replacedBySyns
        self.synsDict = synsDict

    def fuzzySearcher(self):
        
        matched_1st_count=0
        matched_2nd_count=0
        matched_3rd_count=0
        matched_4th_count=0
        matched_5th_count=0
    
        unmatched_1st_count=0
        no_returned=0
        count_total=0
        # 1. construct Seacher:
        # Implements search over a single IndexReader.
        # Use a single instance and use it across queries
        # to improve performance.
        searcher=IndexSearcher(DirectoryReader.open(self.fsDir))
        #
        # unmathed_terms_fields=['MRA_term','Modified_term','SearcherReturned_term', 'State', 'Rank']
        # with open ("unmatched_1st_1syn.csv","a+",newline="") as csvfile:
        #     csvwriter= csv.writer(csvfile)
        #     csvwriter= csvwriter(unmathed_terms_fields)
        # output_unmatchedTerms_fileName = self.outputUnmacthedTermsHeader()
        # read file
        with open(self.input_fileName, 'r') as csvfile:
            reader=csv.reader(csvfile)
            headers=next(reader)
            
            MRA_termsList_noreturn =[]
            modified_termsList_noreturn =[]
            changedBack_termsList_noreturn=[]
            
            
            MRA_termsList1 = []
            modified_termsList1 = []
            searcherReturned_termList1 = []
            changedBack_termsList1=[]
            
            MRA_termsList2 = []
            modified_termsList2 = []
            searcherReturned_termList2 = []
            changedBack_termsList2=[]
            
            MRA_termsList3 = []
            modified_termsList3 = []
            searcherReturned_termList3 = []
            changedBack_termsList3=[]
            
            MRA_termsList4 = []
            modified_termsList4 = []
            searcherReturned_termList4 = []
            changedBack_termsList4=[]
            
            MRA_termsList5 = []
            modified_termsList5 = []
            searcherReturned_termList5 = []
            changedBack_termsList5=[]
            
            
            for row in reader:
                
                count_total+=1
                # read strings
                query_string_original=row[0]
                query_string_edited=row[1]
            
                #2. construct  Query
                # clauses=query_string_edited.split()
                clauses = tokenize(query_string_edited,self.analyzer)
                
                    
                # replace back to its original words
                if self.replacedBySyns == True:
                    # print("replacing")
                    for index, clause in enumerate(clauses):
                        # not the key i.e. could be some key's synonym
                        if clause not in self.synsDict:
                            key = self.searchSynsDicKey(clause,self.synsDict)
                            if key != "None":
                                # print(key)
                                # print(clauses[index])
                                clauses[index] = key  
                                # print("key",key)
                                # print("after",clauses[index])
                                
                
                # print(tokenize(query_string_original, self.analyzer), clauses)
                fixedTerms = " ".join(clauses)   
                # Fuzzy query
                if len(clauses)==1:
                    query = FuzzyQuery(Term("pt",clauses[0]))
                else:
                     for i, val in enumerate(clauses):
                         # print(FuzzyQuery( Term("pt", clauses[i])).getMaxEdits(), clauses[i])
                         clauses[i] =  SpanMultiTermQueryWrapper(FuzzyQuery( Term("pt", clauses[i])))
                     query = SpanNearQuery(clauses,5, True)
                    
    
                topDocs = searcher.search(query, 5)
                scoreDocs = topDocs.scoreDocs
                print ("%s total matching documents." % len(scoreDocs))
                # print(scoreDocs)
        
                matched = False
                #  if no matching at all
                if (len(scoreDocs)==0): 
                    no_returned+=1
                    MRA_termsList_noreturn += [query_string_original]
                    modified_termsList_noreturn += [query_string_edited]
                    changedBack_termsList_noreturn += [fixedTerms]
                    # print("None")
                # matching 
                else:
                    for i,var in enumerate(scoreDocs):
                        doc_matching = searcher.doc(scoreDocs[i].doc)
                        returned_string_matching = doc_matching.getField('pt').stringValue()
                
                        if returned_string_matching == query_string_original:
                            if i==0:
                                matched_1st_count +=1
                                matched = True
                            elif i==1:
                                matched_2nd_count +=1
                                matched = True
                            elif i==2:
                                matched_3rd_count +=1
                                matched = True
                            elif i==3:
                                matched_4th_count +=1
                                matched = True
                            elif i==4:
                                matched_5th_count +=1
                                matched = True
                        elif returned_string_matching != query_string_original:
                            
                            if i==0: 
                                unmatched_1st_count+=1
                                # create lists storing all unmatched results used for statistical analysis( MRA orignial terms, modified terms and returned term )
                                MRA_termsList1 += [query_string_original]
                                modified_termsList1 += [query_string_edited]
                                changedBack_termsList1 += [fixedTerms]
                                searcherReturned_termList1 += [returned_string_matching]
                            
                            elif i==1 and matched == False:
                                MRA_termsList2 += [query_string_original]
                                modified_termsList2 += [query_string_edited]
                                changedBack_termsList2 += [fixedTerms]
                                searcherReturned_termList2 += [returned_string_matching]
                            elif i==2 and matched == False:
                                MRA_termsList3 += [query_string_original]
                                modified_termsList3 += [query_string_edited]
                                changedBack_termsList3 += [fixedTerms]
                                searcherReturned_termList3 += [returned_string_matching]
                            elif i==3 and matched == False:
                                MRA_termsList4 += [query_string_original]
                                modified_termsList4 += [query_string_edited]
                                changedBack_termsList4 += [fixedTerms]
                                searcherReturned_termList4 += [returned_string_matching]
                            elif i==4 and matched == False:
                                MRA_termsList5 += [query_string_original]
                                modified_termsList5 += [query_string_edited]
                                changedBack_termsList5 += [fixedTerms]
                                searcherReturned_termList5 += [returned_string_matching]
                        
                            # with open ("unmatched_1st_1syn.csv","a+",newline="") as csvfile:
                            #     csvwriter= csv.writer(csvfile)
                            #     csvwriter.writerow([query_string_original,query_string_edited,returned_string_matching, 'Unmatched', '1st'])

        
        unmatched_1st_count+=no_returned
        
        results={
            "input_fileName":self.input_fileName,
            "unmatched_1st_count":unmatched_1st_count,
            "macthed_1st_count":matched_1st_count,
            "macthed_2nd_count":matched_2nd_count,
            "macthed_3rd_count":matched_3rd_count,
            "macthed_4th_count":matched_4th_count,
            "macthed_5th_count":matched_5th_count,
            "no_returned":no_returned,
            "count_total":count_total,
            "top1_percentage":"%.2f" %(matched_1st_count/count_total*100),
            "top2_percentage":"%.2f" %((matched_1st_count+matched_2nd_count)/count_total*100),
            "top3_percentage":"%.2f" %((matched_1st_count+matched_2nd_count+matched_3rd_count)/count_total*100),
            "top4_percentage":"%.2f" %((matched_1st_count+matched_2nd_count+matched_3rd_count+matched_4th_count)/count_total*100),
            "top5_percentage":"%.2f" %((matched_1st_count+matched_2nd_count+matched_3rd_count+matched_4th_count+matched_5th_count)/count_total*100)
            }
        
        unmatchedTerms_dict1={'MRA_term':MRA_termsList1,
                             'Modified_term':modified_termsList1,
                             'ChangedBack': changedBack_termsList1,
                             'SearcherReturned_term':searcherReturned_termList1,
                             'State':["Unmatched"]*len(MRA_termsList1), 
                             'Rank': ["1st"]*len(MRA_termsList1)}
        
        unmatchedTerms_dict2={'MRA_term':MRA_termsList2,
                             'Modified_term':modified_termsList2,
                             'ChangedBack': changedBack_termsList2,
                             'SearcherReturned_term':searcherReturned_termList2,
                             'State':["Unmatched"]*len(MRA_termsList2), 
                             'Rank': ["2nd"]*len(MRA_termsList2)}
        
        unmatchedTerms_dict3={'MRA_term':MRA_termsList3,
                             'Modified_term':modified_termsList3,
                             'ChangedBack': changedBack_termsList3,
                             'SearcherReturned_term':searcherReturned_termList3,
                             'State':["Unmatched"]*len(MRA_termsList3), 
                             'Rank': ["3rd"]*len(MRA_termsList3)}
        
        unmatchedTerms_dict4={'MRA_term':MRA_termsList4,
                             'Modified_term':modified_termsList4,
                             'ChangedBack': changedBack_termsList4,
                             'SearcherReturned_term':searcherReturned_termList4,
                             'State':["Unmatched"]*len(MRA_termsList4), 
                             'Rank': ["4th"]*len(MRA_termsList4)}
        
        unmatchedTerms_dict5={'MRA_term':MRA_termsList5,
                             'Modified_term':modified_termsList5,
                             'ChangedBack': changedBack_termsList5,
                             'SearcherReturned_term':searcherReturned_termList5,
                             'State':["Unmatched"]*len(MRA_termsList5), 
                             'Rank': ["5th"]*len(MRA_termsList5)}
        noreturnedTerms_dict = {'MRA_term':MRA_termsList_noreturn,
                             'Modified_term':modified_termsList_noreturn,
                             'ChangedBack': changedBack_termsList_noreturn,
                             'State':["NO return"]*len(MRA_termsList_noreturn)}
        
        return(unmatchedTerms_dict1,unmatchedTerms_dict2,
               unmatchedTerms_dict3,unmatchedTerms_dict4,unmatchedTerms_dict5,noreturnedTerms_dict,results)
    
    # def createTime(self):
    #     created_time= datetime.datetime.now()
    #     created_time=created_time.strftime("%d-%m-%Y %H:%M")    
    #     return (created_time)
    # searchSynsDicKey : find if the imput word is the synonyms of some MedDRA word. 
    # If it is, then return the original MRA word. Otherwise, return None
    # word: input word for searching
    # dictionary: search word in this dictionary which stores the original MRA vocabulary (not term) and their synonyms.
    def searchSynsDicKey(self,word,dictionary):
        for key in dictionary:
            for synonym in dictionary[key]:
                if word==synonym:
                    return key
        #if it is not in the dictionary
        return "None"
    
        
    def findUnmatchedTokens(self, unmatchedTerms_dict):
        
        # unmatched_tokensList = self.listUmatchedTokens(unmatchedTerms_dict)
        unmatchedMRA_termList = unmatchedTerms_dict["MRA_term"]
        unmatchedReturned_termList = unmatchedTerms_dict["SearcherReturned_term"]
        
        unfoundTokens_list=[]
        addedTokens_list=[]
        
        unfoundTokens_list_list=[]
        addedTokens_list_list=[]
        
        unfoundTokens_list2=[]
        addedTokens_list2=[]
        
        tokenmissed_count=0
        tokenadded_count=0
        
        for index, term in enumerate(unmatchedMRA_termList):
            # create set
            
            original_tokens= tokenize(term,self.analyzer)
            returned_tokens= tokenize(unmatchedReturned_termList[index],self.analyzer)
             
            if len(original_tokens) == len(returned_tokens):  
                # original_tokensSet = set(original_tokens)
                # returned_tokensSet = set(returned_tokens)
                
                # unfoundTokens_set = original_tokensSet.difference(returned_tokensSet)                        
                # unfoundTokens_list += list(unfoundTokens_set)
                # unfoundTokens_list_list += [list(unfoundTokens_set)]
                
                # addedTokens_set = returned_tokensSet.difference(original_tokensSet)
                # addedTokens_list += list(addedTokens_set)
                # addedTokens_list_list += [list(addedTokens_set)]
                
                for index, token in enumerate(original_tokens):
                    if token != returned_tokens[index]:
                        
                        unfoundTokens_list2 += [original_tokens[index]]
                        addedTokens_list2 += [returned_tokens[index]]
            elif len(original_tokens) > len(returned_tokens):
                tokenmissed_count+=1
            # returned term is longer than original terms (i.e. new words are added)
            else:
                tokenadded_count +=1

                
        # store in data frame and group by 
        # tokens only in original terms
        # unfoundTokens_df = pandas.DataFrame({"unfoundTokens":unfoundTokens_list,
        #                                      "count":[1]*len(unfoundTokens_list)})
        
        # unfoundTokens_df = unfoundTokens_df.groupby("unfoundTokens").sum().sort_values("count",ascending = False)
        
        # tokens only in returned terms
        # addedTokens_df = pandas.DataFrame({"addedTokens":addedTokens_list,
        #                                      "count":[1]*len(addedTokens_list)})
        
        # addedTokens_df = addedTokens_df.groupby("addedTokens").sum().sort_values("count",ascending = False)
        
        # unfound and added tokens
        # unfound_addedTokens_df = pandas.DataFrame({"unfoundTokens":unfoundTokens_list_list,
        #                                            "addedTokens":addedTokens_list_list,
        #                                            "count":[1]*len(unfoundTokens_list_list)})


        unfound_addedTokens_df2 = pandas.DataFrame({"unfoundTokens":unfoundTokens_list2,
                                                    "addedTokens":addedTokens_list2,
                                                    "count":[1]*len(unfoundTokens_list2)})
       
        unfound_addedTokens_df2 = unfound_addedTokens_df2.groupby(["unfoundTokens","addedTokens"]).sum().sort_values("count",ascending = False)
        print(tokenmissed_count,"tokens are not missed", tokenadded_count,"have added words")
        return (unfound_addedTokens_df2)
        # return(unfoundTokens_df,addedTokens_df,unfound_addedTokens_df)
        
        
    def produceAllTop5UnmatchedPaires(self, matchingRes):
        unmatchedTerms_dict1 = matchingRes[0]
        unmatchedTerms_dict2 = matchingRes[1]
        unmatchedTerms_dict3 = matchingRes[2]
        unmatchedTerms_dict4 = matchingRes[3]
        unmatchedTerms_dict5 = matchingRes[4]
        unfound_addedTokens_df1st= self.findUnmatchedTokens(unmatchedTerms_dict1)
        unfound_addedTokens_df2nd= self.findUnmatchedTokens(unmatchedTerms_dict2)
        unfound_addedTokens_df3rd= self.findUnmatchedTokens(unmatchedTerms_dict3)
        unfound_addedTokens_df4th= self.findUnmatchedTokens(unmatchedTerms_dict4)
        unfound_addedTokens_df5th= self.findUnmatchedTokens(unmatchedTerms_dict5)
            
            
        return(unfound_addedTokens_df1st,unfound_addedTokens_df2nd,unfound_addedTokens_df3rd,unfound_addedTokens_df4th,unfound_addedTokens_df5th)
        

            
    
        
    
    
    
        
    
