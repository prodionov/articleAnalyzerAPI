from restAPI import app, api
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from restAPI.processing.influence_score import textProcessing

@app.route("/")
def home():
    print('init py is running')
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
    request_data = request.get_json()
    result = textProcessing(request_data)
    return jsonify(request_data)


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
