import socket
import threading
import random
import time
from bitstring import Bits

HEADER = 8
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def send_msg(conn, msg):
    msg_bytes = msg.encode(FORMAT)
    msg_len = str(len(msg_bytes)).encode(FORMAT)
    msg_len += b' ' * (HEADER - len(msg_len))
    conn.send(msg_len)
    conn.send(msg_bytes)

def recv_msg(conn):
    msg_len_data = conn.recv(HEADER)
    if not msg_len_data:
        return None
    msg_len = int(msg_len_data.decode(FORMAT).strip())
    msg = conn.recv(msg_len).decode(FORMAT)
    return msg

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    # Step 1: Receive bitstring claim from prover
    bit_string = recv_msg(conn)
    if bit_string is None:
        conn.close()
        return
    print(f"[RECEIVED] bitstring: {bit_string} from {addr}")

    time.sleep(1)  # Pause to visualize reception

    try:
        value = int(Bits(bin=bit_string))
    except:
        value = None

    if value is None:
        send_msg(conn, "Invalid bitstring format. Rejecting.")
        conn.close()
        return

    # Step 2: Send random challenge r
    r = random.randint(1, 20)
    send_msg(conn, str(r))
    print(f"[CHALLENGE] Sent challenge r={r} to {addr}")

    time.sleep(1)  # Pause to visualize sending challenge

    # Step 3: Receive proof from prover
    proof_msg = recv_msg(conn)
    if proof_msg is None:
        conn.close()
        return

    try:
        proof = int(proof_msg)
    except:
        send_msg(conn, "Invalid proof format. Rejecting.")
        conn.close()
        return

    print(f"[PROOF] Received proof={proof} from {addr}")

    time.sleep(1)  # Pause to visualize proof reception

    # Step 4: Verify proof
    # Check (proof - r) mod 20 == value and value == 13
    if (proof - r) % 20 == value and value == 13:
        response = "Accepted: proof verified, x ∈ L"
    else:
        response = f"Rejected: proof invalid, x = {value} ∉ L"

    send_msg(conn, response)
    print(f"[RESPONSE] Sent verification result to {addr}")

    conn.close()

def start():
    server.listen()
    print("[STARTING] Server is listening...")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

start()
