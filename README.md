# Natural Language Processing(NLP) and synonyms 

<p align="justify">
Finding a synonym for a specific word is easy for a human to do using a thesaurus. A thesaurus or synonym dictionary is a general reference for finding synonyms and sometimes the antonyms of a word. A computer application can be programmed to lookup synonyms using a variery of methods.  There are several issues with some of the methods, including selecting the wrong synonym based on context.  For example, one of the synonyms for "mother" is "mum."  The word "mum" can have mutiple meanings. As an adjective the word means to be quiet or slient. As a noun the word "mum" refer to someone's mother in British English or flowering perennial plants of the genus Chrysanthemum.  Computers also have issues when a corpus has related synonyms within the same text being analyzed.  
</p>

<p align="justify">
For instance. considering this text:

<i>"My mom always likes to receive mums on Mother's day."</i>

A human reading this text would instantly know that "mom" and "mother" are related and "mums" is referring to flowers.  A computer would have some difficulty in determining the similarities or non-similarities between these words in this sentence.  This problem is compounded if we're trying to measure the frequency of words with a given corpus
</p>




Producing a precise synonym lists for each potential word in your corpus is hard and will require a multiple prong approach. The code below using WordNet and PyDictionary to create a superset of synonyms. Like all the other answers, this combine methods also leads to some over counting of word frequencies. I've been trying to reduce this over-counting by combining key and value pairs within my final dictionary of synonyms. The latter problem is much harder than I anticipated and might require me to open my own question to solve. In the end, I think that based on your use case you need to determine, which approach works best and will likely need to combine several approaches.
