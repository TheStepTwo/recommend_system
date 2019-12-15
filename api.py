# ---API list---
# top_n
# search
# recommend_item_cf
# recommend_user_cf

import flask
from flask import render_template, jsonify, request, make_response
from flask_cors import CORS
import pandas as pd
import numpy as np
import re
import jieba as jb
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
import json
import time

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app, supports_credentials=True)

def readCSV():
    products = pd.read_csv('./products_join_categories.csv')
    products = products.loc[:, ~products.columns.str.contains('^Unnamed')]
    products.set_index( ['productId'] , inplace=True, drop=True )
    products = products.rename({'name': 'product_name'}, axis='columns')
    categories = pd.read_csv( './categories.csv')
    rating = pd.read_csv('./ratings_drop.csv' , usecols=[ 'userId' , 'productId' , 'rating'])
    return products, categories , rating

def readCSVWord():
    product_lists = pd.read_csv( './product_lists_with_cut.csv').fillna('')
    top_20_words1 = pd.read_csv( './top_20_word1.csv', names = ['cut_name' , 'count'])
    top_20_words2 = pd.read_csv( './top_20_word2.csv', names = ['cut_name' , 'count'])
    top_20_words3 = pd.read_csv( './top_20_word3.csv', names = ['cut_name' , 'count'])
    return product_lists, top_20_words1, top_20_words2, top_20_words3

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
    for idx in idxs:
        row = product_lists[product_lists.index==idx]
        productId = row.productId.values[0]
        name = row.name.values[0]
        
        res.append({
            'productId' : str(productId),
            'product_name' : name,
            'cat1' : str(products.iloc[idx].cat1),
            'cat2' : str(products.iloc[idx].cat2),
            'cat3' : str(products.iloc[idx].cat3),
            'cat1_name' : products.iloc[idx].cat1_name,
            'cat2_name' : products.iloc[idx].cat2_name,
            'cat3_name' : products.iloc[idx].cat2_name,
            'cos' : str(arr[idx])
        })
    return res

def filterRatingArray():
    global rating
    useRatingCount = rating['userId'].value_counts()
    ratingFiltered = rating[rating['userId'].isin(useRatingCount[useRatingCount >= 50 ].index)]
    productRatingCount = rating['productId'].value_counts()
    ratingFiltered = ratingFiltered[ratingFiltered['userId'].isin(productRatingCount[productRatingCount >= 100 ].index)]
    rating = ratingFiltered
    del ratingFiltered
    del useRatingCount
    del productRatingCount
    return rating


def findByKItemByTopKUsers(ratingFilteredPivotByUser,userId,distances,indices,k):
    global products
    prediction=0
    similarities = 1-distances.flatten()
    sum_wt = np.sum(similarities)
    wtd_sum = 0 

    notRatedItems = np.setdiff1d(ratingFilteredPivotByUser.columns.to_numpy() , ratingFilteredPivotByUser[ (ratingFilteredPivotByUser.index == userId) ].iloc[0].nonzero()[0] )
    simArray = np.array([similarities]).T * ratingFilteredPivotByUser.ix[indices.flatten()].filter(notRatedItems.tolist()).to_numpy()
    sortedIndex = (simArray.sum(axis=0)/sum_wt).argsort()[::-1][:10]
    result = []
    for index , productId in enumerate(sortedIndex.tolist()):
        
        result.append({
            'productId' : str(notRatedItems[productId]),
            'product_name' : products.iloc[notRatedItems[productId]].product_name,
            'cat1' : str(products.iloc[notRatedItems[productId]].cat1),
            'cat2' : str(products.iloc[notRatedItems[productId]].cat2),
            'cat3' : str(products.iloc[notRatedItems[productId]].cat3),
            'cat1_name' : products.iloc[notRatedItems[productId]].cat1_name,
            'cat2_name' : products.iloc[notRatedItems[productId]].cat2_name,
            'cat3_name' : products.iloc[notRatedItems[productId]].cat2_name,
        })
    return result
        
