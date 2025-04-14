import socket
from myTar import create

def send_file(file_path, server_address):
    data = create([file_path], 1)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(server_address)
        sock.sendall(data)
        print("File sent successfully.")

def main():
    server_address = ('localhost', 50000)
    print("Enter path of file to send:")
    file_path = input().strip()
    send_file(file_path, server_address)

if __name__ == "__main__":
    main()
