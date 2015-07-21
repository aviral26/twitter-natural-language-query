import ply.yacc as yacc

from tokens import tokens
from queryGenerator import queryGenerator

count = 0;
query = ""
node = ""

def p_start(p):
	'''start : F
		   | follower cond '''
	p[0] = ('start' ,) + tuple(p[1:])

def p_F(p): 
	'''F : friend cond
			 | friendsWithCond AND cond
			 | friend OF friend cond
			 				 '''
	p[0] = ('F' ,) + tuple(p[1:])

def p_friendsWithCond(p):
	'''friendsWithCond : friend WHO whoFollow '''
	p[0] = ('friendsWithCond' , p[1] , p[2] , p[3])

def p_friend(p):
	'''friend : FRIENDS 
			  | MY_FRIENDS'''
	p[0] = ('friend' , p[1])

def p_follower(p):
	'''follower : FOLLOWERS
			    | MY_FOLLOWERS'''
	p[0] = ('follower' , p[1])

def p_cond(p):
	'''cond : specificCond AND cond			
			| specificCond cond 
			| specificCond OR cond 
			| specificCond	'''
	p[0] = ('cond',) + tuple(p[1:])


def p_specificCond(p):
	'''specificCond : placeCond 
					| followCond
					| whoFollow'''

	p[0] = ('specificCond' , p[1])

def p_placeCond(p):
	'''placeCond : LIVING_IN'''
	p[0] = ('placeCond' , p[1] )

def p_followCond(p):
	'''followCond : HAVING_FOLLOWER_GREATER_THAN NUMBER 
				  | HAVING_FOLLOWER_LESS_THAN NUMBER'''

	p[0] = ('followCond' , p[1] , p[2])

def p_whoFollow(p):
        '''whoFollow : FOLLOW F 
			| FOLLOW friend'''
	p[0] = ('whoFollow' , p[1] , p[2])

# Error rule for syntax errors
def p_error(p):
	print("Syntax error at '%s'" % repr(p)) #p.value)

# Build the parser
parser = yacc.yacc()

s = raw_input('Enter string:')
result = parser.parse(s)
print result
#gen = queryGenerator()
#query = gen.start(result)
#print query
