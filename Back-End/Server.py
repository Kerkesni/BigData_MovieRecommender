from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances

import knnpip
import knncos

app = Flask(__name__)
api = Api(app)

class PIP(Resource):

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

        recommended_movies = knnpip.recommand(userId)

        return recommended_movies

class Cos(Resource):

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

        recommended_movies = knncos.recommand(userId)

        return recommended_movies


api.add_resource(PIP, '/pip')
api.add_resource(Cos, '/cos')

if __name__ == '__main__':
    app.run(debug=True)