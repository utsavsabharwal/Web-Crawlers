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
thread_started=[]
#urls=["https://www.acuprice.com/Products/Overview/?id=M005926853:::247:::247"]
urls=open("urls").readlines()
#urls=urls[:10000]
class Crawler(Thread):
	def __init__(self, id):
		#print id
		Thread.__init__(self)
		self.crawl()

	def crawl(self):
	   try:		
		thread_started.append("ok")
		try:
			#required urls(list) format: url(str/split):::filename(int):::product_id(int)
		  domain, filename, url, product_id = urls.pop().split("\t")	
		  domain = domain.strip()
		  if domain not in invalid_domains:		  
			filename=int(filename.strip())
			url=str(url.strip())
			product_id=int(product_id.strip())
			fname = str(filename)+".uss"
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
				print "oye"
				response_code = str(c.getinfo(pycurl.HTTP_CODE))
				pattern = filename+":::"+response_code+chr(10)			
				print "failure", pattern
				failure.append(pattern)	
		  else:
                        failure.append(str(filename)+chr(10))
	
		except Exception, ex:
			failure.append(str(filename)+chr(10))
			print "===", int(ex[0])
			if(ex[0]==6):
				invalid_domains.append(domain)
			print "Eerror:", ex
			pass
		  
		try:
			thread_started.pop()
		except Exception, ex:
			print "Error:", ex
			pass
	   except Exception, ex:
		print ex

def run(pid, *args):
		print "Core thread", pid
		while True:
			t=Crawler(cc.id)
	    		t.start()
			t.join()
	    		cc.id+=1
	
x=0
while x<100:
	th="thread no:"+str(x)
	thread.start_new_thread(run,(th,2))
	x+=1


while len(urls) > 1000:
	time.sleep(10)
	pass
print "O got out of the loop", len(urls)

s=open("success.log","w+")
f=open("failure.log","w+")
i=open("insert.log","w+")
u=open("update.log","a+")
invalid= open("invalid_domains.log","a+")
while len(success)>0:
	s.write(success.pop()+chr(10))
s.close()
while len(failure)>0:
	f.write(failure.pop()+chr(10)) 
f.close()
while len(insert)>0:
	i.write(insert.pop()+chr(10))
i.close()
while len(update)>0:
	u.write(update.pop()+chr(10))
u.close()
while len(invalid_domains)>0:
	invalid.write(invalid_domains.pop()+chr(10))	
invalid.close()
