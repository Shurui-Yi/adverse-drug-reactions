# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 19:22:55 2021

@author: yiysy003
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
from org.apache.lucene.search import FuzzyQuery, MultiTermQuery, IndexSearcher, TermQuery
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader, FieldInfo, IndexOptions,MultiReader, Term
from org.apache.lucene.store import RAMDirectory, SimpleFSDirectory, MMapDirectory
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.search.spans import SpanNearQuery, SpanQuery, SpanTermQuery, SpanMultiTermQueryWrapper
from org.apache.lucene.queryparser.classic import MultiFieldQueryParser, QueryParser

import csv, pandas, numpy
from functions import *

import re, unicodedata, nltk


class TypoSearcher:
    def __init__(self,fsDir, analyzer,input_fileName):
        self.fsDir = fsDir
        self.analyzer = analyzer
        self.input_fileName = input_fileName
        
    # FuzzyQuery
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
    
        # read file
        with open(self.input_fileName, 'r') as csvfile:
            reader=csv.reader(csvfile)
            headers=next(reader)
            
            
            MRA_termsList_noreturn =[]
            modified_termsList_noreturn =[]
            
            
            MRA_termsList1 = []
            modified_termsList1 = []
            searcherReturned_termList1 = []
            
            MRA_termsList2 = []
            modified_termsList2 = []
            searcherReturned_termList2 = []
            
            MRA_termsList3 = []
            modified_termsList3 = []
            searcherReturned_termList3 = []
            
            MRA_termsList4 = []
            modified_termsList4 = []
            searcherReturned_termList4 = []
            
            MRA_termsList5 = []
            modified_termsList5 = []
            searcherReturned_termList5 = []
            
            # returned_tokensList = []
            # original_tokensList = []
            
            for row in reader:
                
                count_total+=1
                # read strings
                # the 1st col is MRA_term , 2nd is Modified_term
                query_string_original=row[0]
                query_string_edited=row[1]
            
                #2. construct  Query
                clauses=tokenize(query_string_edited,self.analyzer)
                # if only one vocabulary
                if len(clauses)==1:
                    query= FuzzyQuery(Term("pt",query_string_edited))
                else:
                    for i, val in enumerate(clauses):
                        clauses[i] =  SpanMultiTermQueryWrapper(FuzzyQuery( Term("pt", clauses[i])))
                    query = SpanNearQuery(clauses,1, True)
    
                topDocs = searcher.search(query, 5)
                scoreDocs = topDocs.scoreDocs
                # print ("%s total matching documents." % len(scoreDocs))
                # print(scoreDocs)
        
                matched = False
                #  if no matching at all
                if (len(scoreDocs)==0): 
                    no_returned += 1
                    MRA_termsList_noreturn += [query_string_original]
                    modified_termsList_noreturn += [query_string_edited]
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
                                searcherReturned_termList1 += [returned_string_matching]
                            
                            elif i==1 and matched == False:
                                MRA_termsList2 += [query_string_original]
                                modified_termsList2 += [query_string_edited]
                                searcherReturned_termList2 += [returned_string_matching]
                            elif i==2 and matched == False:
                                MRA_termsList3 += [query_string_original]
                                modified_termsList3 += [query_string_edited]
                                searcherReturned_termList3 += [returned_string_matching]
                            elif i==3 and matched == False:
                                MRA_termsList4 += [query_string_original]
                                modified_termsList4 += [query_string_edited]
                                searcherReturned_termList4 += [returned_string_matching]
                            elif i==4 and matched == False:
                                MRA_termsList5 += [query_string_original]
                                modified_termsList5 += [query_string_edited]
                                searcherReturned_termList5 += [returned_string_matching]
                            
                            
                            #returned phrase contains additional words
                            # if len(returned_tokens) > len(original_tokens):
                            #     returned_tokensList += [returned_string_matching]
                            #     original_tokensList += [query_string_original]
                               
                            
                            # with open("unmatched1stResult.csv","a+",newline="") as csvfile:
                            #     csvwriter=csv.writer(csvfile)
                                # csvwriter.writerow([query_string_original,query_string_edited,returned_string_matching])
                            
            
            
            # doc_1stMatch = searcher.doc(scoreDocs[0].doc)
            # returned_string_matching = doc_1stMatch.getField('pt').stringValue()
            # if returned_string_matching != query_string_original: 
            #     print("unmatched: ", returned_string_matching)
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
                             'SearcherReturned_term':searcherReturned_termList1,
                             'State':["Unmatched"]*len(MRA_termsList1), 
                             'Rank': ["1st"]*len(MRA_termsList1)}
        
        unmatchedTerms_dict2={'MRA_term':MRA_termsList2,
                             'Modified_term':modified_termsList2,
                             'SearcherReturned_term':searcherReturned_termList2,
                             'State':["Unmatched"]*len(MRA_termsList2), 
                             'Rank': ["2nd"]*len(MRA_termsList2)}
        
        unmatchedTerms_dict3={'MRA_term':MRA_termsList3,
                             'Modified_term':modified_termsList3,
                             'SearcherReturned_term':searcherReturned_termList3,
                             'State':["Unmatched"]*len(MRA_termsList3), 
                             'Rank': ["3rd"]*len(MRA_termsList3)}
        
        unmatchedTerms_dict4={'MRA_term':MRA_termsList4,
                             'Modified_term':modified_termsList4,
                             'SearcherReturned_term':searcherReturned_termList4,
                             'State':["Unmatched"]*len(MRA_termsList4), 
                             'Rank': ["4th"]*len(MRA_termsList4)}
        
        unmatchedTerms_dict5={'MRA_term':MRA_termsList5,
                             'Modified_term':modified_termsList5,
                             'SearcherReturned_term':searcherReturned_termList5,
                             'State':["Unmatched"]*len(MRA_termsList5), 
                             'Rank': ["5th"]*len(MRA_termsList5)}
        noreturnedTerms_dict = {'MRA_term':MRA_termsList_noreturn,
                             'Modified_term':modified_termsList_noreturn,
                             'State':["NO return"]*len(MRA_termsList_noreturn)}
        
        return(unmatchedTerms_dict1,unmatchedTerms_dict2,
               unmatchedTerms_dict3,unmatchedTerms_dict4,unmatchedTerms_dict5,noreturnedTerms_dict,results)
    
    def listUmatchedTokens(self,unmatchedTerms_dict):
        unmatchedMRA_termList = unmatchedTerms_dict["MRA_term"]
        # add all tokens list in one list
        unmatched_tokensList=[]
        for term in unmatchedMRA_termList:
            tokens = tokenize(term,self.analyzer)
            unmatched_tokensList += tokens
        return (unmatched_tokensList)
        
    # def staticUnmatchedTokens(self,unmatchedTerms_dict):
    #     unmatched_tokensList = self.listUmatchedTokens(unmatchedTerms_dict)
    #     unmatched_tokensDict = {"unmatched_tokens":unmatched_tokensList,"count":[1]*len(unmatched_tokensList)}
    #     unmatched_tokensDf = pandas.DataFrame(unmatched_tokensDict)
    #     unmatchedTokens=unmatched_tokensDf.groupby('unmatched_tokens').sum()
    #     gram1 = unmatchedTokens.sort_values("count",ascending = False)
    #     return (gram1)
    
    # produce the most popular token in terms which do not match with the returned results   
    def static1Gram(self,unmatchedTerms_dict):
        unmatched_tokensList = self.listUmatchedTokens(unmatchedTerms_dict)
        
        return((pandas.Series(nltk.ngrams(unmatched_tokensList,1)).value_counts()))
    # produce the most popular 2-grams       
    def static2Grams(self,unmatchedTerms_dict):
        
        unmatchedMRA_termList = unmatchedTerms_dict["MRA_term"]
        # add all tokens list in one list
        allTerms_grams2 = pandas.Series([])
        for term in unmatchedMRA_termList:
            tokens = tokenize(term,self.analyzer)
            term_grams2 = pandas.Series(nltk.ngrams(tokens,2)).value_counts()
            
            allTerms_grams2 = allTerms_grams2.add(term_grams2, fill_value=0)
        return(allTerms_grams2)
    
    # produce the most popular 3-grams
    def static3Grams(self,unmatchedTerms_dict):
        unmatchedMRA_termList = unmatchedTerms_dict["MRA_term"]
        # add all tokens list in one list
        allTerms_grams3 = pandas.Series([])
        for term in unmatchedMRA_termList:
            tokens = tokenize(term,self.analyzer)
            term_grams3 = pandas.Series(nltk.ngrams(tokens,3)).value_counts()
            
            allTerms_grams3 = allTerms_grams3.add(term_grams3, fill_value=0)
        return(allTerms_grams3)
    
    
    # 1. if input term and returned term have the same length, find which token is replaced and store in list
    # 2. if the returned terms are longer or shorter than inout term, find and store them in lists
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
        returnedShorterTerms =[]
        MRA_termsList_shortReturn =[]
        
        returnedLongerTerms =[]
        MRA_termsList_longReturn =[]
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
                # print(tokenmissed_count,unmatchedReturned_termList[index])
                returnedShorterTerms += [unmatchedReturned_termList[index]]
                MRA_termsList_shortReturn += [term]

            # returned term is longer than original terms (i.e. new words are added)
            else:
                tokenadded_count +=1
                returnedLongerTerms += [unmatchedReturned_termList[index]]
                MRA_termsList_longReturn += [term]
                

                
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
        longReturn_df = pandas.DataFrame({"MRA_terms":MRA_termsList_longReturn,"Returned": returnedLongerTerms})
        shortReturn_df = pandas.DataFrame({"MRA_terms":MRA_termsList_shortReturn,"Returned": returnedShorterTerms})
        
        unfound_addedTokens_df2 = unfound_addedTokens_df2.groupby(["unfoundTokens","addedTokens"]).sum().sort_values("count",ascending = False)
        print(tokenmissed_count,"tokens are not missed", tokenadded_count,"have added words")
        return (unfound_addedTokens_df2,longReturn_df,shortReturn_df)
        # return(unfoundTokens_df,addedTokens_df,unfound_addedTokens_df)
        
    # find tokens are not matched in top 5 returned results   
    def produceAllTop5UnmatchedPaires(self, matchingRes):
        unmatchedTerms_dict1 = matchingRes[0]
        unmatchedTerms_dict2 = matchingRes[1]
        unmatchedTerms_dict3 = matchingRes[2]
        unmatchedTerms_dict4 = matchingRes[3]
        unmatchedTerms_dict5 = matchingRes[4]
        unfound_addedTokens_df1st= self.findUnmatchedTokens(unmatchedTerms_dict1)[0]
        unfound_addedTokens_df2nd= self.findUnmatchedTokens(unmatchedTerms_dict2)[0]
        unfound_addedTokens_df3rd= self.findUnmatchedTokens(unmatchedTerms_dict3)[0]
        unfound_addedTokens_df4th= self.findUnmatchedTokens(unmatchedTerms_dict4)[0]
        unfound_addedTokens_df5th= self.findUnmatchedTokens(unmatchedTerms_dict5)[0]
            
            
        return(unfound_addedTokens_df1st,unfound_addedTokens_df2nd,unfound_addedTokens_df3rd,unfound_addedTokens_df4th,unfound_addedTokens_df5th)
    # find returned terms which contain some more tokens than input in top 5 
    def produceAllTop5UnmatchedPairesLongReturn(self, matchingRes):
        unmatchedTerms_dict1 = matchingRes[0]
        unmatchedTerms_dict2 = matchingRes[1]
        unmatchedTerms_dict3 = matchingRes[2]
        unmatchedTerms_dict4 = matchingRes[3]
        unmatchedTerms_dict5 = matchingRes[4]
        longReturnTerms_df1st= self.findUnmatchedTokens(unmatchedTerms_dict1)[1]
        longReturnTerms_df2nd= self.findUnmatchedTokens(unmatchedTerms_dict2)[1]
        longReturnTerms_df3rd= self.findUnmatchedTokens(unmatchedTerms_dict3)[1]
        longReturnTerms_df4th= self.findUnmatchedTokens(unmatchedTerms_dict4)[1]
        longReturnTerms_df5th= self.findUnmatchedTokens(unmatchedTerms_dict5)[1]
            
            
        return(longReturnTerms_df1st,longReturnTerms_df2nd,longReturnTerms_df3rd,longReturnTerms_df4th,longReturnTerms_df5th)
        

  
                
            
    # FuzzyQuery but change maxEdits 
    def fuzzySearcherWithMaxEdits(self, max_Edits):
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
    
        # read file
        with open(self.input_fileName, 'r') as csvfile:
            reader=csv.reader(csvfile)
            headers=next(reader)
            
            
            MRA_termsList_noreturn =[]
            modified_termsList_noreturn =[]
            
            
            MRA_termsList1 = []
            modified_termsList1 = []
            searcherReturned_termList1 = []
            
            MRA_termsList2 = []
            modified_termsList2 = []
            searcherReturned_termList2 = []
            
            MRA_termsList3 = []
            modified_termsList3 = []
            searcherReturned_termList3 = []
            
            MRA_termsList4 = []
            modified_termsList4 = []
            searcherReturned_termList4 = []
            
            MRA_termsList5 = []
            modified_termsList5 = []
            searcherReturned_termList5 = []
            
            # returned_tokensList = []
            # original_tokensList = []
            print(max_Edits)
            maxEdits_set = set()
            for row in reader:
                
                count_total+=1
                # read strings
                # the 1st col is MRA_term , 2nd is Modified_term
                query_string_original=row[0]
                query_string_edited=row[1]
            
                #2. construct  Query
                clauses=tokenize(query_string_edited,self.analyzer)
                # if only one vocabulary
                if len(clauses)==1:
                    query= FuzzyQuery(Term("pt",query_string_edited), max_Edits)
                    maxEdits_set.add(query.getMaxEdits())
                    # print(fq.getMaxEdits()) 
                else:
                    for i, val in enumerate(clauses):
                        fq = FuzzyQuery(Term("pt", clauses[i]),max_Edits)
                        clauses[i] =  SpanMultiTermQueryWrapper(fq)
                        maxEdits_set.add(fq.getMaxEdits())
                        # print(fq.getMaxEdits())
                    query = SpanNearQuery(clauses,1, True)
                
                topDocs = searcher.search(query, 5)
                scoreDocs = topDocs.scoreDocs
                # print ("%s total matching documents." % len(scoreDocs))
                # print(scoreDocs)
        
                matched = False
                #  if no matching at all
                if (len(scoreDocs)==0): 
                    no_returned += 1
                    MRA_termsList_noreturn += [query_string_original]
                    modified_termsList_noreturn += [query_string_edited]
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
                                searcherReturned_termList1 += [returned_string_matching]
                            
                            elif i==1 and matched == False:
                                MRA_termsList2 += [query_string_original]
                                modified_termsList2 += [query_string_edited]
                                searcherReturned_termList2 += [returned_string_matching]
                            elif i==2 and matched == False:
                                MRA_termsList3 += [query_string_original]
                                modified_termsList3 += [query_string_edited]
                                searcherReturned_termList3 += [returned_string_matching]
                            elif i==3 and matched == False:
                                MRA_termsList4 += [query_string_original]
                                modified_termsList4 += [query_string_edited]
                                searcherReturned_termList4 += [returned_string_matching]
                            elif i==4 and matched == False:
                                MRA_termsList5 += [query_string_original]
                                modified_termsList5 += [query_string_edited]
                                searcherReturned_termList5 += [returned_string_matching]
                            
                            
                            #returned phrase contains additional words
                            # if len(returned_tokens) > len(original_tokens):
                            #     returned_tokensList += [returned_string_matching]
                            #     original_tokensList += [query_string_original]
                               
                            
                            # with open("unmatched1stResult.csv","a+",newline="") as csvfile:
                            #     csvwriter=csv.writer(csvfile)
                                # csvwriter.writerow([query_string_original,query_string_edited,returned_string_matching])
                            
            
            
            # doc_1stMatch = searcher.doc(scoreDocs[0].doc)
            # returned_string_matching = doc_1stMatch.getField('pt').stringValue()
            # if returned_string_matching != query_string_original: 
            #     print("unmatched: ", returned_string_matching)
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
            "top5_percentage":"%.2f" %((matched_1st_count+matched_2nd_count+matched_3rd_count+matched_4th_count+matched_5th_count)/count_total*100),
            "maxEdits": max_Edits
            }
        
        unmatchedTerms_dict1={'MRA_term':MRA_termsList1,
                             'Modified_term':modified_termsList1,
                             'SearcherReturned_term':searcherReturned_termList1,
                             'State':["Unmatched"]*len(MRA_termsList1), 
                             'Rank': ["1st"]*len(MRA_termsList1)}
        
        unmatchedTerms_dict2={'MRA_term':MRA_termsList2,
                             'Modified_term':modified_termsList2,
                             'SearcherReturned_term':searcherReturned_termList2,
                             'State':["Unmatched"]*len(MRA_termsList2), 
                             'Rank': ["2nd"]*len(MRA_termsList2)}
        
        unmatchedTerms_dict3={'MRA_term':MRA_termsList3,
                             'Modified_term':modified_termsList3,
                             'SearcherReturned_term':searcherReturned_termList3,
                             'State':["Unmatched"]*len(MRA_termsList3), 
                             'Rank': ["3rd"]*len(MRA_termsList3)}
        
        unmatchedTerms_dict4={'MRA_term':MRA_termsList4,
                             'Modified_term':modified_termsList4,
                             'SearcherReturned_term':searcherReturned_termList4,
                             'State':["Unmatched"]*len(MRA_termsList4), 
                             'Rank': ["4th"]*len(MRA_termsList4)}
        
        unmatchedTerms_dict5={'MRA_term':MRA_termsList5,
                             'Modified_term':modified_termsList5,
                             'SearcherReturned_term':searcherReturned_termList5,
                             'State':["Unmatched"]*len(MRA_termsList5), 
                             'Rank': ["5th"]*len(MRA_termsList5)}
        noreturnedTerms_dict = {'MRA_term':MRA_termsList_noreturn,
                             'Modified_term':modified_termsList_noreturn,
                             'State':["NO return"]*len(MRA_termsList_noreturn)}
        
        return(unmatchedTerms_dict1,unmatchedTerms_dict2,
               unmatchedTerms_dict3,unmatchedTerms_dict4,unmatchedTerms_dict5,noreturnedTerms_dict,results, maxEdits_set)
    
        
        