import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances
import math

 #importing the files
movies = pd.read_csv("Ressources/movies.csv",encoding="Latin1")

def find_n_neighbours(df,n):
    #order = np.argsort(df.values, axis=1)[:, :n]
    df = df.apply(lambda x: pd.Series(x.sort_values(ascending=False)
        .iloc[:n].index,
        index=['top{}'.format(i) for i in range(1, n+1)]), axis=1)
    return df

def sim(ui, uj, final_movie):
    top_sum = 0
    bot_sum1 = 0
    bot_sum2 = 0

    meanUi = ui.mean()
    meanUj = uj.mean()
    for h in range(len(final_movie.columns)):
        top_sum += (ui.values[h] - meanUi)*(uj.values[h] - meanUj)
        bot_sum1 += pow(ui.values[h] - meanUi, 2)
        bot_sum2 += pow(uj.values[h] - meanUj, 2)
    
    return top_sum/math.sqrt(bot_sum1)*math.sqrt(bot_sum2)

def predict(ua, ia, final_movie):
    users_count = final_movie.shape[0]
    ogUser = final_movie.loc[ua]
    Rua = ogUser.mean()
    sum1 = 0
    sum2 = 0
    for user in range(users_count):
        if user+1 == ua:
            continue
        otherUser = final_movie.iloc[user]
        sum1 += sim(ogUser, otherUser, final_movie)*(otherUser[ia]-otherUser.mean())
        sum2 += abs(sim(ogUser, otherUser, final_movie))
    return Rua + sum1/sum2

def getSimilarityTableForOne(user, final_movie):
    users_count = final_movie.shape[0]
    cor = []

    for second_user in range(users_count):
        value = sim(final_movie.iloc[user-1], final_movie.iloc[second_user], final_movie)
        cor.append(value)

    df = pd.DataFrame(cor,index=final_movie.index)
    return df.T

# Similarity Measure (ACOS)
def recommand(user):

    Ratings = pd.read_csv("Ressources/ratings_copy.csv")
    Mean = Ratings.groupby(by="userId",as_index=False)['rating'].mean()
    Rating_avg = pd.merge(Ratings,Mean,on='userId')
    Rating_avg['adg_rating']=Rating_avg['rating_x']-Rating_avg['rating_y']

    check = pd.pivot_table(Rating_avg,values='rating_x',index='userId',columns='movieId')

    # Replacing NaN by Movie Average
    final_movie = check.fillna(check.mean(axis=0))

    df = getSimilarityTableForOne(user, final_movie)
    # top neighbours for each user
    similar_users = find_n_neighbours(df,10)

    average_rating = Rating_avg.astype({"movieId": str})
    Movie_user = average_rating.groupby(by = 'userId')['movieId'].apply(lambda x:','.join(x))

    movies_seen_by_user = check.columns[check[check.index==user].notna().any()].tolist()
    similar_users = similar_users.values.squeeze().tolist()[1:][:4]
    Movie_seen_by_similar_users = ','.join(Movie_user[Movie_user.index.isin(similar_users)].values).split(',')
    Movies_under_consideration = list(set(Movie_seen_by_similar_users)-set(list(map(str, movies_seen_by_user))))
    Movies_under_consideration = list(map(int, Movies_under_consideration))[:15]
    
    score = []
    for item in Movies_under_consideration:
        score.append(predict(user, item, final_movie))
        
    data = pd.DataFrame({'movieId':Movies_under_consideration,'score':score})
    top_recommendation = data.sort_values(by='score',ascending=False).head(15)
    Movie_Name = top_recommendation.merge(movies, how='inner', on='movieId')
    Movie_Names = Movie_Name.title.values.tolist()
    return Movie_Names
