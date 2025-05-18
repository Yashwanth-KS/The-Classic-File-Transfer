# The-Classic-File-Transfer

A Python-based client-server system for secure file transfer over TCP sockets, featuring chunked transmission and checksum verification.

## Features

- **Reliable File Transfer**: Uses TCP sockets for guaranteed delivery
- **Chunked Transmission**: Splits files into 1024-byte chunks for efficient transfer
- **Checksum Verification**: MD5 checksum ensures file integrity
- **Out-of-Order Handling**: Reassembles chunks correctly regardless of transmission order
- **Error Detection**: Identifies missing/corrupted data through checksum mismatches

## Prerequisites

- Python 3.x
- No additional dependencies required (uses standard libraries)

## How to Run

1. **Start the Server** (in one terminal):
   ```bash
   python server.py
   ```

Server will listen on localhost:12345

2. **Run the Client (in another terminal):**

   python client.py path/to/your/file.txt

3. **Check the Output:**

   The client will print the transfer status and checksum verification result.
