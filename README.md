
![Image of Yaktocat](https://github.com/johnbumgarner/synonyms_nlp/blob/master/graphic/discovery_picture.png)


# Natural Language Processing synonym discovery and aggregation

<p align="justify">
Finding a synonym for a specific word is easy for a human to do using a thesaurus. A thesaurus or synonym dictionary is a general reference for finding synonyms and sometimes the antonyms of a word. A computer application can be programmed to lookup synonyms using a variery of methods.  There are several issues with some of the methods, including selecting the wrong synonym based on context.  For example, one of the synonyms for "mother" is "mum."  The word "mum" can have mutiple meanings. As an adjective the word means to be quiet or slient. As a noun the word "mum" refer to someone's mother in British English or flowering perennial plants of the genus Chrysanthemum.  Computers also have issues when a corpus has related synonyms within the same text being analyzed.  
</p>

<p align="justify">
For instance, consider this text:

<i>"My mom always likes to receive mums on Mother's day."</i>

A human reading this text would instantly know that "mom" and "mother" are related and "mums" is referring to flowers, so its not related to the formers.  A computer would have some difficulty in determining the similarities or non-similarities between these words.  This problem is further compounded if someone is trying to measure the frequency of words within a their corpus.  

If you want to understand the complexity of this synonym relationship problem search for terms 'automatic synonym detection' or 'automatic synonym extraction' or 'automatic synonyms identification.' Producing a detail synonym list for each word in a corpus is hard and will often require a multiple prong approach, espcially if accuracy or precision is important.
</p>

<p align="justify">
The code within this repository will look at several common NLP modules used to determine synonyms for words (a.k.a tokens) within a corpus.  These methods included:
  
  * PyDictionary - https://pypi.org/project/PyDictionary
  * WordNet - https://www.nltk.org/howto/wordnet.html
  * spaCy - https://spacy.io/
  * Word2Vec - https://radimrehurek.com/gensim/index.html
  * fastText - https://fasttext.cc/
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
WordNet is a lexical database for the English language, which was originally created by Princeton University. The database is currently part of the NLTK corpus
This database can be used with the Natural Language Toolkit(NLTK) to find the meanings of words, synonyms, antonyms and other linguistica categories. 

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

## spaCy

<p align="justify">
spaCy is a library used for advanced Natural Language Processing.  This library is popular for processing and analyzing unstructured textual data at scale. One of the built-in capabilities of spaCy is object comparisons. spaCy will predict how similar 2 objects (words) are to each other. Predicting similarity is useful for flagging duplicate words or determine potential relationships between words.  

The code below will compute a semantic similarity estimate using spaCy's token.similarity.  The higher the scalar similarity score the more similar tokens are to each other. The tokens being used are from the sentence <i>"My mom always likes to receive mums on Mother's day."</i>.  The sentence text has been normalized to remove all punctuations and English stopwords(e.g., to, on). 

Any token associated with a score of 1.O (perfect match) or less than 0.50 have been filtered out of the final results. 

    import spacy
    
    # Used to download one of Spacy's core models.
    # English Models:
    # 1. en_core_web_lg
    # 2. en_core_web_md
    # 3. en_core_web_sm
    # spacy.cli.download("en_core_web_md")
    
    nlp = spacy.load("en_core_web_md")
    tokens = nlp('mom always likes receive mums mothers day')

    for token1 in tokens:
       for token2 in tokens:
         if token1.text != token2.text and token1.similarity(token2) > 0.50:
            print(token1.text, token2.text, token1.similarity(token2))
            # output
            mom mums 0.6756202
            mom mothers 0.62206906
            always day 0.505295
            mums mom 0.6756202
            mums mothers 0.7151191
            mothers mom 0.62206906
            mothers mums 0.7151191
            day always 0.505295

The output above correcty associated tokens, such as "mom," "mothers" and "mums," because they are synonyms of one another. But in the input sentence the word "mums" was referring to flowers, so the word's association with the "mom" and "mothers" is incorrect based on context.  For the sake of brevity, I did not included the code for the following similarities examples, because on the token section changed.  

     mother father 0.82982457
     father daddy 0.5511614
  
 Note that the tokens "mother" and "father" have a high similarity score, whereas the words "father" and "daddy," have a lesser similarity score.  In the example 
 below we can see that "father" and "dad" have a higher similarity score than "father" and "daddy," but a lesser score than "mother" and "father." 
 
     father dad 0.7914408
 
Overall spaCy's token.similarity function did ok with determining the potential relationships between two words. The spaCy library is a powerful Natural Language Processing application, so it's worth the effort to explore the documentation to discover all the library's capabilities. 
</p>

## Word2Vec

<p align="justify">
Word2vec is a technique for Natural Language Processing. The Word2vec algorithm uses a neural network model to learn word associations from a large corpus of text. Once trained, such a model can detect synonymous words or suggest additional words for a partial sentence.

<b>Please note:</b> Word2Vec needs <i>large</i>, varied text examples to create its "dense" embedding vectors per word. It is the competition between many contrasting examples during training which allows the word-vectors to move to positions that have interesting distances and spatial-relationships with each other. 
If your corpus only contains 50 words then Word2vec is unlikely an appropriate technology to find synonymous for words.

The code below is only for educational purposes, because the corpus being used is too small. 

    import gensim
    from gensim.models import Word2Vec

    # Since the data is contained within a list it must be wrapped into another list, so that it can be interpreted correctly.
    data = ['mom', 'always', 'likes', 'receive', 'mums', 'mother', 'day']
    
    # size is the dimensionality of the vector, which in this case is small.
    # corpuses consisting of tens-of-thousands of words might justify 100-dimensional word-vectors. 
    # 
    # window size of 2 creates vectors that scored best on the analogies-evaluation. 
    model1 = gensim.models.Word2Vec([data], min_count=1, size=2, window=2)

    print(f"The words 'mother' and 'mom' have a cosine similarity score of: {model1.wv.similarity('mother', 'mom')}")
    print(f"The words 'mother' and 'mums' have a cosine similarity score of: {model1.wv.similarity('mother', 'mums')}")
    print(f"The words 'mom' and 'mums' have a cosine similarity score of: {model1.wv.similarity('mom', 'mums')}")
    # output
    The words 'mother' and 'mom' have a cosine similarity score of: 0.8387100696563721
    The words 'mother' and 'mums' have a cosine similarity score of: -0.988419771194458
    The words 'mom' and 'mums' have a cosine similarity score of: -0.9116343259811401

Cosine similarity can range from -1 to 1 based on the angle between the two vectors being compared. A value of 1 is a perfect relationship between word vectors (e.g., "mother" compared with "mother"), whereas a value of 0 represents no relationship between words, and a value of -1 represents a perfect opposite relationship between words. A negative similarity means the two words (e.g., "mom" compared with "mums"  are related in component, but in an opposite (or negative) fashion.  

Based on the size of our corpus, Word2vec is an inappropriate technology to determine the similarities or non-similarities between words.
</p>

## fastText

<p align="justify">
fastText was created by Facebook AI Research (FAIR) lab and is a library for efficient learning of word representations and sentence classification. FastText combines some of the most successful concepts of Natural Language Processing and machine learning in a single module.  Some of the concepts include representing sentences with bag of words and bag of n-grams, as well as using subword information, and sharing information across classes through a hidden representation. 
  
    import fasttext.util
    
    # The following was used to download a pretrained model in the English language
    # https://fasttext.cc/docs/en/english-vectors.html
    # fasttext.util.download_model('en', if_exists='ignore')
    
    ft = fasttext.load_model('cc.en.300.bin')
    
    # "k" is the number of items to include in the output
    results = ft.get_nearest_neighbors('mom', k=10)
    for item in results:
       print(item)
       # output 
       (0.8316885828971863, 'father')
       (0.8139842748641968, 'grandmother')
       (0.8042423725128174, 'daughter')
       (0.7595430612564087, 'aunt')
       (0.7551708221435547, 'stepfather')
       (0.7433159947395325, 'mom')
       (0.7390366792678833, 'step-father')
       (0.7379246950149536, 'stepmother')
       (0.7268661856651306, 'step-mother')
       (0.7265076041221619, 'sister')
       (0.7254297137260437, 'son')
       (0.7242798805236816, 'mother-in-law')
       (0.7103716135025024, 'husband')
       (0.707595944404602, 'wife')
       (0.693300187587738, 'daughter-in-law')
       (0.6749315857887268, 'sister-in-law')
       (0.6736578345298767, 'mother.She')
       (0.6697360873222351, 'granddaughter')
       (0.6673513650894165, 'step-daughter')
       (0.6669045686721802, 'dad')
       (0.664728045463562, 'mother.It')
       (0.6594554781913757, 'daughters')
       (0.659233808517456, 'great-grandmother')
       (0.6584458947181702, 'birth-mother')
  
Interpreting these results is overly complex, especially for discovering synonyms within a corpus. fastText like Word2vec is an inappropriate technology to find synonyms for a specific word.  
<p>
  
## Dictionary approach

<p align="justify">
  
Using a plain old dictionary approach is possible depending on the size of the corpus and your use case for discovering and cross-referencing the synonyms within the corpus.

    import string

    word_relationship = {"father": ['dad', 'daddy', 'old man', 'pa', 'pappy', 'papa', 'pop'],
                         "mother": ["mamma", "momma", "mama", "mammy", "mummy", "mommy", "mom", "mum"]}
                          
    input_text = """My mom always likes to receive mums on Mother's day."""

    # converts the input text to lowercase and splits the words based on empty space.
    wordlist = input_text.lower().split()
    
    # list for word frequencies
    wordfreq = []

    # count the frequencies of a word
    for w in remove_punctuation:
       wordfreq.append(remove_punctuation.count(w))

    word_frequencies = (dict(zip(remove_punctuation, wordfreq)))

    word_matches = []

    for word, frequency in word_frequencies.items():
       for keyword, synonym in word_relationship.items():
          match = [x for x in synonym if word == x]
          if word == keyword or match:
            match = ' '.join(map(str, match)) is 
            word_matches.append([keyword, match, frequency])
  
    for item in word_matches:
      print(item)
      # output
      ['mother', 'mom', 1]
      ['mother', '', 1]

A dictionary approach is useful for a small corpus, but it is hard to scale when the corpus expands.  
<p>
  
## Web scraping approach

<p align="justify">

Another method to acquire synonyms is through web scraping (also known as, web data extraction or web harvesting).  This automative technique can be used to extract and aggregate synonyms from mutiple sources thus building a more comprehensive list for each word. Some of the primary online sources including Collins Dictionary and synonyms.com.  The latter is the source queried by PyDictionary. 

Here is an basic web scraping example for thesaurus.com: 

    import requests

    req = requests.get(f'https://tuna.thesaurus.com/pageData/mother')
    dict_synonyms = req.json()['data']['definitionData']['definitions'][0]['synonyms']
    synonyms = [r["term"] for r in dict_synonyms]
    print(sorted(synonyms))
    # output
    ['ancestor', 'child-bearer', 'creator', 'forebearer', 'mom', 'mommy', 'origin', 'parent', 'predecessor', 'procreator', 'progenitor', 'source']

The example above queries the API used by thesaurus.com, because the primary website employ dynamic content creation, which can severely impact automative data extraction.  Another countermeasure often used by websites are connection threshold limits.  These thresholds can be linked to the number of connections per second from a given host.  Once such a threshold is met a website can automatically drop the external host connections and in some cases block the IP address. Websites also continually modify their code, so web scrapers will require maintenance related to any code changes that impact scraping operations.
<p>
  
## Multi-pronged approach

<p align="justify">
 
One of the best approaches for discovering and aggregating synonyms is one that uses multiple methods. The Python script <i> synonym_finder.py </i> contained within this repository uses web scraping and WordNet from the Natural Language Toolkit(NLTK) to build a more comprehensive list of synonyms for specific word. The script queries 3 primary online repositories for synonyms. These repositories are collinsdictionary.com, synonym.com and thesaurus.com. Each of the queries is operational as of September 15, 2020. If any of these online repositories change their website code structure than the Python query function for the specific repository will need to be updated within the script.

The script contains comments on its usage, but if you have questions please reach out to me via email on GitHub.
<p>
  
## Notes:

_The code within this repository is **not** production ready. It was **strictly** designed for experimental testing purposes only._
