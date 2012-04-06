import sys
assert len(sys.argv) > 1, "Pass directory name as a parameter"
dir = sys.argv[1]
s = open(dir+"/success.log").readlines()
u=open(dir+"/update.log").readlines()

f1=open(dir+"/upload.log","a+")
for uid in s:
    uid = str(int(uid.strip()))
    f1.write(uid+chr(10))
for x in u:
    uid, url = x.split(":::")
    uid = str(int(uid))
    f1.write(uid+chr(10))

f1.flush()
