
import seawolf as sw
import sys
import time


vars = sys.argv[1:-1]
filename = sys.argv[-1]
t = time.strftime("%Y%m%d%H%M%S")
filename = "%s.%s" % (filename, t)

if not vars:
    print "Variable list required"
    sys.exit(1)

sw.loadConfig("../conf/seawolf.conf")
sw.init("Logger")

f = open(filename, "w")

for v in vars:
    sw.var.subscribe(v)

try:
    f.write("\t\t\t" + "\t".join(vars))
    f.write("\n")
    while True:
        sw.var.sync()
        f.write(time.strftime("%b %2d %H:%M:%S  \t"))
        f.write("\t".join(["%.3f" % (sw.var.get(v),) for v in vars]))
        f.write("\n")
        f.flush()
finally:
    f.close()
