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

   ```bash
   python client.py path/to/your/file.txt
   ```

3. **Check the Output:**

   The client will print the transfer status and checksum verification result.

## Sample Output

Below is a screenshot of the client and server after a successful file transfer:
Server:
<img width="1099" alt="Screenshot 2025-05-21 at 12 02 35" src="https://github.com/user-attachments/assets/3bc21e42-33d5-4ed4-9f01-42b32959a5ff" />

Client:
<img width="1098" alt="Screenshot 2025-05-21 at 12 02 45" src="https://github.com/user-attachments/assets/d91be2ad-9129-4875-aa50-d57b97a2daea" />


## Test Files

Sample test files are included in the repository.  
You can use these files to quickly test the functionality of the file transfer system.
Contributors

- [Yashwanth KS](https://github.com/Yashwanth-KS)
