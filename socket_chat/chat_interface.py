from appJar import gui
from ipaddress import ip_address
import threading
import socket

if __name__ == "__main__":
	print("This is not the main!")
	raise SystemExit

class Interface:

	def __init__(self, title="Chat", dimensions="1024x480"):
		self.nick, self.ip, self.port, self.app = None, None, None, None
		self.correct = False
		self.title_up = title
		self.dimensions = dimensions
		self.message = []
		self.connection = None
		self.lock = threading.Lock()

	def __pressing_first(self,  name):
		if name == "Submit" or name == "<Return>":
			self.nick = self.app.getEntry("Nick: ")
			if self.nick is None or len(self.nick) == 0:
				self.app.setLabel("initial", "Insert a nickname")
				self.app.setLabelBg("initial", "red")
				return
	
			self.ip = self.app.getEntry("IP: ")
			try:
				ip_address(self.ip)
			except ValueError:
				self.app.setLabel("initial", "Insert a correct ip")
				self.app.setLabelBg("initial", "red")
				return
	
			self.port = self.app.getEntry("Port: ")
			try:
				if len(self.port) == 0:
					self.port = 9999
				self.port = int(self.port)
			except Exception:
				self.app.errorBox("error", "Unrecognized port, set to default 9999")
				self.port = 9999
	
			if self.port <= 0 or self.port > 65535:
				self.app.setLabel("initial", "Insert a valid port number.")
				return
			self.correct = True
		self.app.stop()
	
	def first_interface(self):
		self.app = gui(self.title_up, self.dimensions)
		self.app.setBg("orange")
		self.app.setFont(16)
	
		self.app.addLabel("initial", "Welcome to the best chat EU")
		self.app.setLabelBg("initial", "green")
		self.app.setPadding([30, 30])

		self.app.addLabelEntry("Nick: ")
		self.app.setEntryMaxLength("Nick: ", 25)

		self.app.addLabelEntry("IP: ")
		self.app.setEntryMaxLength("IP: ", 15)
	
		self.app.addLabelEntry("Port: ")
		self.app.setEntryDefault("Port: ", 9999)
	
		self.app.addButtons(["Exit", "Submit"], self.__pressing_first)
		self.app.enableEnter(self.__pressing_first)
		self.app.setFocus("Nick: ")
		self.app.go()

	def __connecting(self, name):
		try:
			self.connection.connect((self.ip, self.port))
			self.app.stop()
		except:
			pass

	def waiting_connection(self):
		if not self.correct:
			raise SystemExit
		self.app = gui(self.title_up, self.dimensions)
		self.app.addLabel("waiting", "The connection is being established")
		self.app.setBg("orange")
		self.app.setPadding([30, 30])

		self.app.addButton("check", self.__connecting)
		self.app.enableEnter(self.__connecting)

		self.connection = socket.socket()
		self.connection.bind(('', self.port))

		self.app.go()

	def __enter_to_send(self, name):
		if name == "Send" or name == "<Return>":
			if self.app.getEntry("send") != "":
				message = self.nick + ": " + self.app.getEntry("send")
				self.connection.send(message.encode("utf-8"))
				self.__set_messages(message)
			self.app.clearEntry("send")
			self.app.setFocus("send")
		else:
			self.app.stop()

	def __receiving(self):
		while True:
			try:
				self.__set_messages(self.connection.recv(140).decode("utf-8"))
			except:
				break

	def __set_messages(self, msg):
		self.lock.acquire()
		self.message.append(msg)
		if len(self.message) > 22:
			self.message.pop(0)
		self.lock.release()

	def __update_history(self):
		self.app.setLabel("history", "".join([x + "\n" for x in self.message]))

	def chat_room(self):
		if not self.correct:
			raise SystemExit
		self.app = gui(self.title_up, self.dimensions)
		self.message = ["Connection established, congratz! You can start chatting."]

		self.app.addLabel("history", self.message[0])
		self.app.setLabelRelief("history", self.app.GROOVE)
		self.app.setLabelAlign("history", self.app.NW)
		self.app.setLabelHeight("history", 22)

		self.app.addEntry("send")
		self.app.setEntryMaxLength("send", 140)
		self.app.setFocus("send")

		self.app.addButtons(["Exit", "Send"], self.__enter_to_send)
		self.app.enableEnter(self.__enter_to_send)
		self.app.registerEvent(self.__update_history)

		receiver = threading.Thread(target=self.__receiving)
		receiver.start()

		self.app.go()
		self.connection.close()
