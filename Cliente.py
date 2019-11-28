import socket

host = socket.gethostname()
port = 4445

conectado = False
while True:
    mensaje = input("Mensaje: ")
    if mensaje == "connect":
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ip_remoto = socket.gethostbyname(host)
            s.connect((ip_remoto, port))
            print(s.recv(1024).decode("utf-8"))
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
                respuesta = respuesta.decode("utf-8")
                print(respuesta)
                if mensaje == "disconnect":
                    s.close()
                    conectado = False
        except socket.error:
            print("Error al enviar mensaje")

