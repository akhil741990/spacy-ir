'''
Created on 03-Mar-2020

@author: akhil
'''
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import spacy
from heapq import nlargest

def summarize(text):
    stopwords = list(STOP_WORDS)
    nlp = spacy.load("en_core_web_sm")
    testNlp = nlp(text)
    
    word_frequencies = {}
    for doc in testNlp:
        if doc.text not in stopwords:
            if doc.text not in word_frequencies.keys():
                word_frequencies[doc.text] = 1
            else:    
                word_frequencies[doc.text] += 1

    #print(word_frequencies)
    maximum_frequency = max(word_frequencies.values())
    #print(maximum_frequency)


    for word in word_frequencies.keys():
        word_frequencies[word] =  word_frequencies[word]/maximum_frequency
        
      
    #print(word_frequencies)  
        
        
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
                       
                       
                                      
        
    
    
    summarized_sentences = nlargest(7, sentence_sores, key=sentence_sores.get)
    
    #print(summarized_sentences)
    return summarized_sentences