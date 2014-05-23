from location import *

############################################
#          Test Locations                  #
############################################

l1 = Path((0,0),"TestLoc1", True)
l2 = Path((0,1),"TestLoc2", True)
l3 = Path((1,0),"TestLoc3", True)
l4 = Path((0,-1), "TestLoc4", True)
l5 = Path((-1,0), "TestLoc5", True)
t1 = Town((0,2),"Test town", True)

testlocs = {l1.point:l1, l2.point:l2, l3.point:l3, l4.point:l4, l5.point:l5,
	    t1.point:t1}


#############################################
#         Locations                         #
#############################################

loc1 = Path((0,0),"Loc1")
loc2 = Path((0,1),"Loc2")
loc3 = Path((1,0),"Loc3")
loc4 = Path((0,-1),"Loc4")
loc5 = Path((-1,0),"Loc5", False, "", 100)
town1= Town((0,2),"Town1")

locs = {loc1.point:loc1, loc2.point:loc2, loc3.point:loc3, loc4.point:loc4,
	loc5.point:loc5, town1.point:town1}
