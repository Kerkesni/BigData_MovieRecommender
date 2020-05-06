import pandas as pd 
import numpy as np
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
warnings.filterwarnings('ignore')

df = pd.read_csv('./Ressources/ratings.csv')
movie_titles = pd.read_csv('./Ressources/movies.csv')
#movie_titles.head()
df = pd.merge(df, movie_titles, on='movieId')
#df.head()
#df.describe()

ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
ratings['number_of_ratings'] = df.groupby('title')['rating'].count()
#ratings.head()
#ratings['rating'].hist(bins=50)
#ratings['number_of_ratings'].hist(bins=60)
#sns.jointplot(x='rating', y='number_of_ratings', data=ratings)

movie_matrix = df.pivot_table(index='userId', columns='title', values='rating')
#movie_matrix.head()
#ratings.sort_values('number_of_ratings', ascending=False).head(10)

AFO_user_rating = movie_matrix['Air Force One (1997)']
similar_to_air_force_one=movie_matrix.corrwith(AFO_user_rating)
similar_to_air_force_one.head()

corr_AFO = pd.DataFrame(similar_to_air_force_one, columns=['correlation'])
corr_AFO.dropna(inplace=True)
#corr_AFO.head()

corr_AFO = corr_AFO.join(ratings['number_of_ratings'])
corr_AFO[corr_AFO['number_of_ratings'] > 100].sort_values(by='correlation', ascending=False)
corr_AFO.head(10)
