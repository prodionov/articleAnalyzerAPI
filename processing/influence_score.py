import sys, math, os, json, copy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import sent_tokenize

def sigmoid(max):
    #sigmoid that calculates the influnce score
    c=1
    def calc(x):
        return((max/(1+math.exp(-x*c))-max/2)*2)
    return calc

def textProcessing(text):
    print('this function was called')
    working_copy = copy.copy(text)
    token_sentence = sent_tokenize(working_copy)
    words_sentences_pairs = {}
    stops=stopwords.words('english')
    tokenizer=RegexpTokenizer(r'\w+')

    for sentence in token_sentence:
        sentence_lower = sentence.lower()
        token = tokenizer.tokenize(sentence)
        words = [w for w in token if not w in stops and len(w) > 2]
        for word in words:
            if word in words_sentences_pairs.keys():
                words_sentences_pairs[word.lower()].append(sentence)
            else:
                words_sentences_pairs[word.lower()] = [sentence]

    text=text.lower()
    token=tokenizer.tokenize(text)
    words=[w for w in token if not w in stops and len(w)>2]
    words_set=list(set(words))
    words_freq=[]

    with open(os.path.dirname(os.path.realpath(__file__))+'/negative-words.txt','r') as f:
        negative = f.read().split('\n')
    with open(os.path.dirname(os.path.realpath(__file__))+'/positive-words.txt','r') as g:
        postive = g.read().split('\n')

    for i in range(len(words_set)):
        words_freq.append((words_set[i],words.count(words_set[i])))
    final = sorted(words_freq, key=lambda tup:tup[1], reverse = True)

    max_value=final[0][1]
    scoreFunc=sigmoid(max_value)
    result = []

    for i in range(len(final)):
        obj={}
        obj['word']=final[i][0]
        obj['freq']=final[i][1]
        if final[i][0] in postive:
            obj['sentiment']='positive'
            obj['color']='blue'
            obj['score']=scoreFunc(obj['freq'])
        elif final[i][0] in negative:
            obj['sentiment']='negative'
            obj['color']='red'
            obj['score']=scoreFunc(obj['freq'])

        else:
            obj['sentiment']='neutral'
            obj['color']='green'
            obj['score']=obj['freq']

        result.append(obj)
        result = sorted(result, key = lambda obj: obj['score'], reverse = True)

    for entry in result:
        if entry['word'] in words_sentences_pairs.keys():
            entry['sentences'] = words_sentences_pairs[entry['word']]
    result = { "type": "PYTHON_OUTPUT", "payload": {"result" : result[:15], "wordCount" : len(token)}}
    return result
