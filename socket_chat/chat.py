import socket
import threading

print("Welcome to the greatest chat ever.")
name = input("Nick?:")
ip = input("IP to connect with: ")
puerto = input("Port?: ")

conexion = socket.socket()
conexion.bind(('', int(puerto)))
input("Waiting to my other m8: ")
conexion.connect((ip, int(puerto)))
print("Conexion stablished, congratz! You can start chatting")


class modulo(threading.Thread):
    def __init__(self, n):
        threading.Thread.__init__(self)
        self.n = n

    def cliente(self):
        while True:
            message = input(name + ": ")
            conexion.send("{}: {}".format(name, message).encode("utf-8"))

    def servidor(self):
        while True:
            print("\n" + conexion.recv(1024).decode("utf-8"))

    def run(self):
        if self.n == 1:
            self.servidor()
        else:
            self.cliente()

try:
    h1 = modulo(1)
    h2 = modulo(2)
    h1.start()
    h2.start()
    h1.join()
    h2.join()
except:
    print("ERROR")
