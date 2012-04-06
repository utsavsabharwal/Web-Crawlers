import sys
assert len(sys.argv) > 1, "Pass directory name as a parameter"
dir = sys.argv[1]
import urlparse
import MySQLdb as mdb
import hashlib
import unicodedata
insert = open(dir+"/insert.log").readlines() #list of urls:::productids
update = open(dir+"/update.log").readlines() #list of uids:::urls
success = open(dir+"/success.log").readlines() #list of uids to be updated
failure = open(dir+"/failure.log").readlines() #list of uids to be disabled
query = open(dir+"/query","a+")
success = list(set(success))
failure = list(set(failure))
update = list(set(update))
insert = list(set(insert))


def get_hostname_from_url(url):
    hostname = urlparse.urlparse(url).hostname
    if not hostname:
        return False
    return hostname

def get_rdomain_from_url(url):
    hostname = get_hostname_from_url(url)
    if not hostname:
        return False
    rdomain = hostname.split('.')
    rdomain = u'.'.join(rdomain[-1::-1])
    return rdomain


for uid in success:
	try:
		uid=int(uid.strip())
		q = "update url_queue set is_disabled = 0, last_fetch = now() where uid = %s;"%uid
		query.write(q+chr(10))
	except Exception, ex:
		print "Error in Success ", ex

for uid in failure:
	try:
		uid = int(uid.strip())
		q="update url_queue set is_disabled=1, last_fetch = now() where uid = %s;"%uid
		query.write(q+chr(10))
	except Exception, ex:
		print "Error in Failure", ex
		
for x in update:
	try:
		uid, url = x.split(":::")
		uid = int(uid.strip())
		url = url.strip()
		url = url.decode('windows-1252')
		url = mdb.escape_string(url)
		domain = get_rdomain_from_url(url)
		if not domain:
			print "Error in update. No domain"
		try:
            		url_hash = hashlib.sha256(url).hexdigest()
		except Exception, ex:
            		print "Error in update Hash Failure", ex
		q = """update ignore url_queue set is_disabled = 0, last_fetch=now(), url="%s", rdomain="%s", url_hash="%s" where uid=%s;"""%(url, domain, url_hash, uid)
		query.write(q+chr(10))
	except Exception, ex:
		print "Error in update.", ex
		print uid, url
		
for x in insert:
	try:
		url, product_id = x.split(":::")
		product_id = int(product_id.strip())
		url = url.strip()
		url = url.decode('windows-1252')
		url = mdb.escape_string(url)		
		domain = get_rdomain_from_url(url)
		if not domain:
			print "Error in update. No domain"
		try:
            		url_hash = hashlib.sha256(url).hexdigest()
		except Exception, ex:
            		print "Error in update Hash Failure", ex
		q = """insert ignore into url_queue set is_disabled = 1, last_fetch=now(), next_fetch=now(), url ="%s", rdomain="%s", url_hash="%s", product_id=%s;"""%(url, domain, url_hash, product_id)
		query.write(q+chr(10))
	except Exception, ex:
		print "Error in insert.", ex
