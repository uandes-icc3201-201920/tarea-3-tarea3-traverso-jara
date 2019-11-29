import socket
import pickle

host = socket.gethostname()
host = "192.168.1.8"
port = 4445
errores = {40:"NOT FOUND", 50:"KEY NOT FOUND", 60:"ERROR INSERT", 70:"ERROR DISCONNECT", 80:"ERROR DELETE"}

conectado = False
while True:
    mensaje = input("Mensaje: ")
    if mensaje == "connect":
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ip_remoto = socket.gethostbyname(host)
            s.connect((ip_remoto, port))
            print(s.recv(4096).decode("utf-8"))
            conectado = True
        except socket.error:
            print("Error al conectar")
            continue
        try:
            while conectado:
                mensaje = input("Mensaje: ")
                try:
                    s.send(bytes(mensaje,"utf-8"))
                except socket.error:
                    print("Error al enviar mensaje")
                respuesta = s.recv(1024)
                respuesta = pickle.loads(respuesta)
                if mensaje == "list":
                    print("Key\t   Value")
                    for i in respuesta:
                        print(f"{i}\t   {respuesta[i]}")
                elif respuesta in errores:
                    print(errores[respuesta])
                else:
                    print(respuesta) # sdfsdfsdfsdfd aqui modificsr
                if mensaje == "disconnect":
                    s.close()
                    conectado = False
                elif mensaje == "Quit":
                    s.close()
                    break

        except socket.error:
            print("Error al enviar mensaje")