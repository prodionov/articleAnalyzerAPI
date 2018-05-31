from flask import Flask, jsonify, request

app = Flask(__name__)

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

@app.route("/dictionaries")
def get_dictionaries():
    return jsonify({"positive" : positive_dict, "negative": negative_dict})

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

@app.route("/influence", methods=["POST"])
def calculate_influence():
    request_data = request.get_json()
    print('request_data', request_data)
    return jsonify(length=len(request_data["text"]))
