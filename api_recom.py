import flask
from flask import jsonify
from flask import render_template
import pandas as pd
import numpy as np
import re
import jieba as jb
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():import flask
from flask import jsonify
from flask import request
from flask import render_template
import pandas as pd
import numpy as np
import re
import jieba as jb
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
	global common_words
	return(json.dumps(common_words))
    #return render_template("aaa.html")

@app.route('/recommend_item_cf', methods=['GET'])
def recommendByItemCf():
	global ratingFilteredPivot
	global products
	itemId = int(request.args.get('itemid'))
	k = int(request.args.get('k'))
	#489000
	distances, indices = findTopKByItemCf(ratingFilteredPivot,itemId,k)
	topK = []
	for i in range(0, len(distances.flatten())):
		topK.append(products.iloc[ratingFilteredPivot.index[indices.flatten()[i]]].product_name)
	return jsonify(data=topK)
	
@app.route('/recommend_user_cf', methods=['GET'])
def recommendByUserCf():
	global ratingFilteredPivotByUser
	global products
	userId = int(request.args.get('userid'))
	k = int(request.args.get('k'))
	distances, indices = findTopKByUserCf(ratingFilteredPivotByUser,userId)
	topK = findByKItemByTopKUsers(ratingFilteredPivotByUser,userId,distances,indices,k)
	return jsonify(data=topK)
	
def read_csv():
	products = pd.read_csv('./products_join_categories.csv')
	products = products.loc[:, ~products.columns.str.contains('^Unnamed')]
	products.set_index( ['productId'] , inplace=True, drop=True )
	products = products.rename({'name': 'product_name'}, axis='columns')
	categories = pd.read_csv( './categories.csv')
	rating = pd.read_csv('./ratings_drop.csv' , usecols=[ 'userId' , 'productId' , 'rating'] )
	return products, categories , rating

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
	prediction = 0
	similarities = 1 - distances.flatten()
	sum_wt = np.sum(similarities)
	wtd_sum = 0 
	notRatedItems = np.setdiff1d(ratingFilteredPivotByUser.columns.to_numpy() , ratingFilteredPivotByUser[ (ratingFilteredPivotByUser.index == userId) ].iloc[0].nonzero()[0] )
	predictionOfNotRateItems = []	
	for item in notRatedItems.tolist():
		weightedRatingSum = 0
		for i in range(0, len(indices.flatten())):
			ratingUserToItem = ratingFilteredPivotByUser.loc[ratingFilteredPivotByUser.iloc[indices.flatten()[i]].name,item] * similarities[i]
			weightedRatingSum += ratingUserToItem
		predictionOfNotRateItems.append(int(round( weightedRatingSum/sum_wt)))
	predictionOfNotRateItems = np.array(predictionOfNotRateItems)
	sortedIndex = predictionOfNotRateItems.argsort()[::-1][:k]
	result = []
	for index , productId in enumerate(sortedIndex.tolist()):
		result.append({
			'productId' : products.iloc[productId].product_name
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

print("Starting....")
products, categories , rating = read_csv()
rating = filterRatingArray()
rating.drop_duplicates(subset=['userId', 'productId'], keep='first' , inplace =True )
ratingFilteredPivot = rating.pivot( index='productId' , columns='userId' , values="rating" ).fillna(0)
ratingFilteredPivotByUser = rating.pivot( index='userId' , columns='productId' , values="rating" ).fillna(0)

app.run()



