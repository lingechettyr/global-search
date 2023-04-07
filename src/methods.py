from py2neo import Graph, Node, Relationship, NodeMatch, NodeMatcher
import json
from collections import defaultdict

def create_nodes_bulk(df, graph):
    root_node = Node("global_search", id=-1)
    existing_node = graph.nodes.match("global_search", id=-1).first()
    if existing_node:
        root_node = existing_node
    else:
        graph.create(root_node)

    for index, row in df.iterrows():
        node_props = {
            "id": row["data_product_id"],
            "name": row["name"],
            "assetType": row['assetType'],
            "keys": row["keys"]
        }
        node = Node("global_search", **node_props)
        graph.create(node)
        rel = Relationship(root_node, "HAS", node)
        graph.create(rel)

def insert_node(object, graph):
    root_node = Node("global_search", id=-1)

    existing_root = graph.nodes.match("global_search", id=-1).first()
    if existing_root:
        root_node = existing_root
    else:
        graph.create(root_node)

    node_props = {
        "id": object['id'],
        'name': object['name'],
        'assetType': object['assetType'],
        'keys': str(object['keys'])
    }

    node = Node("global_search", **node_props)

    existing_node = graph.nodes.match("global_search", id=object['id'], assetType=object['assetType']).first()
    if existing_node:
        existing_node.update(node_props)
        graph.push(existing_node)
        return {"EXISTS": f"updated node with id {object['id']} and asset type {object['assetType']}"}
    else:
        graph.create(node)
        rel = Relationship(root_node, "HAS", node)
        graph.create(rel)
        return {"NEW NODE": f"inserted node with id {object['id']} and asset type {object['assetType']}"}

def delete_node(id, assetType, graph):
    node = graph.nodes.match("global_search", id=id, assetType=assetType).first()
    if node:
        graph.delete(node)
        return {"DELETE": f"Deleted node with id {id} and assetType {assetType}"}
    else:
        return {"ERR": f"No node with id {id} and assetType {assetType} found"}
    
def fuzzy_full_text_search(word, n, graph):
    query = """
        CALL db.index.fulltext.queryNodes("globalSearchNeo", $word, {limit:$n}) YIELD node, score
        RETURN node.id, node.name, node.assetType, node.keys, score
    """
    parameters = {"word": word + "~", "n": n}
    return graph.run(query, parameters=parameters).data()