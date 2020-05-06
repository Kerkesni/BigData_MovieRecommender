import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances

 #importing the files
movies = pd.read_csv("Ressources/movies.csv",encoding="Latin1")
Ratings = pd.read_csv("Ressources/ratings.csv")
Tags = pd.read_csv("Ressources/tags.csv",encoding="Latin1")

Mean = Ratings.groupby(by="userId",as_index=False)['rating'].mean()
Rating_avg = pd.merge(Ratings,Mean,on='userId')
Rating_avg['adg_rating']=Rating_avg['rating_x']-Rating_avg['rating_y']

check = pd.pivot_table(Rating_avg,values='rating_x',index='userId',columns='movieId')
final = pd.pivot_table(Rating_avg,values='adg_rating',index='userId',columns='movieId')

# Replacing NaN by Movie Average
final_movie = final.fillna(final.mean(axis=0))

def find_n_neighbours(df,n):
    #order = np.argsort(df.values, axis=1)[:, :n]
    df = df.apply(lambda x: pd.Series(x.sort_values(ascending=False)
        .iloc[:n].index,
        index=['top{}'.format(i) for i in range(1, n+1)]), axis=1)
    return df

# Similarity Measure (COS)
def recommand(user):

    # user similarity on replacing NAN by item(movie) avg
    cosine = cosine_similarity(final_movie)
    np.fill_diagonal(cosine, 0 )
    similarity_with_movie = pd.DataFrame(cosine,index=final_movie.index)
    similarity_with_movie.columns=similarity_with_movie.index

    # top neighbours for each user
    similar_users = find_n_neighbours(similarity_with_movie,10)

    average_rating = Rating_avg.astype({"movieId": str})
    Movie_user = average_rating.groupby(by = 'userId')['movieId'].apply(lambda x:','.join(x))

    Movie_seen_by_user = check.columns[check[check.index==user].notna().any()].tolist()
    similar_users = similar_users[similar_users.index==user].values.squeeze().tolist()
    Movie_seen_by_similar_users = ','.join(Movie_user[Movie_user.index.isin(similar_users)].values).split(',')
    Movies_under_consideration = list(set(Movie_seen_by_similar_users)-set(list(map(str, Movie_seen_by_user))))
    Movies_under_consideration = list(map(int, Movies_under_consideration))
    score = []

    for item in Movies_under_consideration:
        c = final_movie.loc[:,item]
        d = c[c.index.isin(similar_users)]
        f = d[d.notnull()]
        avg_user = Mean.loc[Mean['userId'] == user,'rating'].values[0]
        index = f.index.values.squeeze().tolist()
        corr = similarity_with_movie.loc[user,index]
        fin = pd.concat([f, corr], axis=1)
        fin.columns = ['adg_score','correlation']
        fin['score']=fin.apply(lambda x:x['adg_score'] * x['correlation'],axis=1)
        nume = fin['score'].sum()
        deno = fin['correlation'].sum()
        final_score = avg_user + (nume/deno)
        score.append(final_score)
    data = pd.DataFrame({'movieId':Movies_under_consideration,'score':score})
    top_recommendation = data.sort_values(by='score',ascending=False).head(15)
    Movie_Name = top_recommendation.merge(movies, how='inner', on='movieId')
    Movie_Names = Movie_Name.title.values.tolist()
    return Movie_Names