def findTopKByItemCf(ratingFilteredPivot,itemId, k):
    #user based:
    ratingFilteredMatrix = csr_matrix(ratingFilteredPivot.values)
    model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
    model_knn.fit(ratingFilteredMatrix)
    NearestNeighbors(algorithm='brute', leaf_size=30, metric='cosine', metric_params=None, n_jobs=1, n_neighbors=k, p=2, radius=1.0)

    #489000->productId
    queryIndex = ratingFilteredPivot.index.get_loc(itemId)
    # queryIndex = np.random.choice(ratingFilteredPivot.shape[0])
    distances, indices = model_knn.kneighbors(ratingFilteredPivot.iloc[queryIndex, :].values.reshape(1, -1), n_neighbors=k+1)
    return distances, indices

def findTopKByUserCf(ratingFilteredPivotByUser,userId):
    raitingFilteredMatrix = csr_matrix(ratingFilteredPivotByUser.values)
    model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
    model_knn.fit(raitingFilteredMatrix)
    NearestNeighbors(algorithm='brute', leaf_size=30, metric='cosine', metric_params=None, n_jobs=1, n_neighbors=5, p=2, radius=1.0)
    #119->userId
    #114416 , 3400 , 17750 ,83601 => 0.7
    # 127020.0 => 0.3
    # 127579.0 => 0.3
    queryIndex = ratingFilteredPivotByUser.index.get_loc(userId)
    distances, indices = model_knn.kneighbors(ratingFilteredPivotByUser.iloc[queryIndex, :].values.reshape(1, -1), n_neighbors=6)
    return distances, indices

start_time = time.time()
print("Starting....")
products, categories, rating = readCSV()
product_lists, top_20_words1, top_20_words2, top_20_words3 = readCSVWord()

tfidf  = TfidfVectorizer(analyzer='word', ngram_range=(1, 1), min_df=0).fit(product_lists['cut_name'])
tfidf_vec = tfidf.transform(product_lists['cut_name'])

rating = filterRatingArray()
rating.drop_duplicates(subset=['userId', 'productId'], keep='first' , inplace =True )
ratingFilteredPivot = rating.pivot( index='productId' , columns='userId' , values="rating" ).fillna(0)
ratingFilteredPivotByUser = rating.pivot( index='userId' , columns='productId' , values="rating" ).fillna(0)
print("--- %s seconds ---" % (time.time() - start_time))

def makeResponse(result_text):
    response = make_response(jsonify(data=result_text))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

# tf-idf
@app.route('/top_n', methods=['GET'])
def top_n_word():
    n = request.args.get('n') or "1"
    if int(n) > 3:
        n = "1"
    str_n = "top_20_words" + n
    exec("global %s" % str_n)
    words = globals()[str_n].to_dict('index')
    res = [(v) for k, v in words.items()]
    return(makeResponse(res))
    #return render_template("aaa.html")
    
@app.route('/search', methods=['GET'])
def search():
    query_str = request.args.get('query_str')
    res = recommendations(query_str)
    return(makeResponse(res))

# knn
@app.route('/recommend_item_cf', methods=['GET'])
def recommendByItemCf():
    global ratingFilteredPivot
    global products
    itemId = int(request.args.get('itemid'))
    k = int(request.args.get('k') or 10)
    #489000
    distances, indices = findTopKByItemCf(ratingFilteredPivot,itemId,k)
    topK = []
    for i in range(0, len(distances.flatten())):
        topK.append(products.iloc[ratingFilteredPivot.index[indices.flatten()[i]]].product_name)
    return makeResponse(topK)
    
@app.route('/recommend_user_cf', methods=['GET'])
def recommendByUserCf():
    global ratingFilteredPivotByUser
    global products
    userId = int(request.args.get('userid'))
    k = int(request.args.get('k') or 10)
    #7488
    distances, indices = findTopKByUserCf(ratingFilteredPivotByUser,userId)
    topK = findByKItemByTopKUsers(ratingFilteredPivotByUser,userId,distances,indices,k)
    return makeResponse(topK)

app.run(host='0.0.0.0', port=80)
