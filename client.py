import socket
import secrets
import time
from bitstring import Bits
import os

HEADER = 8
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

def generate_random_bitstring(n_bits=5):
    return ''.join(str(secrets.randbits(1)) for _ in range(n_bits))

def send_msg(client, msg):
    msg_bytes = msg.encode(FORMAT)
    msg_len = str(len(msg_bytes)).encode(FORMAT)
    msg_len += b' ' * (HEADER - len(msg_len))
    client.send(msg_len)
    client.send(msg_bytes)

def recv_msg(client):
    msg_len_data = client.recv(HEADER)
    if not msg_len_data:
        return None
    msg_len = int(msg_len_data.decode(FORMAT).strip())
    msg = client.recv(msg_len).decode(FORMAT)
    return msg

def interactive_proof():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(ADDR)

        bit_string = generate_random_bitstring()
        print(f"[Prover] Generated bitstring: {bit_string}")

        # Step 1: send bitstring
        send_msg(client, bit_string)
        print("[Prover] Sent bitstring to server")
        time.sleep(1)

        # Step 2: receive challenge r
        r_str = recv_msg(client)
        if r_str is None:
            print("[Prover] Server disconnected")
            return
        if not r_str.isdigit():
            print(f"[Prover] Server error or rejection: {r_str}")
            return

        r = int(r_str)
        print(f"[Prover] Received challenge r={r}")
        time.sleep(1)

        # Step 3: compute proof
        try:
            value = int(Bits(bin=bit_string))
        except:
            value = None

        if value is None:
            print("[Prover] Invalid bitstring format")
            return

        proof = (value + r) % 20

        # Step 4: send proof
        send_msg(client, str(proof))
        print(f"[Prover] Sent proof={proof}")
        time.sleep(1)

        # Step 5: receive final response
        response = recv_msg(client)
        print(f"[Prover] Server response: {response}")

def main():
    while True:
        interactive_proof()
        print("\n--- Next proof in 3 seconds ---\n")
        time.sleep(3)  # Pause between proofs

if __name__ == "__main__":
    main()
