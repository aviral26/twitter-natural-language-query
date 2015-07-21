class queryGenerator:
	def start(self, tup):
		query = ""
		for t in tup[1:]:
			if isinstance(t, tuple):
				if (t[0] == "cond"):
					temp = "WHERE "
				else:
					temp = ""
				query += temp + getattr(self, t[0])(t)
		return query

	def friend(self, tup):
		return "MATCH (node {screen_name='ayushchd'})-[:FOLLOWS]->(f) "

	def follower(self, tup):
		return "MATCH (node {screen_name='ayushchd'})<-[:FOLLOWS]-(f) "

	def cond(self, tup):
		query = ""
		i = 1
		for t in tup[1:]:
			if isinstance(t, tuple):
				if isinstance(tup[i-1], tuple):
					query += "AND "
				query += getattr(self, t[0])(t)
			else:
				query += str(t) + " "
			i = i + 1
		return query

	def specificCond(self, tup):
		query = ""
		for t in tup[1:]:
			if isinstance(t, tuple):
				query += getattr(self, t[0])(t)
		return query

	def placeCond(self, tup):
		return "f.place='" +  tup[2] +"' "

	def followCond(self, tup):
		query = "f.followers "
		if tup[1].find('greater') > -1:
			query += "> "
		else:
			query += "<= "

		query += str(tup[2])
		return query
