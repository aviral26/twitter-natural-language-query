
from pyparsing import *;
count = 2;

query = ""

def setFriend(strg , lok , toks):
	global query
	temp = " MATCH (node)<-[follows]-() "
	query = temp + query
	#print toks

def setFollower(strg , lol , toks):
	global query
	temp = " MATCH (node)<-[follows]-() "
	query = temp + query

def setAnd(strg , lol , toks):
	global query
	global count
	temp = " AND "
	temp_count = 0;
	temp_i = 0
	pos = 0
	while(1):
		pos = query.find("WHERE" , temp_i , len(query))
		#print pos
		if pos != -1:
			temp_count = temp_count + 1	
			temp_i = pos+1

		if temp_count == count:
			count = count + 1
			break

	
	query = query[0:pos] + temp + query[pos:len(query)]

	#print query

def setOr(strg , lol , toks):
	global query
	global count
	temp = " OR "
	temp_count = 0;
	temp_i = 0
	pos = 0
	while(1):
		pos = query.find("WHERE" , temp_i , len(query))
		#print pos
		if pos != -1:
			temp_count = temp_count + 1	
			temp_i = pos+1

		if temp_count == count:
			count = count + 1
			break

	
	query = query[0:pos] + temp + query[pos:len(query)-1]
	#print temp

def setPlace(strg , lol , toks):
	global query
	temp = "WHERE place = "
	query = temp + query
	#print toks

def getPlace(strg , lol , toks):
	global query
	#print toks[0]
	temp = "'" + toks[0] + "'"
	query = temp + query

def setFollowLessThan(strg , lol , toks):
	global query
	temp = " WHERE followers < "
	query = temp + query

def setFollowGreaterThan(strg , lol , toks):
	global query
	temp = "WHERE followers > "
	query = temp + query

def getFollowCount(strg , lol , toks):
	global query
	temp = "'" + toks[0] + "'";
	query = temp + query
	#print int(toks[0])



#Define grammer
cond = Forward()

followCount = (Word(nums)).setParseAction(getFollowCount)

followCond = ("having followers greater than" + followCount).setParseAction(setFollowGreaterThan) ^ ("having followers less than" + followCount).setParseAction(setFollowLessThan)

place = (Word(alphas + "-")).setParseAction(getPlace)

placeCond = ("living in" + place).setParseAction(setPlace)

specificCond = placeCond ^ followCond

cond << ((specificCond + "and" + cond ^ specificCond + cond).setParseAction(setAnd) ^ (specificCond + "or" + cond).setParseAction(setOr) ^ specificCond)

friend = ("Friends" + cond ^ "My Friends" + cond).setParseAction(setFriend)

follower = (("Followers" + cond) ^ ("My Followers" + cond)).setParseAction(setFollower)

start = friend ^ follower

#Grammer end

test = raw_input("Enter a string to be parsed: ")
result = start.parseString(test)
print query
a = input("");
