
from flask import Flask
from flask_restful import Api
from resources.people import People
from resources.photo import Photo, Photos
from config import config


app = Flask(__name__)
api = Api(app)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER


api.add_resource(People, '/people')
api.add_resource(Photos, '/photos')
api.add_resource(Photo, '/photo/<string:photo_id>')

if __name__ == '__main__':

    app.run(debug=True)
