__author__ = 'jquintanilla'

env = []
jon = open("Mac CSV.csv", 'r')

inta = jon.readlines()
for i in range(len(inta)):
    inta[i] = inta[i].rstrip()
for x in inta:
    env.append(x.split(",",1)[1])

print inta
print env
print len(env)

if 1 == 2 and 3 == 3:
    print "hi"
cool = jon.readline().rstrip()
print cool
fresh = cool.split(",", 1)
print fresh

