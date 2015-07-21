from twython import Twython
import json, io
from py2neo import neo4j, node, rel

json_data = open('rels.txt')
rels = json.load(json_data)
json_data = open('users.txt')
allUsers = json.load(json_data)

graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
graph_db.clear()
batch = neo4j.WriteBatch(graph_db)
batches = {}
for u in allUsers:
	batches[str(u['id'])] = batch.create(node(**u))
for r in rels:
	for p in rels[r]:
		if str(r) in batches and str(p) in batches:
			batch.create(rel(batches[str(r)], "FOLLOWS", batches[str(p)]))
		else:
			print "Skipping.."
results = batch.submit()
