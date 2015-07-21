import ply.yacc as yacc

from tokens import tokens
from queryGenerator import queryGenerator
from preProcessor import preProcessor

def p_start(p):
	'''start : friendsWithCond
				| friendsWithoutCond
				| followersWithCond
				| followersWithoutCond'''

	p[0] = ('start',) + tuple(p[1:])

def p_friendsWithCond(p):
	'''friendsWithCond : FRIENDS OF friendsWithCond WHO cond ENDENTITY
						| FRIENDS OF friendsWithoutCond WHO cond ENDENTITY
						| FRIENDS OF followersWithCond WHO cond ENDENTITY
						| FRIENDS OF followersWithoutCond WHO cond ENDENTITY
						| myFriends WHO cond ENDENTITY'''
	p[0] = ('friendsWithCond',) + tuple(p[1:-1])

def p_friendsWithoutCond(p): 
	'''friendsWithoutCond : FRIENDS OF friendsWithoutCond ENDENTITY
							| FRIENDS OF followersWithoutCond ENDENTITY
							| myFriends ENDENTITY'''
	p[0] = ('friendsWithoutCond' ,) + tuple(p[1:-1])

def p_followersWithCond(p):
	'''followersWithCond : FOLLOWERS OF followersWithCond WHO cond ENDENTITY
						| FOLLOWERS OF followersWithoutCond WHO cond ENDENTITY
						| FOLLOWERS OF friendsWithCond WHO cond ENDENTITY
						| FOLLOWERS OF friendsWithoutCond WHO cond ENDENTITY
						| myFollowers WHO cond ENDENTITY'''
	p[0] = ('followersWithCond',) + tuple(p[1:-1])

def p_followersWithoutCond(p): 
	'''followersWithoutCond : FOLLOWERS OF followersWithoutCond ENDENTITY
							| FOLLOWERS OF friendsWithoutCond ENDENTITY
							| myFollowers ENDENTITY'''
	p[0] = ('followersWithoutCond' ,) + tuple(p[1:-1])

def p_cond(p):
	'''cond : specificCond AND cond			
			| specificCond	'''
	p[0] = ('cond',) + tuple(p[1:])


def p_specificCond(p):
	'''specificCond : placeCond
					| followCond
					| whoFollow'''

	p[0] = ('specificCond',) + tuple(p[1:])

def p_placeCond(p):
	'''placeCond : LIVING_IN_PLACE'''
	p[0] = ('placeCond',) + tuple(p[1:])

def p_followCond(p):
	'''followCond : HAVING_FOLLOWERS_GREATER_THAN_NUM
				  | HAVING_FOLLOWERS_LESS_THAN_NUM'''

	p[0] = ('followCond',) + tuple(p[1:])

def p_whoFollow(p):
    '''whoFollow : FOLLOW followersWithoutCond
    				| FOLLOW friendsWithoutCond'''
    p[0] = ('whoFollow',) + tuple(p[1:])

def p_myFriends(p):
	'''myFriends : MY FRIENDS'''
	p[0] = ('myFriends',) + tuple(p[1:])

def p_myFollowers(p):
	'''myFollowers : MY FOLLOWERS'''
	p[0] = ('myFollowers',) + tuple(p[1:])

# Error rule for syntax errors
def p_error(p):
	raise Exception("Syntax error at '%s'" % repr(p)) #p.value)

def parseQuery(s, username):
	# return "hey it works"
	parser = yacc.yacc(debug=0)
	prep = preProcessor()
	s = prep.mapConditions(s)
	result = parser.parse(s)
	gen = queryGenerator()
	query = gen.start(result, username)
	return query

def getStr(tup):
	if tup[0]:
		s = str(tup[0]).upper() + "===> "
	else:
		s = ''
	l = []
	for t in tup[1:]:
		if isinstance(t, tuple):
			l.append(t)
			s += str(t[0]).upper()
		else:
			s += str(t)
		s+= " "
	print s
	for x in l:
		getStr(x)

