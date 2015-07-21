from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.conf import settings
from twython import Twython
import json, io, os
from py2neo import neo4j, node, rel
from v2parser import parser
from django.views.decorators.csrf import ensure_csrf_cookie
from neo4jrestclient.client import GraphDatabase

def getNeo4jService():
	return GraphDatabase(settings.NEO4J_SERVER, username=settings.NEO4J_USERNAME, password=settings.NEO4J_PASSWORD)
	
def getPy2neoService():
	return neo4j.GraphDatabaseService(settings.NEO4J_CONN_STR)

def setCurrentUser(f):
	def retF(*args, **kw):
		fil = open(os.path.dirname(__file__) + '/current_user.txt', "r")
		c = fil.read()
		fil.close()
		args[0].session['current_user'] = c
		return f(*args, **kw)
	return retF

@ensure_csrf_cookie
@setCurrentUser
def home(request):
	return render(request, 'home.html')


@ensure_csrf_cookie
@setCurrentUser
def mainapp(request):
	print "Accessing as " + request.session['current_user']
	# if 'authorized' not in request.session:
		# return render(request, 'message.html', {'message': 'Invalid request', 'type': 'warning'})
	return render(request, 'myapp.html')

def processQuery(request):
	try:
		print request.POST['userQuery'].lower()
		cypherQuery = parser.parseQuery(request.POST['userQuery'].lower(), request.session['current_user'])
		print cypherQuery
		graph_db = getNeo4jService()
		
		li = []
		resp = ""
		l = graph_db.query(q=cypherQuery)
		
		for record in l:
			r = record[0]['data']
			resp += """<a class='profile center-block' target='_blank' href='https://twitter.com/""" + r['screen_name'] +"""'>
					<div class='img'>
					<img src='""" + r['profile_image_url'] + """' class='img-circle' />
					</div>
					<div class='profileData'>
					<div class='profileDataItem'>""" + r['name'] + """</div>
					<div class='profileDataItem text-info'>""" + r['screen_name'] + """</div>
					<div class='profileDataItem text-muted'>""" + str(r['friends_count']) + """ friends, """ + str(r['followers_count']) + """ followers</div>
					<div class='profileDataItem text-muted'>""" + r['location'] + """</div>
					</div>
					</a>"""
		
		if resp == "":
			resp = "<p class='bg-danger pad'>No matching nodes found</p>"
		else:
			resp = "<p class='bg-success pad'>" + str(len(l)) + " results found </p>" + resp
		return HttpResponse(resp)
	except Exception as e:
		print e
		return HttpResponse("<p class='bg-danger pad'>The query could not be processed</p>")

def oauth(request):
	twitter = Twython(settings.TWITTER_APP_KEY, settings.TWITTER_APP_SECRET)
	auth = twitter.get_authentication_tokens(callback_url=settings.BASE_URL + 'oauth_callback')
	request.session['oauth_token'] = auth['oauth_token']
	request.session['oauth_token_secret'] = auth['oauth_token_secret']
	return redirect(auth['auth_url'])

def oauth_callback(request):
	# request.session['oauth_token_secret'] = '0PNq6EWVWLuGDD7Zz1Y5aiMGc0eavJ6b2lKFaFUSLkqJy'
	# request.session['oauth_token'] = '41803203-daelXLCmfUn9NRxwawmDSnu1nQSDdXG9fpinUwm4y'
	
	if not 'oauth_token' in request.GET or not 'oauth_verifier' in request.GET:
		return render(request, 'message.html', {'message': 'Invalid request', 'type': 'warning'})
	elif request.GET['oauth_token'] != request.session['oauth_token']:
		return render(request, 'message.html', {'message': "Trying an attack?", 'type': 'danger'})
	else:
		oauth_verifier = request.GET['oauth_verifier']
		
		twitter = Twython(
			settings.TWITTER_APP_KEY,
			settings.TWITTER_APP_SECRET,
			request.session['oauth_token'],
			request.session['oauth_token_secret']
		)
		
		# convert request token to access token
		auth = twitter.get_authorized_tokens(oauth_verifier)
		request.session['oauth_token'] = auth['oauth_token']
		request.session['oauth_token_secret'] = auth['oauth_token_secret']
		# request.session['oauth_token_secret'] = '0PNq6EWVWLuGDD7Zz1Y5aiMGc0eavJ6b2lKFaFUSLkqJy'
		# request.session['oauth_token'] = '41803203-daelXLCmfUn9NRxwawmDSnu1nQSDdXG9fpinUwm4y'

		current_username = createDatabase(request);
		request.session['authorized'] = 1
		f = open(os.path.dirname(__file__) + '/current_user.txt', "w")
		f.write(current_username)
		f.close()
		return redirect(mainapp)

def createDatabase(request):
	twitter = Twython(
			settings.TWITTER_APP_KEY,
			settings.TWITTER_APP_SECRET,
			request.session['oauth_token'],
			request.session['oauth_token_secret']
		)

	rels = {}
	current_userid = request.session['oauth_token'].split('-')[0];

	m = i = 5
	mid = m/2
	usersToQuery = [current_userid]
	users = []
	current_userdeets = twitter.verify_credentials()
	users.append(current_userdeets)
	while i > 0:

		userid = usersToQuery[m-i]
		print "Index ", str(i)
		print "Querying userId ", str(userid)
		followers = twitter.get_followers_ids(count=100, user_id=userid)['ids']
		for f in followers:
			if not f in rels:
				rels[f] = [userid]
			elif userid not in rels[f]:
				rels[f].append(userid)

		if len(followers) > 0:
			users = users + twitter.lookup_user(user_id=",".join(map(str, followers)))

		friends = twitter.get_friends_ids(count=100, user_id=userid)['ids']
		for f in friends:
			if not userid in rels:
				rels[userid] = [f]
			elif f not in rels[userid]:
				rels[userid].append(f)

		if len(friends) > 0:
			users = users + twitter.lookup_user(user_id=",".join(map(str, friends)))

		if i == m:
			usersToQuery = usersToQuery + followers[0:mid] + friends[0:mid]
		
		i = i-1

	fields = ['screen_name', 'name', 'location', 'created_at', 'id', 'favourites_count', 'url', 'lang', 'followers_count', 'friends_count', 'statuses_count', 'profile_image_url']
	allUsers = []
	usersIndex = {}
	for u in users:
		if u['id'] in usersIndex:
			continue
		tu = {}
		for f in fields:
			tu[f] = u[f]
		allUsers.append(tu)
		usersIndex[u['id']] = 1

	# print "writing.."
	# save
	# with io.open(os.path.dirname(__file__) + '/users.txt', 'w', encoding='utf-8') as f:
	#   f.write(unicode(json.dumps(allUsers, ensure_ascii=False)))
	# with io.open(os.path.dirname(__file__) + '/rels.txt', 'w', encoding='utf-8') as f:
	#   f.write(unicode(json.dumps(rels, ensure_ascii=False)))

	print 'Writing to neo4j..'
	graph_db = getPy2neoService()
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
	print 'Writing done..'
	return current_userdeets['screen_name']