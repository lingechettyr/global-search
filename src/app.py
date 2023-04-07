from fastapi import FastAPI, Body
from py2neo import Graph
import methods

app = FastAPI()

graph = Graph('bolt://localhost:7687', auth=('neo4j', 'password'))

@app.get('/graph/globalSearch')
async def global_search(word: str, n: int):
    return methods.fuzzy_full_text_search(word, n, graph)

@app.post('/graph/globalSearch')
async def insert_node(object: dict = Body(...)):
    return methods.insert_node(object, graph)

@app.delete('/graph/globalSearch')
async def delete_node(id: str, assetType: str):
    return methods.delete_node(id, assetType, graph)