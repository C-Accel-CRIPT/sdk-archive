from cript import *


a = Cond("temp", 25 * Unit("degC"), uncer=1 * Unit("degC"))
aa = Cond("temp", -99825 * Unit("degC"), uncer=1 * Unit("degC"))
b = Cond("time", 60 * Unit("min"))
bb = Cond("+ttime", 60 * Unit("min"))
c = Cond(key="solvent", value="water")
print(a)
print(b)
print(bb)
print(c)
