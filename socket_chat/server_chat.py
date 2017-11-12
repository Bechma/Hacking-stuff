import socket
import threading
from codes import Codes


class ServerChat:
	all_connections = dict()
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
				nick = connection.recv(200).decode("utf-8")
				with ServerChat.lock:
					if nick not in ServerChat.all_connections:
						ServerChat.all_connections[nick] = connection
					else:
						connection.send(Codes.ERROR + "Nickname already used")
						continue
				t = threading.Thread(target=self.listen_messages, args=(connection, nick))
				t.daemon = True
				t.start()
				print("\nConnection established | IP " + addr[0] + ":" + str(addr[1]))
			except:
				print("\nError accepting connection")
				print(ServerChat.all_connections)

	def listen_messages(self, conn, nick):
		while True:
			try:
				message = conn.recv(140).decode("utf-8")
				# Connection is closed
				if message == "":
					with ServerChat.lock:
						del ServerChat.all_connections[nick]
					conn.close()
					break
				# User is requesting a list of users connected
				elif message[0] == Codes.ASK_FOR_USERS:
					message = Codes.ASK_FOR_USERS + "\n"
					with ServerChat.lock:
						for n in ServerChat.all_connections:
							message += ("\t" + str(n) + "\n")
					conn.send(message.encode("utf-8"))
				# User is sending messages to all people
				elif message[0] == Codes.MESSAGE_TO_ALL:
					message = message.encode("utf-8")
					with ServerChat.lock:
						for c in ServerChat.all_connections:
							ServerChat.all_connections[c].sendall(message)
				# User is sending a private message
				elif message[0] == Codes.MESSAGE_TO_ONE:
					to = message.index("|")
					coming_from = message.index(":")
					other_nick = message[1:to]
					message = message[coming_from:]
					to = "**PM from " + nick + "**:" + message
					my_msg = "**PM to " + other_nick + "**:" + message
					with ServerChat.lock:
						try:
							ServerChat.all_connections[other_nick].send(to.encode("utf-8"))
							conn.send(my_msg.encode("utf-8"))
						except:
							message = Codes.ERROR + "ERROR SENDING MESSAGE TO " + other_nick
							conn.send(message.encode("utf-8"))
				else:
					print("What is this from " + nick + "??: " + message)

			except:
				with ServerChat.lock:
					del ServerChat.all_connections[nick]
				conn.close()
				print("Connection lost with " + nick)
				break


if __name__ == "__main__":
	server = ServerChat()
	server.start_accepting_connections()
