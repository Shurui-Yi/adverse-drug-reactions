# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 12:58:20 2021

@author: yiysy003

Indexer function
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


def Indexer(fsDir, analyzer):


    # print(f"{writer.numDocs()} docs found in index")


    #define field settings
    t2 = FieldType()
    t2.setStored(True)
    t2.setTokenized(True)
    t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    #construct indexWriter
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(fsDir, config)


    # add your logic to add documents to index
    # list stored all MRA pt
    pt_list=[]
    # read MRA
    with open('pt.asc','r') as f:
        lines=f.readlines()
        for line in lines:
        
            record = line.split("$",4)
            pt_code_temp= record[0]
            pt_temp=record[1]
            # print(pt_code_temp,pt_temp)
            # Add a document
            doc = Document()
            # doc.add(Field('pt_code', pt_code_temp, t2 ))
            doc.add(Field('pt', pt_temp,t2))
            # if "/" in doc.getField('pt').stringValue():
            #     print(doc.getField('pt_code').stringValue(),doc.getField('pt').stringValue())
            pt_list.append(doc.getField('pt').stringValue())

            writer.addDocument(doc)
    writer.commit()
    writer.close()
    return (pt_list)
    