import socket
import threading
import traceback


class ServerChat:
	all_connections = list()
	lock = threading.Lock()

	def __init__(self):
		self.server = socket.socket()

		port = 9999

		try:
			self.server.bind(('', port))
		except Exception:
			print("Error binding socket.")
			raise SystemExit

		self.server.listen(10)

	def start_accepting_connections(self):
		while True:
			try:
				connection, addr = self.server.accept()
				connection.setblocking(True)
				with ServerChat.lock:
					ServerChat.all_connections.append(connection)
				t = threading.Thread(target=self.listen_messages, args=(connection,))
				t.daemon = True
				t.start()
				print("\nConnection established | IP " + addr[0] + ":" + str(addr[1]))
			except:
				print("\nError accepting connection")

	def listen_messages(self, conn):
		while True:
			try:
				print(conn)
				message = conn.recv(140)
				print("Recibido: " + str(message) + "\tDecodificado: " + message.decode("utf-8"))
				if message == "":
					with ServerChat.lock:
						ServerChat.all_connections.remove(conn)
					break
				with ServerChat.lock:
					for c in ServerChat.all_connections:
						if c != conn:
							c.sendall(message)
			except:
				traceback.print_exc()
				with ServerChat.lock:
					ServerChat.all_connections.remove(conn)
				print("Conexion perdida...")
				break
