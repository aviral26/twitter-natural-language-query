
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = '\xe5L,\xe0\x1cu\xc2\xf2\xd6m\x15\x94\x1f\xea\xa8\xf6'
    
_lr_action_items = {'AND':([9,10,13,16,20,21,],[17,-12,-11,-13,-15,-14,]),'LIVING_IN':([2,3,4,5,6,7,9,10,13,16,17,19,20,21,],[8,-5,-4,-3,-6,8,8,-12,-11,-13,8,8,-15,-14,]),'NUMBER':([11,14,],[20,21,]),'OR':([9,10,13,16,20,21,],[19,-12,-11,-13,-15,-14,]),'HAVING_FOLLOWER_LESS_THAN':([2,3,4,5,6,7,9,10,13,16,17,19,20,21,],[11,-5,-4,-3,-6,11,11,-12,-11,-13,11,11,-15,-14,]),'FOLLOWERS':([0,],[3,]),'PLACE':([8,],[16,]),'MY_FRIENDS':([0,],[4,]),'HAVING_FOLLOWER_GREATER_THAN':([2,3,4,5,6,7,9,10,13,16,17,19,20,21,],[14,-5,-4,-3,-6,14,14,-12,-11,-13,14,14,-15,-14,]),'FRIENDS':([0,],[5,]),'MY_FOLLOWERS':([0,],[6,]),'$end':([1,9,10,12,13,15,16,18,20,21,22,23,],[0,-10,-12,-2,-11,-1,-13,-8,-15,-14,-7,-9,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'specificCond':([2,7,9,17,19,],[9,9,9,9,9,]),'start':([0,],[1,]),'follower':([0,],[2,]),'cond':([2,7,9,17,19,],[12,15,18,22,23,]),'placeCond':([2,7,9,17,19,],[13,13,13,13,13,]),'followCond':([2,7,9,17,19,],[10,10,10,10,10,]),'friend':([0,],[7,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> start","S'",1,None,None,None),
  ('start -> friend cond','start',2,'p_start','parser.py',11),
  ('start -> follower cond','start',2,'p_start','parser.py',12),
  ('friend -> FRIENDS','friend',1,'p_friend','parser.py',16),
  ('friend -> MY_FRIENDS','friend',1,'p_friend','parser.py',17),
  ('follower -> FOLLOWERS','follower',1,'p_follower','parser.py',21),
  ('follower -> MY_FOLLOWERS','follower',1,'p_follower','parser.py',22),
  ('cond -> specificCond AND cond','cond',3,'p_cond','parser.py',26),
  ('cond -> specificCond cond','cond',2,'p_cond','parser.py',27),
  ('cond -> specificCond OR cond','cond',3,'p_cond','parser.py',28),
  ('cond -> specificCond','cond',1,'p_cond','parser.py',29),
  ('specificCond -> placeCond','specificCond',1,'p_specificCond','parser.py',33),
  ('specificCond -> followCond','specificCond',1,'p_specificCond','parser.py',34),
  ('placeCond -> LIVING_IN PLACE','placeCond',2,'p_placeCond','parser.py',39),
  ('followCond -> HAVING_FOLLOWER_GREATER_THAN NUMBER','followCond',2,'p_followCond','parser.py',43),
  ('followCond -> HAVING_FOLLOWER_LESS_THAN NUMBER','followCond',2,'p_followCond','parser.py',44),
]
