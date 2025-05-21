import socket
import struct
import hashlib

HOST = "localhost"
PORT = 12345


def receive_all(sock, n):
    data = b""
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data


def main():
    import sys

    if len(sys.argv) != 2:
        print("Usage: python client.py <filepath>")
        return

    filepath = sys.argv[1]
    try:
        with open(filepath, "rb") as f:
            file_data = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Send file to server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(file_data)
        s.shutdown(socket.SHUT_WR)

        # Receive metadata
        metadata_header = receive_all(s, 8)
        if not metadata_header:
            print("Failed to receive metadata header.")
            return

        num_chunks, checksum_len = struct.unpack("II", metadata_header)
        checksum = receive_all(s, checksum_len)
        if not checksum:
            print("Failed to receive checksum.")
            return
        checksum = checksum.decode()

        # Receive all chunks (with verbose output)
        import time
        chunks = {}
        start_time = time.time()
        for i in range(num_chunks):
            header = receive_all(s, 8)
            if not header:
                print("Incomplete chunk header received.")
                return
            seq_num, data_len = struct.unpack("II", header)
            data = receive_all(s, data_len)
            if not data:
                print(f"Incomplete data for chunk {seq_num}.")
                return
            chunks[seq_num] = data

            # Verbose output
            elapsed = time.time() - start_time
            percent = ((i+1)/num_chunks)*100
            avg_time_per_chunk = elapsed/(i+1)
            remaining_chunks = num_chunks - (i+1)
            eta = avg_time_per_chunk * remaining_chunks
            print(f"[CLIENT] Received chunk {i+1}/{num_chunks} (seq={seq_num}, size={data_len} bytes) | {percent:.1f}% complete | ETA: {eta:.1f}s | Remaining: {remaining_chunks}")
        total_time = time.time() - start_time
        print(f"[CLIENT] All chunks received. Total time: {total_time:.2f}s. Average chunk time: {total_time/num_chunks:.3f}s.")

        # Reassemble file
        if len(chunks) != num_chunks:
            print("Missing chunks detected.")
            return

        reconstructed = b"".join(chunks[i] for i in range(num_chunks))
        computed_checksum = hashlib.md5(reconstructed).hexdigest()

        if computed_checksum == checksum:
            print("Transfer successful. Checksums match.")
        else:
            print("Transfer failed. Checksums do not match.")


if __name__ == "__main__":
    main()
