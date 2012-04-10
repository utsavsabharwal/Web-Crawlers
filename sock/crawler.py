import socket
from urlparse import urlparse

class abc:
	def __init__(self):
		urls = ['http://docs.python.org/release/3.1.3/library/urllib.parse.html']
		self.run(urls)
		
	def create_socket(self):
		return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def remove_socket(self, sock):
		sock.close()
		del sock

	def run(self, urls):
		for url in urls:
			scheme, self.host, path, params, query, fragment = urlparse(url)
			self.uri = url[url.find(self.host)+len(self.host):]
			self.send_request(self.create_socket())
		
	def send_request(self, sock):
		l = ''
		print self.uri, self.host
		line1 = "GET %s HTTP/1.1"%(self.uri)
		line2 = "Host: %s"%(self.host)
		line3 = "Connection: close"
		for line in (line1, line2, line3):  
			print "--", line
			l+= (line + "\r\n")
		sock.send(l)
		sock.send("\r\n")
		
a = abc()


'''
sock = create_socket()
print "Connecting"
sock.connect( ('en.wikipedia.org', 80) )
print "Sending Request"

import socket
sock = socket.socket()
sock.connect(('en.wikipedia.org', 80))

for line in (
    "GET /wiki/List_of_HTTP_header_fields HTTP/1.1",
    "Host: en.wikipedia.org",
    "Connection: close",
):
    sock.send(line + "\r\n")
sock.send("\r\n")

while True:
    content = sock.recv(1024)
    if content:
        print content
    else:
        break'''
