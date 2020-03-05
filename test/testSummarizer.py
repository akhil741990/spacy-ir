'''
Created on 03-Mar-2020

@author: akhil
'''
from  summerizer.textSummarizer import summarize
from  reader.pdfReader import extract_text_from_pdf
from  reader.textReader import getText
import csv
from os import listdir
from os.path import isfile, join
import spacy
'''
text = extract_text_from_pdf('/home/akhil/devTools/spark-2.4.4-bin-hadoop2.7/housingData/resume.pdf')

tokens = ""

for page in text:
    tokens = tokens + ' ' + page


toks = ' '.join(tokens.split())

#print(toks)

summ = summarize(toks)

#print(summ)
'''


jobPostingDir = '/home/akhil/devTools/spark-2.4.4-bin-hadoop2.7/housingData/jobPosting/'


files = [join(jobPostingDir,f) for f in listdir(jobPostingDir) if isfile(join(jobPostingDir,f))]

for file in files:
    print("fileName :" + file)
    text = getText(file)
    print("Input :" + text)    
    summ = summarize(text)
    strSumm = ' '.join(str(e) for e in summ)
    print(strSumm)    
    with open('/home/akhil/devTools/spark-2.4.4-bin-hadoop2.7/housingData/jobPostingProcessed/data.csv','a') as fd:
        newFileWriter = csv.writer(fd)
        newFileWriter.writerow([text ,strSumm])



'''
Extracting noun from job posting
'''
for file in files:
    text = getText(file)
    with open('/home/akhil/devTools/spark-2.4.4-bin-hadoop2.7/housingData/jobPostingProcessed/data_noun.csv','a') as fd:
        newFileWriter = csv.writer(fd)
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        for n in doc.noun_chunks:
            newFileWriter.writerow([file,n.text.lower().strip()])
            
'''
Maually mark the noun as skill and no_skill
'''
            
            

import pandas as pd;
data = pd.read_csv('/home/akhil/devTools/spark-2.4.4-bin-hadoop2.7/housingData/jobPostingProcessed/data_noun.csv')
data.drop_duplicates(subset="Noun", keep = False, inplace = True)
data['SKILL'] = data['manual_skill_marking'].apply(lambda x : 1 if x == 'SKILL' else 0)
data[['FileName','Noun','SKILL']].to_csv('out.csv', index = False)


