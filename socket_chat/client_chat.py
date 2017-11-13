from ipaddress import ip_address
import threading
import socket
from client_chat_room import *
from codes import Codes
import traceback


class ClientChat:
	DECISION = Codes.MESSAGE_TO_ALL
	DESTINY_NICKNAME = ""

	def __init__(self):
		self.nick, self.ip, self.port = None, None, None
		self.message = []
		self.connection = None
		self.chat_open = False
		self.nfile = 0

	def start_chat(self):
		self.nick = str(input("Insert a nick: "))
		while self.nick is None or len(self.nick) == 0 or not str.isalpha(self.nick):
			self.nick = str(input("Insert an alphanumeric nickname: "))

		while True:
			try:
				self.ip = str(input("Insert an IP: "))
				ip_address(self.ip)
				break
			except ValueError:
				pass
		self.port = 9999
		self.connection = socket.socket()

		self.__waiting_connection()

	def __waiting_connection(self):
		try:
			print("Connecting...")
			self.connection.connect((self.ip, self.port))
			self.connection.send(self.nick.encode("utf-8"))
			handshake = self.connection.recv(140).decode("utf-8")
			if handshake[0] == Codes.ERROR:
				print("NICKNAME ALREADY IN USE")
				self.connection.close()
				self.start_chat()
				return
			self.__chat_room()
		except InterruptedError:
			print("Connexion interrupted.")
			raise SystemExit
		except socket.timeout:
			print("Connexion is taking too long.")
			raise SystemExit
		except ConnectionRefusedError:
			print("Connexion refused.")
			raise SystemExit

	def __manage_chat(self):
		print("...:::Insert a command:::...")
		print("'list' to list users connected to the server")
		print("'all' change the chat to send messages to ALL connected users")
		print("'send <NICK>' send messages to a specific user")
		print("'file <NICK>' to send a file to another user")
		while self.chat_open:
			command = str(input("INSERT A COMMAND: "))
			if command == "list" or command == 'l':
				print("CHANGE MESSAGE TO LIST USERS")
				ClientChat.DECISION = Codes.ASK_FOR_USERS
			elif command == "all" or command == 'a':
				print("CHANGE MESSAGE TO SEND TO ALL")
				ClientChat.DECISION = Codes.MESSAGE_TO_ALL
			elif command[0:4] == "send":
				command = command[5:]
				if str.isalpha(command):
					ClientChat.DECISION = Codes.MESSAGE_TO_ONE
					ClientChat.DESTINY_NICKNAME = command
					print("CHANGE MESSAGE TO SEND MESSAGES TO " + ClientChat.DESTINY_NICKNAME)
				else:
					print("Bad nickname")
			elif command[0:4] == "file":
				command = command[5:]
				if str.isalpha(command):
					ClientChat.DECISION = Codes.FILE_TO_ONE
					ClientChat.DESTINY_NICKNAME = command
					print("CHANGE MESSAGE TO SEND FILE TO " + ClientChat.DESTINY_NICKNAME)
				else:
					print("Bad nickname")
			else:
				print("Command not recognized")
			print()

	def __initialize_chat_interface(self):
		self.chat_open = True
		try:
			master = tk.Tk()
			self.interface = Interface(master, self)
			self.interface.pack(side="top", fill="both", expand=True)
			master.mainloop()
		except:
			print("Chat closed")
			self.chat_open = False

	def __receive_from_server(self):
		while True:
			try:
				message = self.connection.recv(1024).decode("utf-8")
				print("Mensaje: " + message)
				if message[0] == Codes.MESSAGE_TO_ALL or message[0] == Codes.MESSAGE_TO_ONE:
					delimiter = message.index(":")
					nick = message[1:delimiter]
					message = message[delimiter+1:]
					self.interface.populate(nick, message)
				elif message[0] == Codes.ASK_FOR_USERS:
					print("Those are all users connected right now:" + message[1:])
				elif message[0] == Codes.FILE_TO_ONE:
					print(message[1:])
					file = self.connection.recv(2**26).decode("utf-8")
					create = open("received_%04d" % self.nfile, "x")
					create.write(file)
					print(self.connection.recv(1024).decode("utf-8"))
				elif message[0] == Codes.ERROR:
					print(message[1:])

			except ValueError:
				print("Server is sick, received something wrong :(")
			except OSError:
				print("Connection closed")
				raise SystemExit

	def send_to_server(self, message):
		if ClientChat.DECISION == Codes.ASK_FOR_USERS:
			self.connection.send(Codes.ASK_FOR_USERS.encode("utf-8"))
		elif ClientChat.DECISION == Codes.MESSAGE_TO_ALL:
			to_server = Codes.MESSAGE_TO_ALL + self.nick + ":" + message
			self.connection.send(to_server.encode("utf-8"))
		elif ClientChat.DECISION == Codes.MESSAGE_TO_ONE:
			to_server = Codes.MESSAGE_TO_ONE + ClientChat.DESTINY_NICKNAME + "|" + self.nick + ":" + message
			self.connection.send(to_server.encode("utf-8"))
		elif ClientChat.DECISION == Codes.FILE_TO_ONE:
			try:
				message = open(message, "r").read()
				to_server = Codes.FILE_TO_ONE + ClientChat.DESTINY_NICKNAME + "|" + message
				self.connection.sendall(to_server.encode("utf-8"))
			except IOError:
				print("FILE NOT VALID")

	def __chat_room(self):
		print("Connection established, congratz! You can start chatting.")
		threading.Thread(target=self.__initialize_chat_interface).start()
		while not self.chat_open:
			pass
		threading.Thread(target=self.__manage_chat).start()
		self.__receive_from_server()

		self.connection.close()


if __name__ == "__main__":
	ClientChat().start_chat()
