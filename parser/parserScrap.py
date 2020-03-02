'''
Created on 28-Feb-2020

@author: akhil
'''

import io
import os
import re
import nltk
import pandas as pd
import docx2txt
from datetime import datetime
from dateutil import relativedelta
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFSyntaxError
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import spacy
from spacy.matcher import Matcher
def extract_text_from_pdf(pdf_path):
   
    '''
     https://www.blog.pythonlibrary.org/2018/05/03/exporting-data-from-pdfs-with-python/
    '''
    if not isinstance(pdf_path, io.BytesIO):
        # extract text from local pdf file
        with open(pdf_path, 'rb') as fh:
            try:
                for page in PDFPage.get_pages(
                        fh,
                        caching=True,
                        check_extractable=True
                ):
                    resource_manager = PDFResourceManager()
                    fake_file_handle = io.StringIO()
                    converter = TextConverter(
                        resource_manager,
                        fake_file_handle,
                        codec='utf-8',
                        laparams=LAParams()
                    )
                    page_interpreter = PDFPageInterpreter(
                        resource_manager,
                        converter
                    )
                    page_interpreter.process_page(page)

                    text = fake_file_handle.getvalue()
                    yield text

                    # close open handles
                    converter.close()
                    fake_file_handle.close()
            except PDFSyntaxError:
                return
    else:
        # extract text from remote pdf file
        try:
            for page in PDFPage.get_pages(
                    pdf_path,
                    caching=True,
                    check_extractable=True
            ):
                resource_manager = PDFResourceManager()
                fake_file_handle = io.StringIO()
                converter = TextConverter(
                    resource_manager,
                    fake_file_handle,
                    codec='utf-8',
                    laparams=LAParams()
                )
                page_interpreter = PDFPageInterpreter(
                    resource_manager,
                    converter
                )
                page_interpreter.process_page(page)

                text = fake_file_handle.getvalue()
                yield text

                # close open handles
                converter.close()
                fake_file_handle.close()
        except PDFSyntaxError:
            return


text = extract_text_from_pdf('/home/akhil/devTools/spark-2.4.4-bin-hadoop2.7/housingData/resume.pdf')

tokens = ""

for page in text:
    tokens = tokens + ' ' + page


toks = ' '.join(tokens.split())


#print("Resume Text Content:"+ toks)


nlp = spacy.load("en_core_web_sm")

testNlp = nlp(toks)


matcher = Matcher(nlp.vocab)



#Name Extraction

matcher.add('NAME', None, [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}])
matches = matcher(testNlp)

for _, start, end in matches:
    span = testNlp[start:end]
    if 'name' not in span.text.lower():
            print(span.text)

print("====")

people = [ee for ee in testNlp.ents if ee.label_ == 'PERSON']

print(people)


#Summarization

from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
stopwords = list(STOP_WORDS)


word_frequencies = {}
for doc in testNlp:
    if doc.text not in stopwords:
        if doc.text not in word_frequencies.keys():
            word_frequencies[doc.text] = 1
        else:    
            word_frequencies[doc.text] += 1

print(word_frequencies)
maximum_frequency = max(word_frequencies.values())
print(maximum_frequency)


for word in word_frequencies.keys():
    word_frequencies[word] =  word_frequencies[word]/maximum_frequency
    
  
print(word_frequencies)  
    
    
sentences = [sentence for sentence in testNlp.sents]

sentence_sores = {}
for sent in sentences:
    for wordNew in sent:
        if wordNew.text.lower() in word_frequencies.keys():
            if len(sent.text.split(' ')) < 30:
                if sent not in sentence_sores.keys():
                   sentence_sores[sent] = word_frequencies[wordNew.text.lower()]
                else:
                   sentence_sores[sent] += word_frequencies[wordNew.text.lower()]    
                   
                   
for sent in sentence_sores.keys():
    print(sent)
    print(sentence_sores[sent])                   
                                  
    
from heapq import nlargest

summarized_sentences = nlargest(7, sentence_sores, key=sentence_sores.get)

print(summarized_sentences)





