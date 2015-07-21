from twython import Twython
import json, io, time
from py2neo import neo4j, node, rel
import sys

oauth_token_secret = '0PNq6EWVWLuGDD7Zz1Y5aiMGc0eavJ6b2lKFaFUSLkqJy'
oauth_token = '41803203-daelXLCmfUn9NRxwawmDSnu1nQSDdXG9fpinUwm4y'
TWITTER_APP_KEY = 'E8ds3rRK7g7jQEacYaaginqBb'
TWITTER_APP_SECRET = 'QMNUSJlLpGFeePfRfXEIcxwskEdpLXVmzjAVMSF0BksNv6zO6o'
twitter = Twython(
			TWITTER_APP_KEY,
			TWITTER_APP_SECRET,
			oauth_token,
			oauth_token_secret
		)

print twitter.lookup_user(user_id="50144698")
sys.exit(0)

rels = {}
current_userid = oauth_token.split('-')[0];

m = i = 5
mid = m/2
usersToQuery = [current_userid]
users = []
while i > 0:

	userid = usersToQuery[m-i]

	print "Index ", str(i)
	print "Querying userId ", str(userid)

	followers = twitter.get_followers_ids(count=100, user_id=userid)['ids']
	
	t = time.time()
	for f in followers:
		if not f in rels:
			rels[f] = [userid]
		elif userid not in rels[f]:
			rels[f].append(userid)
	print time.time() - t
	users = users + twitter.lookup_user(user_id=",".join(map(str, followers)))

	friends = twitter.get_friends_ids(count=100, user_id=userid)['ids']
	
	t = time.time()
	for f in friends:
		if not userid in rels:
			rels[userid] = [f]
		elif f not in rels[userid]:
			rels[userid].append(f)
	print time.time() - t
	
	users = users + twitter.lookup_user(user_id=",".join(map(str, friends)))

	if i == m:
		usersToQuery = usersToQuery + followers[0:mid] + friends[0:mid]
	i = i-1

# fields = ['screen_name', 'name', 'location', 'created_at', 'id', 'favourites_count', 'url', 'lang', 'followers_count', 'friends_count', 'statuses_count']
# nullableFields = ['location', 'url']
# allUsers = []
# usersIndex = {}
# for u in users:
# 	if u['id'] in usersIndex:
# 		continue
# 	tu = {}
# 	for f in fields:
# 		tu[f] = u[f]
# 	allUsers.append(tu)
# 	usersIndex[u['id']] = 1

# print "writing.."
# # save
# with io.open('users.txt', 'w', encoding='utf-8') as f:
#   f.write(unicode(json.dumps(allUsers, ensure_ascii=False)))
# with io.open('rels.txt', 'w', encoding='utf-8') as f:
#   f.write(unicode(json.dumps(rels, ensure_ascii=False)))

# graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
# batch = neo4j.WriteBatch(graph_db)
# batches = {}
# for u in allUsers:
# 	batches[str(u['id'])] = batch.create(node(**u))
# for r in rels:
# 	for p in rels[r]:
# 		if str(r) in batches and str(p) in batches:
# 			batch.create(rel(batches[str(r)], "FOLLOWS", batches[str(p)]))
# 		else:
# 			print "Skipping.."
# results = batch.submit()
