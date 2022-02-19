
from flask import Flask
from flask_restful import Api
from resources.people import People
from resources.photo import Photo


app = Flask(__name__)
api = Api(app)


api.add_resource(People, '/people')
api.add_resource(Photo, '/photos')

if __name__ == '__main__':

    app.run(debug=True)
