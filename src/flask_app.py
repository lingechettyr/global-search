import flask 
from flask import request, jsonify
from py2neo import Graph
import json
import methods

app = flask.Flask(__name__)

graph = Graph('bolt://localhost:7687', auth=('neo4j', 'password'))

@app.route('/graph/globalSearch', methods=["GET"])
def global_search():
    word, n = request.args.get('word'), request.args.get('n', "")
    return methods.fuzzy_full_text_search(word, int(n), graph)

@app.route('/graph/globalSearch', methods=['POST'])
def insert_node():
    object = json.loads(request.data)
    return methods.insert_node(object, graph)

@app.route('/graph/globalSearch', methods=['DELETE'])
def delete_node():
    id, assetType = request.args.get('id'), request.args.get('assetType')
    return methods.delete_node(id, assetType, graph)

if __name__ == "__main__":
    app.run(port=8000, debug=True)