'''
Created on 03-Mar-2020

@author: akhil
'''


def getText(file):
    with open(file, 'r') as file:
        data = file.read().replace('\n', ' ')
    return data