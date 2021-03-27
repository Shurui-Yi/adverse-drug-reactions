# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 20:37:04 2021
Test how FuzzyQuery works for matching single character
@author: -
"""

JVM_DLL_PATH = 'C:/Program Files/AdoptOpenJDK/jdk-8.0.275.1-hotspot/jre/bin/server'

# Ensure paths are correct to find the jvm.dll for lucene
import os
path = os.environ['Path'].split(os.pathsep)
path.append(JVM_DLL_PATH)
os.environ['Path'] = os.pathsep.join(path)
#install pylucene from http://lucene.apache.org/pylucene/




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


lucene.initVM(vmargs=['-Djava.awt.headless=true'])
#set analyzer and directory
fsDir = MMapDirectory(Paths.get('index'))
analyzer = StandardAnalyzer()

t2 = FieldType()
t2.setStored(True)
t2.setTokenized(True)
t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
doc = Document()
# doc.add(Field('pt_code', pt_code_temp, t2 ))
doc.add(Field('pt', "x",t2))
doc.add(Field('pt', "i",t2))


# doc.add(Field('pt', "ii",t2))
# if "/" in doc.getField('pt').stringValue():
#     print(doc.getField('pt_code').stringValue(),doc.getField('pt').stringValue())
#construct indexWriter
config = IndexWriterConfig(analyzer)
config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
writer = IndexWriter(fsDir, config)
writer.addDocument(doc)
writer.commit()
writer.close()

searcher=IndexSearcher(DirectoryReader.open(fsDir))

query= FuzzyQuery(Term("pt","i"))
print(query.getMaxEdits())
topDocs = searcher.search(query, 5)
scoreDocs = topDocs.scoreDocs
                
for i,var in enumerate(scoreDocs):
    doc_matching = searcher.doc(scoreDocs[i].doc)
    returned_string_matching = doc_matching.getField('pt').stringValue()
    print(returned_string_matching)





                


##
clauses = ['a','ab']
for i, val in enumerate(clauses):
    clauses[i] =  SpanMultiTermQueryWrapper(FuzzyQuery( Term("pt", clauses[i])))
query = SpanNearQuery(clauses,1, True)

topDocs = searcher.search(query, 5)
scoreDocs = topDocs.scoreDocs

for i,var in enumerate(scoreDocs):
    doc_matching = searcher.doc(scoreDocs[i].doc)
    returned_string_matching = doc_matching.getField('pt').stringValue()
    print(returned_string_matching)
    
    
        
        
        
        
        