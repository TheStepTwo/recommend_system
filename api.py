import flask
from flask import render_template
import pandas as pd
import re
import jieba as jb
from sklearn.feature_extraction.text import CountVectorizer
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
	global common_words
	return(json.dumps(common_words))
    #return render_template("aaa.html")

def read_csv():
	products = pd.read_csv('./products_join_categories.csv')
	categories = pd.read_csv( './categories.csv')
	return products, categories

def processText(text, join_str = " ", array = False):
    text = str(text)
    if text.strip()=='':
        return ''
    r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+'
    text = re.sub(r, '', text)
    # cut word, GitBub: https://github.com/fxsjy/jieba
    text = join_str.join([w for w in list(jb.cut(text)) if w !=' '])
    return text

def get_top_n_words(corpus, n=None, ngram = 1):
    vec = CountVectorizer(ngram_range=(ngram, ngram)).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq, words_freq[:n]

print("Starting....")
products, categories = read_csv()
product_lists = products[['productId','name']]
product_lists['cut_name'] = product_lists['name'].apply(processText)
words_freq, common_words = get_top_n_words(product_lists['cut_name'], 20)
df1 = pd.DataFrame(common_words, columns = ['cut_name' , 'count'])
#df1.groupby('cut_name').sum()['count'].sort_values()
app.run()



