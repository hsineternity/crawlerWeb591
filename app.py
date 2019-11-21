from flask import Flask, jsonify, request
from elasticsearch import  Elasticsearch
import json

app = Flask(__name__)

es = Elasticsearch()

'''
format = {
    "query": {
        "bool": {
            "must": [
                { "match" : { "_index" : "taipei" }}...
            ],
            "must_not": [
                {"match": { "_index" : "taipei" }}...
                
            ],
            "should": [
                {"match": { "_index" : "taipei" }}...
            ]
        }
    }
}
'''

findBase = {
    "query": {
        "bool": {
        }
    }
}

#get
@app.route("/esay", methods=['GET'])
def getHouse():
    findBodys = json.loads(request.get_data().decode('utf8'))
    rt1= es.search(body=findBodys)
    return jsonify(rt1)

#get
@app.route("/houseDetail", methods=['GET'])
def getHouseData():
    findBodys = json.loads(request.get_data().decode('utf8'))
    
    for conditionK, conditionV in findBodys.items():
        matchV = []      
        if ( conditionV[0] ):
            for v in conditionV :
                matchV.append( { 'match' : v } )
        findBase['query']['bool'][conditionK] = matchV

    rt1= es.search(body=findBase)
    return jsonify(rt1)

if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.run(host='127.0.0.1', port=5000, debug=True)
