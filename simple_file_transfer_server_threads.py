import os
import socket
import threading
from myTar import extract

def handle_client(conn, addr):
    print(f"Connection from {addr}")
    try:
        extract(conn.fileno(), 1)
    except Exception as e:
        os.write(2, f"Error: {e}\n".encode())
    finally:
        conn.close()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 50001)
    sock.bind(server_address)
    sock.listen(5)
    print(f"Server listening on {server_address}")

    while True:
        conn, addr = sock.accept()

        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    main()
