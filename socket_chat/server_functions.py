import socket
import threading


class ServerChat:
	def __init__(self):
		self.all_connections = []
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
				self.all_connections.append(connection)
				t = threading.Thread(target=self.listen_messages, args=(connection,))
				t.daemon = True
				t.start()
				print("\nConnection established | IP " + addr[0] + ":" + str(addr[1]))
			except:
				print("\nError accepting connection")

	def listen_messages(self, conn):
		while True:
			try:
				message = conn.recv(140)
				print("Recibido: " + message + "\tDecodificado: " + message.decode("utf-8"))
				if message == "":
					self.all_connections.remove(conn)
					break
				self.server.sendall(message)
				# self.send_message_to_all(message, conn)
			except:
				self.all_connections.remove(conn)
				print("Conexion perdida...")
				break

	def send_message_to_all(self, message, conn):
		for i, other in enumerate(self.all_connections):
			if conn != other:
				if other.send(message) == 0:
					self.all_connections.remove(other)
