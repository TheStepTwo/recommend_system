import flask
from flask import render_template
from flask import jsonify
from flask import request
import pandas as pd
import numpy as np
import re
import jieba as jb
import json
from json_tricks import dump, dumps, load, loads, strip_comments
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def readCSV():
	products = pd.read_csv('./products_join_categories.csv')
	categories = pd.read_csv( './categories.csv')
	product_lists = pd.read_csv( './product_lists_with_cut.csv').fillna('')
	top_20_words = pd.read_csv( './top_20_word.csv', names = ['cut_name' , 'count'])
	return products, categories, product_lists, top_20_words

def processText(text, join_str = " ", array = False):
    text = str(text)
    if text.strip()=='':
        return ''
    r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+'
    text = re.sub(r, '', text)
    # cut word, GitBub: https://github.com/fxsjy/jieba
    text = join_str.join([w for w in list(jb.cut(text)) if w !=' '])
    return text

def recommendations(text,num = 20):
    res = []
    ss = [processText(text, ",")]
    ss_vec = tfidf.transform(ss)
    cos_sim = cosine_similarity(ss_vec, tfidf_vec)
    arr =cos_sim[0]
    
    idxs=list(np.argsort(-arr)[:num])
    i = 0
    for idx in idxs:
        row = product_lists[product_lists.index==idx]
        productId = row.productId.values[0]
        name = row.name.values[0]
		
        res.append({
            'productId' : str(productId),
            'product_name' : name
		})
    return res

start_time = time.time()
print("Starting....")
products, categories, product_lists, top_20_words = readCSV()
tfidf  = TfidfVectorizer(analyzer='word', ngram_range=(1, 1), min_df=0).fit(product_lists['cut_name'])
tfidf_vec = tfidf.transform(product_lists['cut_name'])
print("--- %s seconds ---" % (time.time() - start_time))

@app.route('/', methods=['GET'])
def home():
	global top_20_words
	words = top_20_words.to_dict('index')
	res = [(v) for k, v in words.items()]
	return(jsonify(data=res))
    #return render_template("aaa.html")

@app.route('/search', methods=['GET'])
def search():
	query_str = request.args.get('query_str')
	res = recommendations(query_str)
	return(jsonify(data=res))
	
app.run()



