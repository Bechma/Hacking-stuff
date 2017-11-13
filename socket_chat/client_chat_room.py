import tkinter as tk
from threading import Lock


class Interface(tk.Frame):
	locked = Lock()

	def __init__(self, root, client):
		tk.Frame.__init__(self, root)

		self.canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
		self.frame = tk.Frame(self.canvas, background="#ffffff")
		self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=self.vsb.set)

		self.vsb.pack(side="right", fill="y")
		self.canvas.pack(side="top", fill="both", expand=True)
		self.canvas.create_window((4, 4), window=self.frame, anchor="nw", tags="self.frame")

		self.frame.bind("<Configure>", self.__configure_frame)

		tk.Label(root, text="Enter to send").pack(side="bottom", fill="both")
		self.entry = tk.Entry(root)
		self.entry.pack(side="bottom", fill="both")
		self.entry.focus()
		self.entry.bind("<Return>", self.__listening)

		self.client = client
		self.row_control = 0

	def populate(self, nick, message):
		with Interface.locked:
			tk.Label(self.frame, text="%s" % nick, width=len(nick), borderwidth="1", relief="solid").\
				grid(row=self.row_control, column=0)
			tk.Label(self.frame, text=message).grid(row=self.row_control, column=1)
			self.row_control += 1

	def __configure_frame(self, event):
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))

	def __listening(self, key):
		message = self.entry.get()
		if message != "":
			self.entry.delete(0, "end")
			self.client.send_to_server(message)
