import socket

sock = socket.socket()
sock.connect(('localhost', 51234))
data_set = input().encode()
sock.send(data_set)

data = sock.recv(1024).decode()
sock.close()

print(data)
