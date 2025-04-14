import os
import sys


def extract(extractFromFd, extractToFd):
    try:
        name_length_bytes = read_n_bytes(extractFromFd, 8)
        name_length = int.from_bytes(name_length_bytes, byteorder='little')

        file_name_bytes = read_n_bytes(extractFromFd, name_length)
        file_name = file_name_bytes.decode()

        file_size_bytes = read_n_bytes(extractFromFd, 8)
        file_size = int.from_bytes(file_size_bytes, byteorder='little')

        remaining = file_size
        while remaining > 0:
            chunk = os.read(extractFromFd, min(1024, remaining))
            if not chunk:
                raise EOFError(f"Expected {remaining} more bytes of file data, got EOF")
            os.write(extractToFd, chunk)
            remaining -= len(chunk)

    except EOFError as e:
        os.write(2, f"Extraction error: {e}\n".encode())
        sys.exit(1)



def read_n_bytes(fd, num_bytes):
    data = b''
    while len(data) < num_bytes:
        chunk = os.read(fd, num_bytes - len(data))
        if not chunk:
            raise EOFError(f"Expected {num_bytes} bytes, got only {len(data)}")
        data += chunk
    return data



def create(files, writeToFd):
    output_file = b''

    for i in range(0, len(files)):
        curr_file = os.open(files[i], os.O_RDONLY)

        filename = files[i]

        encoded_filename = filename.encode('utf-8')
        length_name = len(encoded_filename).to_bytes(8, byteorder='little')

        output_file += length_name

        output_file += encoded_filename

        file_size = os.fstat(curr_file).st_size.to_bytes(8, byteorder='little')
        output_file += file_size

        file_byte = os.read(curr_file, 1)
        while file_byte:
            output_file += file_byte
            file_byte = os.read(curr_file, 1)

        os.close(curr_file)
    os.write(writeToFd, output_file)
    return output_file



def main():
    if len(sys.argv) <= 1:
        print('Usage: python myTar.py <mode>')
        sys.exit(1)

    if sys.argv[1] == 'c':
        if len(sys.argv) <= 2:
            print('Usage: python myTar.py c <filename>')
            sys.exit(1)
        create(sys.argv, 1)
    elif sys.argv[1] == 'x':
        extract(0,1)
    else:
        print('Invalid mode. Use "c" to create or "x" to extract.')
        sys.exit(1)


if __name__ == '__main__':
    main()
