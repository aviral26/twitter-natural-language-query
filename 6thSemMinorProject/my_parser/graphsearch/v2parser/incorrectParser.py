import ply.yacc as yacc
import sys
from tokens import tokens
from preProcessor import preProcessor

def p_start(p):
	'''start : FRIENDSOF friendsWithCond whoCond
				| FRIENDSOF friendsWithoutCond whoCond
				| friendsWithoutCond'''

	p[0] = ('start',) + tuple(p[1:])

def p_friendsWithCond(p):
	'''friendsWithCond : FRIENDSOF friendsWithCond whoCond
						| FRIENDSOF friendsWithoutCond whoCond
						| MYFRIENDS whoCond'''
	p[0] = ('friendsWithCond',) + tuple(p[1:])

def p_friendsWithoutCond(p): 
	'''friendsWithoutCond : FRIENDSOF friendsWithoutCond
							| MYFRIENDS'''
	p[0] = ('friendsWithoutCond' ,) + tuple(p[1:])

def p_whoCond(p):
	'''whoCond : WHO cond'''
	p[0] = ('whoCond', ) + tuple(p[1:])

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
    '''whoFollow : FOLLOW friendsWithCond
    				| FOLLOW friendsWithoutCond'''
    p[0] = ('whoFollow',) + tuple(p[1:])

def p_myFriends(p):
	'''myFriends : MYFRIENDS WHO cond'''
	p[0] = ('myFriends',) + tuple(p[1:])

# Error rule for syntax errors
def p_error(p):
	print("Syntax error at '%s'" % repr(p)) #p.value)

# Build the parser
parser = yacc.yacc()

s = "friends of my friends who live in india" #raw_input('Enter string:')
result = parser.parse(s, debug=1)
print result
#gen = queryGenerator()
#query = gen.start(result)
#print query
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

getStr(result)
