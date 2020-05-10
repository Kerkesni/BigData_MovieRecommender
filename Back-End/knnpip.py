import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances
import math

#importing the files
tags = pd.read_csv("Ressources/tags.csv",encoding="Latin1")


def Sim(ui, uj, final_movie):
    sum = 0
    for k in range(len(final_movie.columns)):
        µk = final_movie.iloc[:, k].values.mean()
        sum += PIP(ui.values[k],uj.values[k], µk)
    return sum

def PIP(r1, r2, uk):
    return Proximity(r1, r2) * Impact(r1, r2) * Popularity(r1, r2, uk)

def Agreement(r1, r2):
    Rmed = 3.5
    if(r1 > Rmed and r2 < Rmed or r2 > Rmed and r1 < Rmed):
        return False
    else:
        return True

def Proximity(r1, r2):
    Dr1r2 = 0
    if(Agreement(r1, r2)):
        Dr1r2 = abs(r1-r2)
    else:
        Dr1r2 = 2*abs(r1-r2)
    return math.pow((2*(5-0)+1)-Dr1r2, 2)

def Impact(r1, r2):
    Rmed = 3.5
    if(Agreement(r1, r2)):
        return ((abs(r1 - Rmed) + 1)*(abs(r2 - Rmed) + 1))
    else:
        return 1/((abs(r1 - Rmed) + 1)*(abs(r2 - Rmed) + 1))
#uk : average rating of movie k
def Popularity(r1, r2, uk):
    if(r1 > uk and r2 > uk or r1 < uk and r2 < uk):
        return 1 + math.pow((r1 + r2)/2 - uk, 2)
    else:
        return 1

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
        sum1 += Sim(ogUser, otherUser, final_movie)*(otherUser[ia]-otherUser.mean())
        sum2 += abs(Sim(ogUser, otherUser, final_movie))
    return Rua + sum1/sum2

def find_n_neighbours(df,n):
    df = df.apply(lambda x: pd.Series(x.sort_values(ascending=False)
        .iloc[:n].index, 
        index=['top{}'.format(i) for i in range(1, n+1)]), axis=1)
    return df

def getSimilarityTableForOne(user, final_movie):
    users_count = final_movie.shape[0]
    pip = []

    for second_user in range(users_count):
        value = Sim(final_movie.iloc[user-1], final_movie.iloc[second_user], final_movie)
        pip.append(value)

    df = pd.DataFrame(pip,index=final_movie.index)
    return df.T

def recommand(user):
    movies = pd.read_csv("Ressources/movies.csv",encoding="Latin1")
    Ratings = pd.read_csv("Ressources/ratings_copy.csv")
    Mean = Ratings.groupby(by="userId",as_index=False)['rating'].mean()
    Rating_avg = pd.merge(Ratings,Mean,on='userId')
    Rating_avg['adg_rating']=Rating_avg['rating_x']-Rating_avg['rating_y']

    check = pd.pivot_table(Rating_avg,values='rating_x',index='userId',columns='movieId')

    # Replacing NaN by Movie Average
    final_movie = check.fillna(check.mean(axis=0))


    df = getSimilarityTableForOne(user, final_movie)
    # top 10 neighbours for each user
    similar_users = find_n_neighbours(df, 10)

    average_rating = Rating_avg.astype({"movieId": str})
    Movie_user = average_rating.groupby(by = 'userId')['movieId'].apply(lambda x:','.join(x))

    movies_seen_by_user = check.columns[check[check.index==user].notna().any()].tolist()
    similar_users = similar_users.values.squeeze().tolist()[1:]
    Movie_seen_by_similar_users = ','.join(Movie_user[Movie_user.index.isin(similar_users)].values).split(',')
    Movies_under_consideration = list(set(Movie_seen_by_similar_users)-set(list(map(str, movies_seen_by_user))))
    Movies_under_consideration = list(map(int, Movies_under_consideration))

    # getting the genres watched by user
    movies.index = movies['movieId']
    user_genre = []
    for movie in movies_seen_by_user:
        movie_genre = movies['genres'].loc[movie].split('|')
        user_genre = list(set(user_genre) | set(movie_genre)) 

    # giving a score to each movie based on its genres
    movie_genre_scores = []
    for movie in Movies_under_consideration:
        movie_genre = movies['genres'].loc[int(movie)].split('|')
        intersection = [value for value in movie_genre if value in user_genre]
        movie_genre_scores.append((len(intersection), movie))

    movie_genre_scores.sort(key=lambda tup: tup[0], reverse=True)

    Movies_under_consideration = [int(movie[1]) for movie in movie_genre_scores][:5]

    score = []
    for item in Movies_under_consideration:
        score.append(predict(user, item, final_movie))

    movies = movies.reset_index(drop=True)
    data = pd.DataFrame({'movieId':Movies_under_consideration,'score':score})
    top_recommendation = data.sort_values(by='score',ascending=False).head(20)
    Movie_Name = top_recommendation.merge(movies, how='inner', on='movieId')
    Movie_Names = Movie_Name.title.values.tolist()
    return Movie_Names
