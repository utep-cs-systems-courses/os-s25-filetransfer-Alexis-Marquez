import os
import socket
import sys

from myTar import extract

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 3311)
    sock.bind(server_address)
    sock.listen(5)
    print(f"Server listening on {server_address}")

    while True:
        conn, addr = sock.accept()
        print(f"Accepted connection from {addr}")

        pid = os.fork()

        if pid == 0:
            sock.close()
            try:
                extract(conn.fileno(), 1)
            except Exception as e:
                os.write(2, f"Error: {e}\n".encode())
            conn.close()
            sys.exit(1)
        else:
            conn.close()

if __name__ == "__main__":
    main()
