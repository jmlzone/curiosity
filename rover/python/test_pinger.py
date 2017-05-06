#!/usr/bin/python

import ranger

r1 = ranger.ranger(17,27)
r2 = ranger.ranger(19,26)

while True :
    m1 = r1.measure()
    m2 = r2.measure()
    print "Forward = %f, Aft = %f" % (m1, m2)
