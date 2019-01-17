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
    if newngram in ngrams:
        ngrams[newngram] += 1
    else:
        ngrams[newngram] = 1

def GetNGram(text,n):
    ngrams = {}
    for i in range(0,len(text) - (n - 1)):
        AddNgram(ngrams,text,i,n)   
    return ngrams

def sortSecond(val): 
    return val[1]  

def GetProfile(text,n,profileSize):
    profile = GetNGram(text,n)
    for key in profile:
        profile[key] /= len(text) - (n - 1)
    pr = sorted( profile.items(), key = sortSecond, reverse = True) 
    return dict(pr[:profileSize])

def FindFraqency(pair, profile):
    for ngram in profile:
        if (pair[0] == ngram[0]):
            return ngram[1]
    return 0

def ProfileDissimilarity1(profile1, profile2):
    suma = 0.0
    for key in profile1:
        f1 = profile1[key]
        f2 = 0.0
        if key in profile2:
            f2 = profile2[key]
        suma += (2 * (f1 - f2) / (f1 + f2)) * (2 * (f1 - f2) / (f1 + f2))
    for key in profile2:
        f1 = profile2[key]
        if key in profile1:
            continue
        else:
            suma += 4
    return suma

def ProfileDissimilarity2(profile1, profile2):
    suma = 1.0
    for key in profile1:
        f1 = profile1[key]
        f2 = 0.0
        if key in profile2:
            f2 = profile2[key]
        suma *= (2 * (f1 - f2) / (f1 + f2)) * (2 * (f1 - f2) / (f1 + f2))
    for key in profile2:
        f1 = profile2[key]
        if key in profile1:
            continue
        else:
            suma *= 4
    return suma

def ProfileDissimilarity3(profile1, profile2):
    suma = 0.0
    for key in profile1:
        if key in profile2:
            suma -= 1
    return suma

def ProfileDissimilarity4(profile1, profile2):
    suma = 0.0
    for key in profile1:
        f1 = profile1[key]
        f2 = 0.0
        if key in profile2:
            f2 = profile2[key]
        suma += (f1 - f2) * (f1 - f2) 
    for key in profile2:
        f1 = profile2[key]
        if key in profile1:
            continue
        else:
            suma += f1 * f1
    return suma

def ProfileDissimilarity5(profile1, profile2):
    suma = 0.0
    for key in profile1:
        f1 = profile1[key]
        f2 = 0.0
        if key in profile2:
            f2 = profile2[key]
        suma += abs(f1 - f2) 
    for key in profile2:
        f1 = profile2[key]
        if key in profile1:
            continue
        else:
            suma += f1
    return suma


def ChooseAuthor(profile,profiles,author,mode):
    minValue = 0
    minIndex = -1
    for i in range(0,len(profiles)):  
        pd = 0 
        if (mode == 1):
            pd = ProfileDissimilarity1(profile, profiles[i])
        if (mode == 2):
            pd = ProfileDissimilarity2(profile, profiles[i])
        if (mode == 3):
            pd = ProfileDissimilarity3(profile, profiles[i])
        if (mode == 4):
            pd = ProfileDissimilarity4(profile, profiles[i])
        if (mode == 5):
            pd = ProfileDissimilarity5(profile, profiles[i])
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
  
def Trial(profileSize,n,crossvalidation,authorNumber,textNumber,mode):
    # Wczytaj teksty
    training = []
    test = []
    
    for i in range(0,authorNumber):
        textSet = ""
        for j in range(0,textNumber):
            if (j == crossvalidation):
                test.append(LoadText(i + 1,j + 1))
            else:
                textSet += (LoadText(i + 1,j + 1))
        training.append(textSet)       
        
    # Wyznacz profile tekstów
    trainingProfiles = []
    for i in range(0,authorNumber):
        trainingProfiles.append(GetProfile(training[i],n,profileSize))
        
    testProfiles = []
    for i in range(0,authorNumber):
        testProfiles.append(GetProfile(test[i],n,profileSize))

    testSize = 0
    positiveSum = 0
    
    for i in range(0,9):
            testSize += 1
            positiveSum += ChooseAuthor(testProfiles[i],trainingProfiles,i,mode)
    return positiveSum / testSize
  
     
def Trials(profileSize,n,resultText,authorNumber,textNumber,mode):
    result = 0.0
    for i in range(0,authorNumber):
        result += Trial(profileSize,n,i,authorNumber,textNumber,mode)
    result /= authorNumber
    resultText += "Profile size: " + str(profileSize) + " \t N: " + str(n) + " \t Result: " + str(result) +"\n"
    return resultText

def Experiment(profileSizes,ns,authorNumber,textNumber,mode):
    resultText = ""
    for profileSize in profileSizes:
        for n in ns:
            resultText = Trials(profileSize,n,resultText,authorNumber,textNumber,mode)
    return resultText

#profileSizes = [20,50]
#ns = [1,2]

profileSizes = [20,50,100,200,500,1000,1500,2000,3000,4000,5000]
ns = [1,2,3,4,5,6,7,8,9,10]
authorNumber = 9
textNumber = 10

f=open("results1.txt", "a+")
f.write(Experiment(profileSizes,ns,authorNumber,textNumber,1)) 
f.close() 

f=open("results2.txt", "a+")
f.write(Experiment(profileSizes,ns,authorNumber,textNumber,2)) 
f.close() 

f=open("results3.txt", "a+")
f.write(Experiment(profileSizes,ns,authorNumber,textNumber,3)) 
f.close() 

f=open("results4.txt", "a+")
f.write(Experiment(profileSizes,ns,authorNumber,textNumber,4)) 
f.close() 

f=open("results5.txt", "a+")
f.write(Experiment(profileSizes,ns,authorNumber,textNumber,5)) 
f.close() 
