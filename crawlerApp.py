from flask import Flask, jsonify, request
from crawlerByBS4 import crawler591
import json
import re

app = Flask(__name__)

#post /store data: {name :}
@app.route("/bs4StoreCity", methods=['POST'])
def saveHouses():
    request_data = request.get_json()
    citys = re.split(",", request_data['city'])
    crawler591(citys)
    # return jsonify("123")

if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run(host='127.0.0.1', port=5591, debug=True)
