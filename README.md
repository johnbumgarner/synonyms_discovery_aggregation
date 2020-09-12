# Natural Language Processing(NLP) and synonyms 

<p align="justify">
Finding a synonym for a specific word is easy for a human to do using a thesaurus. A thesaurus or synonym dictionary is a general reference for finding synonyms and sometimes the antonyms of a word. A computer application can be programmed to lookup synonyms using a variery of methods.  There are several issues with some of the methods, including selecting the wrong synonym based on context.  For example, one of the synonyms for "mother" is "mum."  The word "mum" can have mutiple meanings. As an adjective the word means to be quiet or slient. As a noun the word "mum" refer to someone's mother in British English or flowering perennial plants of the genus Chrysanthemum.  Computers also have issues when a corpus has related synonyms within the same text being analyzed.  
</p>

<p align="justify">
For instance, considering this text:

<i>"My mom always likes to receive mums on Mother's day."</i>

A human reading this text would instantly know that "mom" and "mother" are related and "mums" is referring to flowers, so its not related to the formers.  A computer would have some difficulty in determining the similarities or non-similarities between these words.  This problem is further compounded if someone is trying to measure the frequency of words within a their corpus.  

If you want to understand the complexity of this synonym relationship problem search for 'automatic synonym extraction' or 'automatic synonyms identification.' Producing a detail synonym list for each word in a corpus is hard and will often require a multiple prong approach, espcially if accuracy or precision is important.
</p>

<p align="justify">
The code within this repository will look at several common NLP modules used to determine synonyms for words (a.k.a tokens) within a corpus.  These methods included:
  
  * PyDictionary - https://pypi.org/project/PyDictionary
  * WordNet - 
</p>

## PyDictionary

<p align="justify">
  
PyDictionary is a module for Python 2.x and Python 3.x that queries synonym.com for the synonyms and antonyms of a word.  It does have some capabilities to translate words via Google Translations and obtain the definition of a word. 

    from PyDictionary import PyDictionary
dictionary = PyDictionary()
synonym = dictionary.synonym('mother')
print(synonym)
['mother-in-law', 'female parent', 'supermom', 'mum', 'parent', 'mom', 'momma', 'para I', 'mama', 'mummy', 'quadripara', 'mommy', 'quintipara', 'ma', 'puerpera', 'surrogate mother', 'mater', 'primipara', 'mammy', 'mamma']



</p>
