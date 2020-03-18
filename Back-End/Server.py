from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances

from source import GetRecommendations

app = Flask(__name__)
api = Api(app)

class RecommendationAPI(Resource):
    def post(self):
        #importing Ratings
        Ratings = pd.read_csv("Ressources/ratings.csv")

        parser = reqparse.RequestParser()
        parser.add_argument('taste', type = list, location='json')
        args = parser.parse_args()

        #Adding user taste to csv file
        userId = Ratings['userId'].tail(1).values[0]+1
        userTaste = args.get('taste')

        for taste in userTaste:
            row_content = pd.DataFrame([[userId, taste['movieId'], taste['rating'], taste['timestamp']]])
            row_content.to_csv('./Ressources/ratings.csv', mode='a', header=False, index=False)

        recommended_movies = GetRecommendations(userId)

        return recommended_movies

api.add_resource(RecommendationAPI, '/')

if __name__ == '__main__':
    app.run(debug=True)