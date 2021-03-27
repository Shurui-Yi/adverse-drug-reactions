# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 12:02:57 2021

@author: yiysy003
"""
from functions import *
from nltk.metrics import edit_distance
import pandas, numpy,csv, itertools

class TypoSimulation:
    
    def __init__(self, pt_list,directory, analyzer,simulation_type,simulation_round,modificationPercentage):
        self.pt_list = pt_list
        self.directory = directory
        self.analyzer = analyzer
        self.simulation_type = simulation_type
        self.simulation_round = simulation_round
        self.modificationPercentage=modificationPercentage
    
    
    #modify N pecentage error rate for each word not term
    def modifyNpPerWord(self):
        # store the modified results
        rows_modified=[]
        newTerms_list=[]
        edit_distance_sumList=[]
        edit_distance_sumList_tokens=[]
        modificationNum_sumList=[]
        # go through each term 
        for i in range(0,len(self.pt_list)):
            
            # get the term
            query_string_original=self.pt_list[i]
            
            # tokenization
            tokens = tokenize(query_string_original,self.analyzer)
            
            # Go through each round
            for j in range(0,self.simulation_round):
                # Go through each token
                word_edited_list=[]
                modificationNum=0
                # print(tokens)
                substitution_cost_sum=0
                transpositions_valid_term = False
                edit_distance_sum = 0
                edit_distance_tokens_sum = 0
                modificationNum_sum=0
                for index,token in enumerate(tokens):
                    charNum = len(token)   
                    modificationNum=round((self.modificationPercentage)*charNum)
                    modificationNum_sum += modificationNum
                    # operationNum_ins=0
                    # modify for k times
                    word_edited=token
                    for k in range(1,modificationNum+1):                            
                        pos_valid=False
                        # choose untile it's a valid modification
                        while not pos_valid:
                            # randomly select one type of errors  
                            modificationType=self.__ranSelectModification(word_edited)
                            # if deletion/ insertion/ substitution is chosen, then one postion of char should be selected, 
                            # and attention the char should not be modified
                            # before, i.e. the edit distance should increase by 1.
                            if modificationType=="deletion" or modificationType=="insertion" or modificationType=="substitution":            
                                # select 1 char randomly
                                # print(word_edited)
                                char_pos=self.__ranSelect1Char(word_edited)
                                
                                # modification
                                if modificationType=="deletion":
                    
                                    #1.delete 1 char
                                    word_edited = self.deletion(word_edited, char_pos)
                                elif modificationType=="insertion":
                                    #2.insert 1 char
                                    word_edited = self.insertion(word_edited, char_pos)
                                elif modificationType=="substitution":                
                                    #3.substitute 1 char
                                    word_edited = self.substitution(word_edited, char_pos)
                                    # substitution_cost+=1
                                    # substitution_cost_sum+=1
                            # if it's transposition, then 2 char positions have to be selected
                            elif modificationType=="transposition":
                                 ## select 2 char randomly
                                 char_pos=self.__ranselect2TransChars(word_edited)
                                 pos1=char_pos[0]
                                 pos2=char_pos[1]       
                                 #4.switch 2 char
                                 word_edited = self.transposition(word_edited, pos1, pos2)
                                 
                            # calculate distance
                            new_edit_distance = edit_distance(token,word_edited,1,True)                             
                            # determine if it is valid modification 
                            if new_edit_distance >= k:
                                pos_valid=True
                                # sum of all edit distance of token
                                edit_distance_tokens_sum += new_edit_distance
                                # operationNum+=1
                            else:
                                pos_valid=False
                    word_edited_list += [word_edited] 
                
                query_string_edited= " ".join(word_edited_list)
                # calculate the edit distance of the whole term
                edit_distance_sum = edit_distance(query_string_original,query_string_edited,1,True)
                edit_distance_sumList +=  [edit_distance_sum]
                
                edit_distance_sumList_tokens +=  [edit_distance_tokens_sum]
                    
                # print(k,modificationNum,query_string_edited,query_string_original,new_edit_distance)
                # store all new modified terms in list
                newTerms_list += [query_string_edited] 
                modificationNum_sumList += [modificationNum_sum]
                # rows_modified.append(["mixed",modificationNum,query_string_edited,query_string_original,new_edit_distance])
        
        pt_sumList = list(itertools.chain.from_iterable(itertools.repeat(i, self.simulation_round) for i in self.pt_list))
        newTerm_dict= {"MRA_term":pt_sumList,
                       "Modified_terms":newTerms_list,
                       "modification_total":modificationNum_sumList,
                       "edit_distance":edit_distance_sumList,
                       "edit_distance_tokens":edit_distance_sumList_tokens}
        newTerms_df= pandas.DataFrame(newTerm_dict)
        print("5 round",self.modificationPercentage)
        return (newTerms_df)
    
    
    def writeDictFile(self , output_dict):
        if self.simulation_type =="TYPO_MIXING":
            output_fileName = "typo"+str(self.modificationPercentage)+"pSimulatedDataset.csv"
        fields = list(output_dict.keys())
        with open (output_fileName,'w',newline="") as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames = fields )
            csvwriter.writeheader()
            csvwriter.writerow(output_dict)


    def __ranSelectModification(self,token):
        if self.__checkTransValidity(token):
            n= random.randint(0,3)
        else:
            n= random.randint(0,2)
        modificationType=["deletion", "insertion","substitution","transposition"]
        return modificationType[n]


    def __ranSelect1Char(self,token):
         return random.randint(0,len(token)-1)
    
    def __ranselect2TransChars(self, token):
        ran_position = random.randint(0,len(token)-1)
        pos1=ran_position
        valid_position =False
        while valid_position == False:
            
            if pos1 == 0:
                pos2 = 1
            elif pos1 == len(token)-1:
                pos2 = len(token)-2
            else:
                ran = random.choice([-1,1])
                pos2 = pos1 + ran
            
            if token[pos1]==token[pos2] :
                valid_position = False  
                pos1 = random.randint(0,len(token)-1)
            else:
                valid_position = True
          # pos1 must be smaller      
        if pos1>pos2:
              pos_temp=pos1
              pos1=pos2
              pos2=pos_temp
        return (pos1,pos2)
        
    
    
    def __checkTransValidity(self,token):
        #check if the token can have the transform error
        # if the token is only one letter
        if token[0]*len(token) == token:
            trans_valid= False
        else:
            trans_valid =True
        return (trans_valid)
    
    def deletion(self,word_selected,char_pos):
        word_edited= word_selected[:char_pos]+word_selected[char_pos+1:]
        return (word_edited)
    
    def insertion(self,word_selected,char_pos):
        if word_selected[char_pos].isalpha():
            ran = random.choice(string.ascii_lowercase)
        
        elif word_selected[char_pos].isdigit():
            ran= str(random.randint(0, 9))
        elif word_selected[char_pos] == '\'':
            ran = random.choice(["c","v","b"])
        elif word_selected[char_pos] == '(':
            ran = random.choice(["j","k","l"])
        elif word_selected[char_pos] == ')':
            ran = random.choice(["k","l"])
        elif word_selected[char_pos] == '*':
            ran = random.choice(["d","f","g"])
        elif word_selected[char_pos] == ',':
            ran = random.choice([" "])
        elif word_selected[char_pos] == '-':
            ran = random.choice(["f","g","h"])
        elif word_selected[char_pos] == '.':
            ran = random.choice([" "])
        elif word_selected[char_pos] == '/':
            ran = random.choice(["n","m"])
        else:
            print(word_selected[char_pos])
        # if the selected character is not the last one, 
        # then insert the random char before the selected position
        if char_pos != (len(word_selected)-1):
            word_edited=  word_selected[:char_pos] + ran + word_selected[char_pos:]
        # if it is the last one, then there is one more situation that
        # it could be added at the end (after the position)
        else:
            n=random.randint(0, 1)
            # add before the last character/ initial 
            if n==0:
                word_edited=  word_selected[:char_pos] + ran + word_selected[char_pos:]
                # add after the end /initial
            else:
                word_edited=  word_selected+ ran 
    
        return(word_edited)
                
                
    
    def substitution(self,word_selected,char_pos):
        if word_selected[char_pos].isalpha():
            ran = random.choice(string.ascii_lowercase)
        
        elif word_selected[char_pos].isdigit():
            ran= str(random.randint(0, 9))
        elif word_selected[char_pos] == '\'':
            ran = random.choice(["c","v","b"])
        elif word_selected[char_pos] == '(':
            ran = random.choice(["j","k","l"])
        elif word_selected[char_pos] == ')':
            ran = random.choice(["k","l"])
        elif word_selected[char_pos] == '*':
            ran = random.choice(["d","f","g"])
        elif word_selected[char_pos] == ',':
            ran = random.choice([" "])
        elif word_selected[char_pos] == '-':
            ran = random.choice(["f","g","h"])
        elif word_selected[char_pos] == '.':
            ran = random.choice([" "])
        elif word_selected[char_pos] == '/':
            ran = random.choice(["n","m"])
            
        word_edited=  word_selected[:char_pos] + ran + word_selected[char_pos+1:]
        return (word_edited)
    
    
    
    def transposition(self,word_selected,char_pos1,char_pos2):
        char1= word_selected[char_pos1]
        char2= word_selected[char_pos2]
        word_edited = word_selected[:char_pos1]+char2+char1+word_selected[char_pos2+1:]
        return (word_edited)   
