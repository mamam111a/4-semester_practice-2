import socket

def client() -> None:
    HOST = '127.0.0.1'  
    PORT = 5500         

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))  

    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        print(data, end="")  
        message = input()
        client_socket.send(message.encode())

        if message.lower().strip() == "exit":
            break

    client_socket.close()

if __name__ == '__main__':
    client()
