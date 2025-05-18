import socket
import struct
import hashlib
import random

CHUNK_SIZE = 1024
HOST = "localhost"
PORT = 12345


def handle_client(conn):
    try:
        # Receive all file data from client
        data = b""
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            data += chunk

        if not data:
            print("No data received from client.")
            return

        # Split the file data into chunks
        chunks = []
        num_chunks = (len(data) + CHUNK_SIZE - 1) // CHUNK_SIZE
        for i in range(num_chunks):
            start = i * CHUNK_SIZE
            end = start + CHUNK_SIZE
            chunks.append((i, data[start:end]))

        # Compute checksum of the original data
        checksum = hashlib.md5(data).hexdigest()
        checksum_bytes = checksum.encode()

        # Prepare and send metadata
        metadata = struct.pack("II", num_chunks, len(checksum_bytes)) + checksum_bytes
        conn.sendall(metadata)

        # Shuffle chunks to simulate out-of-order delivery
        random.shuffle(chunks)

        # Send each chunk with header (sequence number and data length)
        for seq_num, chunk_data in chunks:
            header = struct.pack("II", seq_num, len(chunk_data))
            conn.sendall(header + chunk_data)

    except Exception as e:
        print(f"Server error: {e}")
    finally:
        conn.close()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            print(f"Connected by {addr}")
            handle_client(conn)


if __name__ == "__main__":
    main()
