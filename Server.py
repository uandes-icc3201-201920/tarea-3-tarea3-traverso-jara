import socket
import _thread
import pickle

host = (socket.gethostbyname_ex(socket.gethostname()))[-1][-1]
port = 4445

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((host, port))
    print(f"IP: {host}")
except socket.error:
    print("Bind error")

s.listen(10)
datos = {}

def verificar(mensaje):
    comandos = ["insert(", "get(", "peek(", "update(", "delete(" ]
    for comando in comandos:
        if comando == mensaje[:len(comando)] and mensaje[-1] == ")":
            return (comando[:-1],mensaje[len(comando):-1])
    return 0

def Thread(conn):
    conn.send(bytes("Conectado!","utf-8"))
    while True:
        mensaje = conn.recv(1024)
        mensaje = mensaje.decode("utf-8")
        if mensaje == "disconnect" or mensaje == "quit":
            respuesta = "Chao!."
            respuesta = pickle.dumps(respuesta)
            conn.send(respuesta)
            break
        elif mensaje == "list":
            respuesta = datos
        else:
            data = verificar(mensaje)
            if data == 0:
                respuesta = 40
            #mutex
            elif data[0] == "insert" :
                if ',' in data[1]:
                    index = data[1].index(',')
                    dato = data[1][index+1:]
                    try:
                        key = int(data[1][:index])
                        if int(key) not in datos:
                            datos[key] = dato
                            respuesta = "elemento insertado correctamente."
                        else:
                            respuesta = 60
                    except:
                        respuesta = 60
                else:
                    contador = 0
                    while True:
                        if contador not in datos:
                            break
                        contador += 1
                    datos[contador] = data[1]
                    respuesta = "Elemento insertado correctamente."
            elif data[0] == "update":
                try:
                    if ',' in data[1]:
                        index = data[1].index(',')
                        key = int(data[1][:index])
                        dato = data[1][index+1:]
                        datos[key] = dato
                        respuesta = "Elemento actualizado."
                    else:
                        respuesta = 50
                except:
                    respuesta = 50
            elif data[0] == "delete":
                try:
                    if int(data[1]) in datos:
                        del datos[int(data[1])]
                        respuesta = "Elemento eliminado."
                    else:
                        respuesta = 80
                except:
                    respuesta = 50
            #mutex
            elif data[0] == "get":
                try:
                    if int(data[1]) in datos:
                        respuesta = datos[int(data[1])]
                    else:
                        respuesta = 50
                except:
                    respuesta = 50
            elif data[0] == "peek":
                try:
                    if int(data[1]) in datos:
                        respuesta = True
                    else:
                        respuesta = False
                except:
                    respuesta = 50
        respuesta = pickle.dumps(respuesta)
        conn.send(respuesta)

    conn.close()
    print("Cliente desconectado")

while True:
    conn, addr = s.accept()
    print(f"Conectado con {addr[0]}:{addr[1]}")
    print("Cliente conectado")
    _thread.start_new_thread(Thread, (conn,))

s.close()