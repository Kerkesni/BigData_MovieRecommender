from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances

import knnpip
import knnacos

app = Flask(__name__)
api = Api(app)

class PIP(Resource):

    def post(self):
        #importing Ratings
        Ratings = pd.read_csv("Ressources/ratings_copy.csv")

        parser = reqparse.RequestParser()
        parser.add_argument('taste', type = list, location='json')
        args = parser.parse_args()
        #Adding user taste to csv file
        userId = Ratings['userId'].tail(1).values[0]+1
        userTaste = args.get('taste')
        for taste in userTaste:
            row_content = pd.DataFrame([[userId, taste['movieId'], taste['rating'], taste['timestamp']]])
            row_content.to_csv('./Ressources/ratings_copy.csv', mode='a', header=False, index=False)

        recommended_movies = knnpip.recommand(userId)

        return recommended_movies

class ACOS(Resource):

    def post(self):
        #importing Ratings
        Ratings = pd.read_csv("Ressources/ratings.csv")

        parser = reqparse.RequestParser()
        parser.add_argument('taste', type = list, location='json')
        args = parser.parse_args()

        #Adding user taste to csv file
        userId = Ratings['userId'].tail(1).values[0]
        userTaste = args.get('taste')

        for taste in userTaste:
            row_content = pd.DataFrame([[userId, taste['movieId'], taste['rating'], taste['timestamp']]])
            row_content.to_csv('./Ressources/ratings.csv', mode='a', header=False, index=False)

        recommended_movies = knnacos.recommand(userId)

        return recommended_movies


api.add_resource(PIP, '/pip')
api.add_resource(ACOS, '/acos')

if __name__ == '__main__':
    app.run(debug=True)