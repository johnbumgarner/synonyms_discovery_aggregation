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
  * WordNet - https://www.nltk.org/howto/wordnet.html
  * spacy - https://spacy.io/
  
</p>

## PyDictionary

<p align="justify">
  
PyDictionary is a module for Python 2.x and Python 3.x that queries synonym.com for the synonyms and antonyms of a word.  It does have some capabilities to translate words via Google Translations and obtain the definition of a word. 

    from PyDictionary import PyDictionary
    
    dictionary = PyDictionary()
    synonym = dictionary.synonym('mother')
    
    print(synonym)
    # output 
    ['mother-in-law', 'female parent', 'supermom', 'mum', 'parent', 'mom', 'momma', 'para I', 'mama', 'mummy', 
    'quadripara', 'mommy', 'quintipara', 'ma', 'puerpera', 'surrogate mother', 'mater', 'primipara', 'mammy', 'mamma']
    
Note the word "mum" is included in the synonyms for "mother". Whereas the synonyms for the word "mum" do not include the word "mother."

    synonym = dictionary.synonym('mum')
    
    print(synonym)
    # output 
    ['incommunicative', 'silent', 'uncommunicative']
</p>

## WordNet
<p align="justify">


    from nltk.corpus import wordnet as wn
    
    # synsets is used to obtain synonyms for a word
    for synonym in wn.synsets('mother'):
       print (synonym)
       # output 
       Synset('mother.n.01')
       Synset('mother.n.02')
       Synset('mother.n.03')
       Synset('mother.n.04')
       Synset('mother.n.05')
       Synset('mother.v.01')
       Synset('beget.v.01')
   
 The output above shows that WordNet found 5 nouns and 2 verbs in its database for the word "mother."  We can gather more precise data by querying the lemmas, 
 which is the canonical form for a set of words. 
    
    for synonym in wn.synsets('mother'):
       for item in synonym.lemmas():
          print(item)
          # output 
          Lemma('mother.n.01.mother')
          Lemma('mother.n.01.female_parent')
          Lemma('mother.n.02.mother')
          Lemma('mother.n.03.mother')
          Lemma('mother.n.04.mother')
          Lemma('mother.n.05.mother')
          Lemma('mother.v.01.mother')
          Lemma('mother.v.01.fuss')
          Lemma('mother.v.01.overprotect')
          Lemma('beget.v.01.beget')
          Lemma('beget.v.01.get')
          Lemma('beget.v.01.engender')
          Lemma('beget.v.01.father')
          Lemma('beget.v.01.mother')
          Lemma('beget.v.01.sire')
          Lemma('beget.v.01.generate')
          Lemma('beget.v.01.bring_forth')
        
The output in the example above shows the synonyms for the noun and verbs for the word "mother" withing WordNet.  This output can be further refined by querying for specific parts of speech.  The example below is querying for nouns. 

    for synonym in wn.synsets('mother', wn.NOUN):
       for item in synonym.lemmas():
          if 'mother' != item.name():
            print(item.name())
            # output 
            female_parent

 Note the only synonym for "mother" is "female_parent."  But for the word "mom" there are 8 synonyms and not one is "mother." 
 
    for synonym in wn.synsets('mom', wn.NOUN):
       for item in synonym.lemmas():
          if 'mom' != item.name():
            print(item.name())
            # output 
            ma
            mama
            mamma
            momma
            mommy
            mammy
            mum
            mummy
           
</p>

## Spacy

<p align="justify">
  
 
    import spacy
    
    # Used to download one of Spacy's core models.
    # English Models:
    # 1. en_core_web_lg
    # 2. en_core_web_md
    # 3. en_core_web_sm
    # spacy.cli.download("en_core_web_md")
    
    nlp = spacy.load("en_core_web_md")
    tokens = nlp("ma mama mommy mother mum mummy")

    for token1 in tokens:
       for token2 in tokens:
          if token1.text != token2.text:
            print(token1.text, token2.text, token1.similarity(token2))

  
</p>
