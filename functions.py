# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 14:43:50 2021

@author: yiysy003
all functions
"""
import string, random, numpy

#check if all modification is valid
def checkValidModification(newTerms_df):   
    #compare the number of modification and the sum of edit distance of each token in the term
    comparison_col= numpy.where(newTerms_df["modification_total"] <= newTerms_df["edit_distance_tokens"],0,1)
    
    #compare the number of modification and edit distance of the whole term (i.e. tokens are linked by space)
    # comparison_col= numpy.where(newTerms_df["modification_total"] <= newTerms_df["edit_distance"],0,1)
    if numpy.sum(comparison_col) == 0:
        # all edit distance is larger than modification number
        return(True)
    else:
        return(comparison_col)

# wordnet import
from nltk.corpus import wordnet
# tokenizition import
from java.io import StringReader
from org.apache.lucene.analysis.standard import StandardTokenizer 
from org.apache.lucene.analysis.tokenattributes import CharTermAttribute 


# getSyns: find the synonyms of each vocabulary in MRA term
# Return a dictionary storing those tokens having syns and derivationally related forms
# pt_list: preferred terms stored in a list
# analyzer: decide how to split terms into tokens
def getSyns(pt_list,analyzer):
    # token_dic: stores all tokens as key; its synonyms and derivationally related forms as key values
    token_dic={}
    # tokenSyns_dic; stores all tokens as key; its synonyms as values
    tokenSyns_dic={}
    # tokenRelated_dic; stores all tokens as key; its synonyms as values
    tokenRelated_dic={}
    
    # Go though each term, find syns and other forms. Only store those tokens which have key values.
    for term in pt_list:
        
        # tokenization
        tokens=tokenize(term, analyzer)
        # Go though each token
        for token in tokens:
            # For tokens which have not been store in the output dicionary
            if token not in token_dic:
                # 
                syns_set=set()
                formsRelated=set()
                syns_forms_set=set()
                syns = wordnet.synsets(token)
                if len(syns) != 0:
                    # for i in range(0,len(syns)):
    
                    #     for j in range(0,len(syns[i].lemmas())):
                    #         # print(syns[i].definition())
                    #         print(syns[i].lemmas()[j].name())
                            # syns_set.add(syns[i].lemmas()[j].name())
                    for syn in syns:
                        for lemma in syn.lemmas():
                            if lemma.name() != token:
                                syns_set.add(lemma.name())
                                syns_forms_set.add(lemma.name())
                                
                            for form in lemma.derivationally_related_forms():
                                if form.name() != token:
                                    formsRelated.add(form.name())
                                    syns_forms_set.add(form.name())
                            
                if len(syns_forms_set) != 0:
                    tokenSyns_dic[token]=list(syns_set)
                    tokenRelated_dic[token]=list(formsRelated)
                    token_dic[token]=list(syns_forms_set)
        # stream.close()
    return(token_dic)

# tokenize: tokenize input phrase into word list; 
# Return the word (i.e. tokens) list 
# term: phase for tokenizion
# analyzer: decide which method is applied for spliting the phrase
def tokenize(term,analyzer):
    #tokenize
    # "" is the field name
    stream = analyzer.tokenStream("", StringReader(term))
    stream.reset()
    tokens=[]
    while stream.incrementToken():
        tokens.append(stream.getAttribute(CharTermAttribute.class_).toString())
    stream.close()
    return (tokens)




import datetime
import csv, pandas
def createTime():
    created_time= datetime.datetime.now()
    created_time=created_time.strftime("%d-%m-%Y %H:%M")    
    return (created_time)
def addCreatedTimetoDf(dataFrame):
    created_time_df= pandas.DataFrame({"created_time":list(createTime())})
    newDf = pandas.concat([dataFrame, created_time_df], ignore_index= True, axis = 1)
    return (newDf)

# write dataframe to a csv file
def writeDftoCSVFile(dataFrame, outputFileName,writeIndex):
    #index can be changed as False
    dataFrame.to_csv(outputFileName, index= writeIndex)
# write dictionary to csv file
def writeDicttoCSVFile(dictionary, outputFileName):
    pandas.DataFrame(dictionary).to_csv(outputFileName, index= False)

# write reults to csv files
#(i) write the header
def writeStatisticHeadertoCSVFile():
    searcher_results_fields =["input_fileName",
            "unmatched_1st_count",
            "macthed_1st_count",
            "macthed_2nd_count",
            "macthed_3rd_count",
            "macthed_4th_count",
            "macthed_5th_count",
            "no_returned",
            "count_total",
            "top1_percentage",
            "top2_percentage",
            "top3_percentage",
            "top4_percentage",
            "top5_percentage"]
    #create file name
    # input_fileName= results["input_fileName"]
    # output_fileName=input_fileName[:-4]+'_SearcherResults.csv'
    with open ("SearchingResults.csv","a+",newline='') as csvfile:
        csvwriter= csv.DictWriter(csvfile,fieldnames=searcher_results_fields)
        csvwriter.writeheader()
#(ii) write the results        
def writeStatisticResDicttoCSVFile(results):
    searcher_results_fields =["input_fileName",
            "unmatched_1st_count",
            "macthed_1st_count",
            "macthed_2nd_count",
            "macthed_3rd_count",
            "macthed_4th_count",
            "macthed_5th_count",
            "no_returned",
            "count_total",
            "top1_percentage",
            "top2_percentage",
            "top3_percentage",
            "top4_percentage",
            "top5_percentage"]
    #create file name
    # input_fileName= results["input_fileName"]
    # output_fileName=input_fileName[:-4]+'_SearcherResults.csv'
    with open ("SearchingResults.csv","a+",newline='') as csvfile:
        csvwriter= csv.DictWriter(csvfile,fieldnames=searcher_results_fields)
        # csvwriter.writeheader()
        csvwriter.writerow(results)
# write results to csv files (baseline for different maxEdits)      
#write header  
def writeStatisticHeadertoCSVFile2():
    searcher_results_fields =["input_fileName",
            "unmatched_1st_count",
            "macthed_1st_count",
            "macthed_2nd_count",
            "macthed_3rd_count",
            "macthed_4th_count",
            "macthed_5th_count",
            "no_returned",
            "count_total",
            "top1_percentage",
            "top2_percentage",
            "top3_percentage",
            "top4_percentage",
            "top5_percentage",
            "maxEdits"]
    #create file name
    # input_fileName= results["input_fileName"]
    # output_fileName=input_fileName[:-4]+'_SearcherResults.csv'
    with open ("SearchingResults_changedEdits.csv","a+",newline='') as csvfile:
        csvwriter= csv.DictWriter(csvfile,fieldnames=searcher_results_fields)
        csvwriter.writeheader()
# write results        
def writeStatisticResDicttoCSVFile2(results):
    searcher_results_fields =["input_fileName",
            "unmatched_1st_count",
            "macthed_1st_count",
            "macthed_2nd_count",
            "macthed_3rd_count",
            "macthed_4th_count",
            "macthed_5th_count",
            "no_returned",
            "count_total",
            "top1_percentage",
            "top2_percentage",
            "top3_percentage",
            "top4_percentage",
            "top5_percentage",
            "maxEdits"]
    #create file name
    # input_fileName= results["input_fileName"]
    # output_fileName=input_fileName[:-4]+'_SearcherResults.csv'
    with open ("SearchingResults_changedEdits.csv","a+",newline='') as csvfile:
        csvwriter= csv.DictWriter(csvfile,fieldnames=searcher_results_fields)
        # csvwriter.writeheader()
        csvwriter.writerow(results)
        
        
import numpy

# get all terms which have punctuations
def calculatePunctuationNum(term_list):
    punctuation_dict ={}
    terms_dict={}
    for term in term_list:
        for char in term:
            # return char which is not number, character, and space
            if not char.isdigit() and not char.isalpha() and char != " ":
                if char not in punctuation_dict:
                    punctuation_dict[char] = 1
                    terms_dict[char] = [term]
                else:
                    punctuation_dict[char] = punctuation_dict[char] + 1
                    terms_dict[char] = terms_dict[char] + [term]
    return (punctuation_dict,terms_dict)

        
# get the maximum length of tokens in each term
def getMaxLengthOfTokenPerTerm(noReturn_df, analyzer,modificationPercentage):
    MRA_list = list(noReturn_df["MRA_term"])
    Modified_list = list (noReturn_df["Modified_term"])
    # maximum of lengh is set as 30
    length_max_list= [0]*31
    edit1_list=[]
    edit2_list=[]
    for term in MRA_list:
        tokens = tokenize(term,analyzer)
        length_max = 0
        for token in tokens:
            length = len(token)
            if length > length_max:
                length_max = length
        length_max_list[length_max] += 1
        if round(length_max*modificationPercentage) == 1:
            edit1_list += [term]
        elif round(length_max*modificationPercentage) == 2:
            edit2_list += [term]

        
    return (length_max_list,edit1_list,edit2_list)
