import sys
assert len(sys.argv) > 1, "Pass directory name as a parameter"
dir = sys.argv[1]
urls = open(dir+"/urls")
uri=open(dir+"/url","w+")
pool={}
print "Mapping Domains"
while True:
                domain = urls.readline().split("\t")[0]
		if(len(domain)==0):
	                break
                if domain not in pool.keys():
                        pool[domain]=[]
                pos = urls.tell()
                pool[domain].append(pos)
print "Writing urls"

while True:
        for x in pool.keys():
                pos = pool[x].pop()
                urls.seek(pos)
                uri.write(urls.readline())
                if(len(pool[x])==0):
                        del pool[x]
        if(len(pool.keys())==0):
                break

uri.close()
urls.close()
print "Done"

