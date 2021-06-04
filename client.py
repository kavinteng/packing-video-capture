import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP, PORT)

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    file = open("vdo/640171.mp4", "r")
    data = file.read()

    client.send("640171.mp4".encode("utf-8"))
    msg = client.recv(1024).decode("utf-8")
    print("server :{}".format(msg))

    client.send(data.encode("utf-8"))

    file.close()
    client.close()

if __name__ == '__main__':
    main()