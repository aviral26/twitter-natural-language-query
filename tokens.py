import ply.lex as lex
import sys
# from preProcessor import preProcessor

# s = raw_input('String: ')
# p = preProcessor()
# print p.mapConditions(s)
# sys.exit(0)

reserved_words = {
	'friends': 'FRIENDS',
	'followers': 'FOLLOWERS',
	'and': 'AND',
	'or': 'OR',
	'of': 'OF',
	'who': 'WHO',
	'follow': 'FOLLOW',
	'endEntity': 'ENDENTITY',
	'my': 'MY'
}

tokens = [
			'LIVING_IN_PLACE',
			'HAVING_FOLLOWERS_GREATER_THAN_NUM',
			'HAVING_FOLLOWERS_LESS_THAN_NUM',
			'SPACE',
			'ID'
		] + list(reserved_words.values())

t_ignore_SPACE = r'\s'

# def t_FRIENDSOF(t):
# 	r'friends\sof'
# 	return t

# def t_MYFRIENDS(t):
# 	r'my\sfriends'
# 	return t

def t_LIVING_IN_PLACE(t):
	r'\b(living|live)\sin\s[a-zA-Z]+\b'
	t.value = t.value.split(' ')[2]
	return t

def t_HAVING_FOLLOWERS_GREATER_THAN_NUM(t):
	r'\b(having|have)\sfollowers\sgreater\sthan\s[0-9]+'
	num = int(t.value.split(' ')[4])
	t.value = " >= " + str(num)
	return t

def t_HAVING_FOLLOWERS_LESS_THAN_NUM(t):
 	r'\b(having|have)\sfollowers\sless\sthan\s[0-9]+'
	num = int(t.value.split(' ')[4])
	t.value = " < " + str(num)
	return t

def t_ID(t):
	r'[a-zA-Z]+'
	if t.value in reserved_words:
		t.type = reserved_words.get(t.value)
		return t
	else:
		pass

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

lexer = lex.lex()

data = '''my friends who follow friends living in delhidsg and having followers greater than 20'''
data = '''friends of my friends who live in delhi who live in mumbai'''
lexer.input(data)

# for tok in lexer:
# 	print tok
