import re

class preProcessor:

	def mapConditions(self, inp):
		# print inp
		pos = [m.start() for m in re.finditer(r'\bwho\b', inp)]

		if pos:
			prefix = inp[:pos[0]]
		else:
			prefix = inp
		
		numberOfentities = prefix.count('friends') + prefix.count('followers')
		entitiesWithoutConditions = numberOfentities - len(pos)

		for i in range(entitiesWithoutConditions):
			prefix += " endEntity "

		for i in range(len(pos)):
			if i+1 >= len(pos):
				app = inp[pos[i]:]
			else:
				app = inp[pos[i]:pos[i+1]]
			if app.find('follow ') >= 0:
				app = app[0:3] + self.mapConditions(app[3:])
			prefix += app
			prefix += " endEntity "

		return re.sub(r'\s+', r' ', prefix)
