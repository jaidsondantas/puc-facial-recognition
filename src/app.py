
from flask import Flask
from flask_restful import Api
from resources.people import People

app = Flask(__name__)
api = Api(app)

api.add_resource(People, '/people')

if __name__ == '__main__':
  app.run(debug=True)
