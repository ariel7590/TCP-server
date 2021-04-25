import socket
import threading
import time

ports = [3000, 3001, 3002, 3003, 3004]
choosePort = input("Choose a port (0~4):")
portIndex = int(choosePort)
myPort = ports[portIndex]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.bind(('0.0.0.0', ports[portIndex]))
sock.listen(1)


def respond_to_client(conn, client_address):
    while True:
        try:
            data = conn.recv(1024)
            print(data.decode())
            time.sleep(2)
            conn.send('World'.encode())
        except ConnectionRefusedError:
            continue
        except ConnectionAbortedError:
            continue


def become_a_client():
    global portIndex
    global myPort
    takenPorts = []
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            portIndex = portIndex + 1
            if portIndex == 5:
                portIndex = 0
            if ports[portIndex] != myPort and ports[portIndex] not in takenPorts:
                sock.connect(('127.0.0.1', ports[portIndex]))
                takenPorts.append(ports[portIndex])
                sock.send("Hello".encode())
                data = sock.recv(1024)
                print()
                print(data.decode())
                sock.close()
        except ConnectionRefusedError:
            continue
        except ConnectionAbortedError:
            continue


threading.Thread(target=become_a_client).start()
while True:
    conn, client_address = sock.accept()
    print('new connection from', conn.getpeername())
    thread=threading.Thread(target=respond_to_client, args=(conn, client_address)).start()
