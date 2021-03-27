# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 17:05:52 2021

@author: yiysy003

Simulation class
"""
import csv, datetime, pandas
from itertools import combinations, product
from functions import *

class SynsSimulation:
    #instantiating
    def __init__(self, pt_list,directory, analyzer,syns_dic,simultion_type):
       
        # input list for simulation
        self.pt_list = pt_list
        self.directory=directory
        self.analyzer=analyzer
        self.syns_dic=syns_dic
        # SYNONYM or MODIFICATION
        self.simultion_type= simultion_type

        
    def replace1WordWithSyn(self):
       
        # Calulate how many words having syns in each term
        countWordsWithSyns_dic={}
        words_num_list=[]
        wordsWithSyns_count_list=[]
        
        newTerms_list=[]
        pt_sumList=[]
        # Go through each term    
        for term in self.pt_list:
            
            wordsWithSyns_count=0
            
            tokens= tokenize(term, self.analyzer)

            for index, token in enumerate(tokens):
                # tokens_temp = tokens
                # print(tokens_temp)
                if token in self.syns_dic:
                    wordsWithSyns_count+=1
                    for syn in self.syns_dic[token]:
                        tokens_temp = list(tokens)
                        # print(tokens_temp)
                        tokens_temp[index] = syn                        
                        newTerm =" ".join(tokens_temp)                        
                        newTerms_list += [newTerm]
                        pt_sumList += [term]

       
        newTerms_dict = {"MRA_term":pt_sumList,
                        "Replaced_term":newTerms_list,
                        "replacement_total":[1]*len(pt_sumList)}
        
        newTerms_df= pandas.DataFrame(newTerms_dict)
        # print(comb_sum)
        return (newTerms_df)
    
    
    def replace2WordsWithSyn(self):
        
        # Calulate how many words having syns in each term
        countWordsWithSyns_dic={}
        words_num_list=[]
        wordsWithSyns_count_list=[]
        newTerms_count=0
        # store all new created terms
        newTerms_list=[]
        comb_sum=0
        pt_sumList=[]
        # Go through each term    
        for term in self.pt_list:
            
            wordsWithSyns_count=0
            
            tokens= tokenize(term, self.analyzer)
            # Only select terms having more than 1 (i.e. 2 and more) words/tokens
            if len(tokens)>1:
                
                synsNum_list=[]
                # create a 2 dimesional list: from up to down each row presents one token, and all syns stored in rows
                term_matrix=[]
                wordsWithSyns_indexList=[]
                # go through each token (i.e. words) in the term
                for index, token in enumerate(tokens):
                    row=[token]
                    if token in self.syns_dic:
                        wordsWithSyns_count+=1
                        # store the index numbers of each word having synonyms in a list (i.e. wordsWithSyns_indexList)
                        wordsWithSyns_indexList = wordsWithSyns_indexList + [index]
                        # go though all syns of the word and store them in a list (i.e. row)
                        row += self.syns_dic[token]
                        synsNum_list += [len(self.syns_dic[token])]
                    # store found syns of the token in the matrix
                    term_matrix.append(row)
                
                
                # calculate the number of tokens in the term after tokenization
                tokens_num = len(term_matrix)
                # words_num=len(term_matrix)
                # words_num_list.append(words_num)
                # wordsWithSyns_count_list.append(wordsWithSyns_count)
                
                # make sure there are at least 2 words having syns
                # if wordsWithSyns_count >1:
                if len(synsNum_list)>=2:
                    
                    # Get all combinations, and store sets in a list (i.e.comb_inedexPairList )
                    comb_inedexPairList= list(combinations(wordsWithSyns_indexList,2))
                    comb_list=list(combinations((synsNum_list),2))
                    for comb in comb_list:
                        comb_sum+=comb[0]*comb[1]
                    
                    for indexPair in comb_inedexPairList:
                        # get two index numbers of the selected words
                        index1 = indexPair[0]
                        index2= indexPair[1]
                        # get the two syns lists used for replacement (remove the original word in lists by list slicing)
                        syns_list1 = term_matrix[index1][1:]
                        syns_list2 = term_matrix[index2][1:]
                        
                        # get all combinations of syns of two selected words
                        comb_synsPairList = list(product(syns_list1,syns_list2))
                        
                        newTerms_num = len(comb_synsPairList)
                        
                        newTerms_count+=newTerms_num
                        # create a 2 dimesional list storing new created terms by replacing with 2 syns 
                        # newTerms_matrix= [tokens]*newTerms_num
                        string_template = list(tokens)
                        for comb_synsPair in comb_synsPairList:
                            string_template[index1] = comb_synsPair[0]
                            string_template[index2] = comb_synsPair[1]
                            
                            string=" ".join(string_template)
                            # with open(output_fileName,"a+",newline="") as csvfile:
                            #     csvwriter=csv.writer(csvfile)
                            #     csvwriter.writerow([string])
                            newTerms_list += [string]
                            pt_sumList += [term]
                   
        #         countWordsWithSyns_dic={'words_num':words_num_list,'wordsWithSyns_count':wordsWithSyns_count_list}
        #         countWordsWithSyns_df=pandas.DataFrame(countWordsWithSyns_dic)
        # newTerms_dict= {"replaced2SynsMRATerms":newTerms_list}
        newTerms_dict = {"MRA_term":pt_sumList,
                       "Replaced_terms":newTerms_list,
                       "replacement_total":[2]*len(pt_sumList)}
        
        newTerms_df= pandas.DataFrame(newTerms_dict)
        # print(comb_sum)
        return (newTerms_df)
    
    

# calculate all many combinations    
    def calculateCombinations(self,comb_length):
  
        # store how many combinations 
        comb_sum=0
        for term in self.pt_list:
            
            # wordsWithSyns_count=0
            
            tokens= tokenize(term, self.analyzer)
            # Only select terms having more than 1 (i.e. 2 and more) words/tokens
            if len(tokens)>1:
                                
                # create a 2 dimesional list: from up to down each row presents one token, and all syns stored in rows
                synsNum_list=[]
                
                # go through each token (i.e. words) in the term
                for index, token in enumerate(tokens):
                    if token in self.syns_dic:
                        # wordsWithSyns_count+=1
                        synsNum_list += [len(self.syns_dic[token])]
                        
                if len(synsNum_list)>= comb_length:
                    
                    comb_list=list(combinations((synsNum_list),2))
                    for comb in comb_list:
                        comb_sum+=comb[0]*comb[1]

        return (comb_sum)
    

    # def writeCSVFile(self, output_fileName):
    #     # output_fileName= "syns2Simulated.csv"
    #     #write headline
    #     created_time=datetime.datetime.now()
    #     created_time= created_time.strftime("%d-%m-%Y %H:%M")
    #     fields=["simulated_term", "MRA_term",created_time]
        
        
    #     with open(output_fileName,"a+",newline='') as csvfile:
    #         csvwriter=csv.writer(csvfile)
    #         csvwriter.writerow(fields)
        
        
  



                    
    
    
            
    