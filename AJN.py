# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 15:48:13 2019

@author: kamron6
"""

def LoadText(author,article):  
    text = open("datasets\\" +  str(author) + "\\" + str(article) + ".txt", "r")
    lines = text.readlines()
    text = ""
    for line in lines:
        text += line
    return text

def AddNgram(ngrams,text,i,n):
    newngram = text[i:(i+n)]
    new = True
    for ngram in ngrams:
        if (ngram[0] == newngram):
            new = False
            ngram[1] += 1
            break
    if (new):
        ngrams.append([newngram,1])

def GetNGram(text,n):
    ngrams = []
    for i in range(0,len(text) - (n - 1)):
        AddNgram(ngrams,text,i,n)   
    return ngrams

def sortSecond(val): 
    return val[1]  

def GetProfile(text,n,profileSize):
    profile = GetNGram(text,n)
    for ngram in profile:
        ngram[1] /= len(text) - (n - 1)
    profile.sort(key = sortSecond, reverse = True) 
    return profile[:profileSize]

def FindFraqency(pair, profile):
    for ngram in profile:
        if (pair[0] == ngram[0]):
            return ngram[1]
    return 0

def ProfileDissimilarity(profile1, profile2):
    suma = 0.0
    for pair in profile1:
        f1 = FindFraqency(pair, profile1)
        f2 = FindFraqency(pair, profile2)
        suma += (2 * (f1 - f2) / (f1 + f2)) * (2 * (f1 - f2) / (f1 + f2))
    for pair in profile2:
        f1 = FindFraqency(pair, profile1)
        if (f1 == 0):
            f2 = FindFraqency(pair, profile2)
            suma += (2 * (f1 - f2) / (f1 + f2)) * (2 * (f1 - f2) / (f1 + f2))
    return suma

def ChooseAuthor(profile,profiles,author):
    minValue = 0
    minIndex = -1
    for i in range(0,len(profiles)):
       pd =  ProfileDissimilarity(profile, profiles[i])
       if (minIndex == -1 or pd < minValue):
           minValue = pd
           minIndex = i
    if (author == minIndex):
        return 1
    return 0


def ShowProfile(profile):
    print("Profile:")
    for pair in profile:
        print(pair[0] + "   " + str(pair[1]))
  
def Trial(profileSize,n,crossvalidation):
    # Wczytaj teksty
    training = []
    test = []
    
    for i in range(0,9):
        textSet = ""
        for j in range(0,10):
            if (j == crossvalidation):
                test.append(LoadText(i + 1,j + 1))
            else:
                textSet += (LoadText(i + 1,j + 1))
        training.append(textSet)       
        
    # Wyznacz profile tekstów
    trainingProfiles = []
    for i in range(0,9):
        trainingProfiles.append(GetProfile(training[i],n,profileSize))
        
    testProfiles = []
    for i in range(0,9):
        testProfiles.append(GetProfile(test[i],n,profileSize))

    """
    for profile in trainingProfiles:
        ShowProfile(profile)
    for profile in testProfiles:
        ShowProfile(profile)
    """ 
    testSize = 0
    positiveSum = 0
    
    for i in range(0,9):
            testSize += 1
            positiveSum += ChooseAuthor(testProfiles[i],trainingProfiles,i)
    return positiveSum / testSize
       
def Trials(profileSize,n):
    result = 0.0
    for i in range(0,9):
        result += Trial(profileSize,n,i)
    result /= 9.0
    resultText = "Profile size: " + str(profileSize) + " \t N: " + str(n) + " \t Result: " + str(result)
    print(resultText)
    f=open(str(profileSize) + "n" + str(n) + ".txt", "a+")
    f.write(resultText)
    f.close()  

def Experiment(profileSizes,ns):
    for profileSize in profileSizes:
        for n in ns:
            Trials(profileSize,n)

profileSizes = [20,50,100,200,500,1000,1500,2000,3000,4000,5000]
ns = [1,2]

#profileSizes = [20,50,100,200,500,1000,1500,2000,3000,4000,5000]
#ns = [1,2,3,4,5,6,7,8,9,10]
Experiment(profileSizes,ns)
    

"""
import numpy as np
import nltk
import glob
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from scipy.cluster.vq import whiten
sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
word_tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
 
# Load data
data_folder = r"[path to chapters]"
files = sorted(glob.glob(os.path.join(data_folder, "chapter*.txt")))
chapters = []
for fn in files:
    with open(fn) as f:
        chapters.append(f.read().replace('\n', ' '))
all_text = ' '.join(chapters)

# create feature vectors
num_chapters = len(chapters)
fvs_lexical = np.zeros((len(chapters), 3), np.float64)
fvs_punct = np.zeros((len(chapters), 3), np.float64)
for e, ch_text in enumerate(chapters):
    # note: the nltk.word_tokenize includes punctuation
    tokens = nltk.word_tokenize(ch_text.lower())
    words = word_tokenizer.tokenize(ch_text.lower())
    sentences = sentence_tokenizer.tokenize(ch_text)
    vocab = set(words)
    words_per_sentence = np.array([len(word_tokenizer.tokenize(s))
                                   for s in sentences])
 
    # average number of words per sentence
    fvs_lexical[e, 0] = words_per_sentence.mean()
    # sentence length variation
    fvs_lexical[e, 1] = words_per_sentence.std()
    # Lexical diversity
    fvs_lexical[e, 2] = len(vocab) / float(len(words))
 
    # Commas per sentence
    fvs_punct[e, 0] = tokens.count(',') / float(len(sentences))
    # Semicolons per sentence
    fvs_punct[e, 1] = tokens.count(';') / float(len(sentences))
    # Colons per sentence
    fvs_punct[e, 2] = tokens.count(':') / float(len(sentences))
 
# apply whitening to decorrelate the features
fvs_lexical = whiten(fvs_lexical)
fvs_punct = whiten(fvs_punct)

# get most common words in the whole book
NUM_TOP_WORDS = 10
all_tokens = nltk.word_tokenize(all_text)
fdist = nltk.FreqDist(all_tokens)
vocab = fdist.keys()[:NUM_TOP_WORDS]
 
# use sklearn to create the bag for words feature vector for each chapter
vectorizer = CountVectorizer(vocabulary=vocab, tokenizer=nltk.word_tokenize)
fvs_bow = vectorizer.fit_transform(chapters).toarray().astype(np.float64)
 
# normalise by dividing each row by its Euclidean norm
fvs_bow /= np.c_[np.apply_along_axis(np.linalg.norm, 1, fvs_bow)]

# get part of speech for each token in each chapter
def token_to_pos(ch):
    tokens = nltk.word_tokenize(ch)
    return [p[1] for p in nltk.pos_tag(tokens)]
chapters_pos = [token_to_pos(ch) for ch in chapters]
 
# count frequencies for common POS types
pos_list = ['NN', 'NNP', 'DT', 'IN', 'JJ', 'NNS']
fvs_syntax = np.array([[ch.count(pos) for pos in pos_list]
                       for ch in chapters_pos]).astype(np.float64)
 
# normalise by dividing each row by number of tokens in the chapter
fvs_syntax /= np.c_[np.array([len(ch) for ch in chapters_pos])]

def PredictAuthors(fvs):
    km = KMeans(n_clusters=2, init='k-means++', n_init=10, verbose=0)
    km.fit(fvs)
 
    return km
    
"""