import socket
sock = socket.socket()
sock.connect(('docs.python.org', 80))
for line in (
    "GET /release/3.1.3/library/urllib.parse.html HTTP/1.1",
    "Host: docs.python.org",
    "Connection: close",
):
    print line
    sock.send(line + "\r\n")
sock.send("\r\n")


