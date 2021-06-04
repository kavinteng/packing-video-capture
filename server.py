import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)

def main():
    print("start")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("listen")

    while True:
        conn, addr = server.accept()
        print("New connection : {}" .format(addr))

        filename = conn.recv(1024).decode("utf-8")
        print("received")
        file = open("serverdata/"+filename, "w")
        conn.send("received".encode("utf-8"))

        data = conn.recv(1024).decode("utf-8")
        file.write(data)

        file.close()
        conn.close()
        print("disconnect")

if __name__ == '__main__':
    main()