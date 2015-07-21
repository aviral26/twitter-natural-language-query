
from pyparsing import *;

#deifne grammer 1
digits = "1234567890"
number = Word(digits)
phoneNumber = Optional("(" + number + ")") + number + "-" + number
phoneNumberList = OneOrMore(phoneNumber)

#define grammer 2
salutation     = Word( alphas ).setResultsName("salute")
comma          = Literal(",")
greetee        = Word( alphas ).setResultsName("grettee")
endPunctuation = Literal("!")

greeting = salutation + comma + greetee + endPunctuation

#define grammer 3
lowers = "abcdefghijklmnopqrstuvwxyz"
caps = lowers.upper()
element = Word(caps ,max = 1) + Word(lowers) ^ Word(caps)
elementRef = Group(element + Optional(Word(digits) , default = "1"))
formula = OneOrMore(elementRef)

#define grammer 4
numberList = OneOrMore(number)
# print numberList.parseString('173 38 8')

#define grammer 5

followCount = Word(digits)
followCond = "where follower count is" + followCount
place = Word(alphas , max = 8).setResultsName("place")
placeCond = ("living in" + place).setResultsName("livingIn")
specificCond = placeCond ^ followCond
cond = Forward()
cond << (specificCond + "and" + cond ^ specificCond + "or" + cond ^ specificCond ^ empty)
friend = "Friends" + cond ^ "My Friends" + cond
follower = "Followers" + cond ^ "My Followers" + cond
start = friend ^ follower

test = "Followers living in delhi and where follower count in 200"
result = start.parseString(test);
print result;
c = input("number?");