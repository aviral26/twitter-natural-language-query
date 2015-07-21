class queryGenerator:
	
	clause = ''
	queryList = []
	maxNode = ''

	def start(self, tup, username):
		self.query = "MATCH "
		self.queryList = []
		self.clause = ''
		self.username = username
		for t in tup[1:]:
			getattr(self, t[0])(t, self.getNextNode())

		self.clause = self.clause.strip()
		if len(self.clause) > 0:
			self.clause = "WHERE " + self.clause

		return self.query + ",\n".join(self.queryList) + self.clause + " RETURN DISTINCT(a)"

	def friendsWithCond(self, tup, currentNode):
		if tup[1] and tup[1][0] and str(tup[1][0]).find('my') >= 0:
			self.myFriendsOrFollowers(tup[1:], currentNode)
			return 0

		nextNode = self.getNextNode()
		for t in tup[1:]:
			if t == 'friends':
				self.queryList.append(self.getAFollowsB(nextNode, currentNode))
			elif t == 'followers':
				self.queryList.append(self.getAFollowsB(currentNode, nextNode))
			elif isinstance(t, tuple) and str(t[0]).find('cond') >= 0:
				getattr(self, t[0])(t, currentNode)
			elif isinstance(t, tuple):
				getattr(self, t[0])(t, nextNode)

	def friendsWithoutCond(self, tup, currentNode):
		self.friendsWithCond(tup, currentNode)

	def followersWithCond(self, tup, currentNode):
		self.friendsWithCond(tup, currentNode)

	def followersWithoutCond(self, tup, currentNode):
		self.friendsWithCond(tup, currentNode)

	def myFriendsOrFollowers(self, tup, currentNode):
		for t in tup:
			if isinstance(t, tuple):
				getattr(self, t[0])(t, currentNode)

	def myFriends(self, tup, currentNode):
		self.queryList.append(self.getAFollowsB("node {screen_name:'" + self.username +"'}", currentNode))

	def myFollowers(self, tup, currentNode):
		self.queryList.append(self.getAFollowsB(currentNode, "node {screen_name:'" + self.username +"'}"))

	def cond(self, tup, currentNode):
		i = 1
		for t in tup[1:]:
			if isinstance(t, tuple):
				if isinstance(tup[i-1], tuple):
					self.clause += "AND "
				getattr(self, t[0])(t, currentNode)
			else:
					self.clause += str(t) + " "
			i = i + 1

	def specificCond(self, tup, currentNode):
		for t in tup[1:]:
			if isinstance(t, tuple):
				# print "specCondCalling " + t[0] + " with " + currentNode
				getattr(self, t[0])(t, currentNode)

	def placeCond(self, tup, currentNode):
		self.clause += currentNode + ".location=~'(?i).*" +  tup[1] +".*' "

	def followCond(self, tup, currentNode):
		self.clause = currentNode + ".followers_count "
		self.clause += tup[1]

	def whoFollow(self, tup, currentNode):
		#hack to remove 'and'
		if self.clause[-4:] == "and ":
			self.clause = self.clause[:-4]
		nextNode = self.getNextNode()
		self.queryList.append(self.getAFollowsB(currentNode, nextNode))
		for t in tup[1:]:
			if isinstance(t, tuple):
				getattr(self, t[0])(t, nextNode)

	def getAFollowsB(self, a, b):
		return "(" + a + ")-[:FOLLOWS]->(" + b + ") "

	def getNextNode(self):
		if self.maxNode == '':
			self.maxNode = chr(97)
		else:
			self.maxNode = chr(ord(self.maxNode)+1)
		return self.maxNode