'''
Created on 21-Feb-2020

@author: akhil
'''


from pyresparser import ResumeParser
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
def extract_text_from_pdf(pdf_path):
    '''
    Helper function to extract the plain text from .pdf files

    :param pdf_path: path to PDF file to be extracted (remote or local)
    :return: iterator of string of extracted text
    '''
    # https://www.blog.pythonlibrary.org/2018/05/03/exporting-data-from-pdfs-with-python/
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


data = ResumeParser('/home/akhil/devTools/spark-2.4.4-bin-hadoop2.7/housingData/resume.pdf').get_extracted_data()


text = extract_text_from_pdf('/home/akhil/devTools/spark-2.4.4-bin-hadoop2.7/housingData/resume.pdf')

tokens = ""

for page in text:
    tokens = tokens + ' ' + page


toks = ' '.join(tokens.split())
nlp = spacy.load("en_core_web_sm")
testNlp = nlp(toks)


for tok in testNlp:
    print(f'Token : {tok}, POS :{tok.pos_}')





nouns = ""
for n in testNlp.noun_chunks:
    print(f'Noun : {n.text.lower().strip()}')
    nouns = nouns + ' ' + n.text.lower().strip()

'''
print(list(testNlp.noun_chunks))



for ent in testNlp.ents:
    print(f'Entity : {ent}, Label : {ent.label_},  {spacy.explain(ent.label_)}')
    
    



for idx, sentence in enumerate(testNlp.sents):
    for noun in sentence.noun_chunks:
        print(f'sentence: {sentence}  ---> has noun chunc {noun}')

'''