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

        # Send each chunk with header (sequence number and data length) and verbose output
        import time
        total_bytes_sent = 0
        start_time = time.time()
        for i, (seq_num, chunk_data) in enumerate(chunks):
            header = struct.pack("II", seq_num, len(chunk_data))
            conn.sendall(header + chunk_data)
            total_bytes_sent += len(chunk_data)
            elapsed = time.time() - start_time
            percent = ((i+1)/num_chunks)*100
            avg_time_per_chunk = elapsed/(i+1)
            remaining_chunks = num_chunks - (i+1)
            eta = avg_time_per_chunk * remaining_chunks
            print(f"[SERVER] Sent chunk {i+1}/{num_chunks} (seq={seq_num}, size={len(chunk_data)} bytes) | {percent:.1f}% complete | ETA: {eta:.1f}s | Bytes sent: {total_bytes_sent}")
        total_time = time.time() - start_time
        print(f"[SERVER] All chunks sent. Total time: {total_time:.2f}s. Average chunk time: {total_time/num_chunks:.3f}s. Total bytes sent: {total_bytes_sent}")

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
