import socket
import _thread

host = socket.gethostname()
port = 4445

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((host, port))
except socket.error:
    print("Bind error")

s.listen(10)
datos = {}

def Thread(conn):
    conn.send(bytes("Conectado!","utf-8"))
    while True:
        mensaje = conn.recv(1024)
        mensaje = mensaje.decode("utf-8")
        if mensaje == "disconnect":
            break
        else:
            conn.send(bytes(mensaje,"utf-8"))

    conn.send(bytes("Chao!!!","utf-8"))
    conn.close()
    print("Cliente desconectado")

while True:
    conn, addr = s.accept()
    print(f"Conectado con {addr[0]}:{addr[1]}")
    print("Cliente conectado")
    _thread.start_new_thread(Thread, (conn,))

s.close()