'''
Created on 03-Mar-2020

@author: akhil
'''
from  summerizer.textSummarizer import summarize
from  reader.pdfReader import extract_text_from_pdf
from  reader.textReader import getText

text = extract_text_from_pdf('/home/akhil/devTools/spark-2.4.4-bin-hadoop2.7/housingData/resume.pdf')

tokens = ""

for page in text:
    tokens = tokens + ' ' + page


toks = ' '.join(tokens.split())

#print(toks)

summ = summarize(toks)

#print(summ)


text = getText('/home/akhil/devTools/spark-2.4.4-bin-hadoop2.7/housingData/jobPosting/jobPostig4.txt')
print("Input :" + text)

summ = summarize(text)
print(summ)
