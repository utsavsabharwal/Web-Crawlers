import sys
assert len(sys.argv) > 1, "Pass directory name as a parameter"
dir = sys.argv[1]
import pycurl
import thread
import time
import config as cc

from threading import Thread
success=[] #list of uids with urls for which we need to set last_fetch=now() and next_fetch="2012-12-12"
failure=[] #list of uids with urls for which we need to set last_fetch=now() and is_disabled=1
update=[] #list of uids, urls sperated by :::
insert=[] #list of urls with product id to be inserted

invalid_domains=[]
invalid_domain=[]
thread_started=[]
#INPUT FORMAT: domain[\t]filename[\t]url[\t]product_id
urls=open(dir+"/urls")
class Crawler(Thread):
	def __init__(self, id):
		#print id
		Thread.__init__(self)
		self.crawl()

	def crawl(self):
	   try:		
		thread_started.append("ok")
		try:
		  
		
		  content = urls.readline()
		  if(len(content)==0):
			print "Terminating"
			cc.terminate += 1
			return
		  domain, filename, url, product_id = content.split("\t")	
		  domain = domain.strip()
		  if domain not in invalid_domain:		  
			filename=int(filename.strip())
			url=str(url.strip())
			product_id=int(product_id.strip())
			fname = dir+"/"+str(filename)+".uss"
			c = pycurl.Curl()
			c.fp = open(fname,"a+")
			c.setopt(pycurl.FOLLOWLOCATION, 1)
			c.setopt(pycurl.MAXREDIRS, 5)
			c.setopt(pycurl.CONNECTTIMEOUT, 30)
			c.setopt(pycurl.TIMEOUT, 300)
			c.setopt(pycurl.NOSIGNAL, 1)
			c.setopt(pycurl.URL, url)
			c.setopt(pycurl.WRITEDATA, c.fp)
			c.perform()
			original_url = str(url)
			final_url = str(c.getinfo(pycurl.EFFECTIVE_URL))
			c.fp.close()
			if not c.errstr():
				if(original_url==final_url):
					success.append(str(filename))
				else:
					update.append(str(filename)+":::"+final_url)			
					insert.append(str(original_url)+":::"+str(product_id))
			else:
				#print "oye"
				response_code = str(c.getinfo(pycurl.HTTP_CODE))
				pattern = filename+":::"+response_code+chr(10)			
				print "failure", pattern
				failure.append(pattern)	
		  else:
                        failure.append(str(filename)+chr(10))
	
		except Exception, ex:
			failure.append(str(filename)+chr(10))
			print int(ex[0])
			if(ex[0]==6):
				invalid_domains.append(domain)
			pass
		  
		try:
			thread_started.pop()
		except Exception, ex:
			print "Error:", ex
			pass
	   except Exception, ex:
		print ex
		raise

def run(pid, *args):
		print "Core thread", pid
		while (cc.terminate == 0):
			t=Crawler(cc.id)
	    		t.start()
			t.join()
			print cc.id
	    		cc.id+=1
	
x=0
error = open("error.log","a+")
while x<100 and (cc.terminate == 0):
	try:
		th="thread no:"+str(x)
		thread.start_new_thread(run,(th,2))
		x+=1
	except Exception, ex:
		print ex
		error.write(str(time.time())+":"+str(ex))
error.close()

'''
while len(urls) > 1000:
	time.sleep(10)
	pass

print "O got out of the loop", len(urls)
'''
s=open(dir+"/success.log","w+")
f=open(dir+"/failure.log","w+")
i=open(dir+"/insert.log","w+")
u=open(dir+"/update.log","a+")
invalid= open(dir+"/invalid_domains.log","a+")

while (cc.terminate == 0):
	while len(success)>0:
		s.write(success.pop()+chr(10))
	s.flush()
	while len(failure)>0:
		f.write(failure.pop()+chr(10)) 
	f.flush()
	while len(insert)>0:
		i.write(insert.pop()+chr(10))
	i.flush()
	while len(update)>0:
		u.write(update.pop()+chr(10))
	u.flush()
	while len(invalid_domains)>0:
		dd = invalid_domains.pop()
		invalid_domain.append(dd)
		invalid.write(dd+chr(10))	
	invalid.flush()
