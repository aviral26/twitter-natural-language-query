import ply.lex as lex

tokens = ('MY_FRIENDS',
			'FRIENDS',
			'MY_FOLLOWERS',
			'FOLLOWERS',
			'AND',
			'OR',
			'LIVING_IN',
			'PLACE',
			'HAVING_FOLLOWER_GREATER_THAN',
			'HAVING_FOLLOWER_LESS_THAN',
			'NUMBER'
		)

t_FRIENDS = r'(friends|Friends)'
t_MY_FRIENDS = r'(My \s Friends \s|My \s friends \s|my \s friends \s|my \s Friends \s)'
t_FOLLOWERS = r'(Followers|followers)'
t_MY_FOLLOWERS = r'(My \s Followers \s|My \s followers \s|my \s followers \s|my \s Followers \s)'
t_AND = r'\s and \s'
t_OR = r'\s or \s'
t_PLACE = r'([a-zA-Z]+)'
t_LIVING_IN = r'(living \s in \s|Living \s in \s)'
t_HAVING_FOLLOWER_GREATER_THAN = r'having \s followers \s greater \s than \s'
t_HAVING_FOLLOWER_LESS_THAN = r'having \s followers \s less \s than \s'


def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

lexer = lex.lex()


data = '''my friends living in delhi and yoyo'''
lexer.input(data)

for tok in lexer:
	print tok
