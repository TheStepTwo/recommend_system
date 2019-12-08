import pandas as pd
import math
from sklearn.neighbors import NearestNeighbors

chunksize = 10000
final = pd.DataFrame()
for dfTemp in pd.read_csv('D:/step/ratings_drop.csv', chunksize=chunksize , usecols=[ 'userId' , 'productId' , 'rating'], 
                          dtype={ 'userId' : 'int32'  , 'productId' : 'int32' , 'rating' : 'int32'  } ):
    dfTemp.drop_duplicates(subset=['userId', 'productId'], keep='first' , inplace =True )
    dfTemp2 = dfTemp.pivot( index='userId' , columns='productId' , values="rating" ).fillna(0)
    final = final.add(dfTemp2, fill_value=0)
    del dfTemp2
    print("processing the " + str(dfTemp.shape[0]) + " rows." )
    
print(final.shape)
display(final)

print("output to the csv file...")
final.to_csv('D:/step/raiting_matrix.csv', encoding="utf_8_sig")
