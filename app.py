from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
#app.config.from_object('config.BaseConfig')
app.config['SERVER_NAME'] = "localhost:5555"
api = Api(app)

negative_dict = [
    "abnormal",
    "abolish",
    "abort"
]

positive_dict = [
    "acclaim",
    "accolade",
    "accurate"
]

@app.route("/")
def home():
    return jsonify({"greeting":"hello world"})

class Dictionaries(Resource):
    def get(self):
        return {"positive" : positive_dict, "negative": negative_dict}


class Dictionary(Resource):
    def get(self, word):
        if word in positive_dict:
            return {"sentiment": "positive"}
        if word in negative_dict:
            return {"sentiment" : "negative"}
        return {"sentiment" : "neutral"}


api.add_resource(Dictionaries, '/dictionaries')
api.add_resource(Dictionary, '/dictionary/<string:word>')

@app.route("/influence", methods=['POST'])
def process_data():
    print('request', request)
    request_data = request.get_json()
    print('request_data what', request_data)
    return jsonify({"text" : "love"})


@app.route("/dictionary/positive/<string:word>")
def add_positive_word(word):
    if word in positive_dict:
        return jsonify(positive_dict=positive_dict)
    if word in negative_dict:
        negative_dict.remove(word)
    positive_dict.append(word)
    positive_dict.sort()
    return jsonify(positive_dict=positive_dict)

@app.route("/dictionary/negative/<string:word>")
def add_negative_word(word):
    if word in negative_dict:
        return jsonify(positive_dict=negative_dict)
    if word in positive_dict:
        positive_dict.remove(word)
    negative_dict.append(word)
    negative_dict.sort()
    return jsonify(positive_dict=positive_dict)



# @app.route("/influence", methods=["POST"])
# def calculate_influence():
#     request_data = request.get_json()
#     print('request_data', request_data)
#     return jsonify(length=len(request_data["text"]))
