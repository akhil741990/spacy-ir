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


