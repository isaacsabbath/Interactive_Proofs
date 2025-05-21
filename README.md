# 🔐 Interactive Proof System over Sockets (Python)

This project demonstrates a basic **Interactive Proof (IP) system** implemented using Python sockets. It simulates a simple proof of membership in a language **L = {x | x = 13}**, using a **challenge-response protocol** between a **Prover** (client) and a **Verifier** (server).

---

## 📘 What is an Interactive Proof?

An **interactive proof system** involves two parties:

- **Prover (P)**: Wants to convince the Verifier that a given statement is true.
- **Verifier (V)**: Interacts with the Prover to validate the claim through a series of steps.

In this project, the proof revolves around proving that an input value `x` (derived from a bitstring) belongs to the language `L = {13}`.

---

##  Protocol Steps

### Prover generates and sends a claim  
The Prover (client) generates a random 5-bit binary string (e.g., `"01101"`) representing a number **x**. This bitstring is sent to the Verifier (server) as a claim that **x** belongs to the language  
\[
L = \{13\}
\]

---

### Verifier receives and validates the claim  
The Verifier converts the received bitstring into an integer value.

- If the bitstring is invalid or cannot be converted, the Verifier immediately rejects the claim and closes the connection.  
- If valid, the Verifier proceeds to the next step.

---

### Verifier sends a random challenge **r**  
To verify the claim, the Verifier generates a random integer challenge **r** (e.g., between 1 and 10) and sends it back to the Prover.

---

### Prover computes and sends proof  
The Prover calculates the proof value as:

\[
\text{proof} = (x + r) \bmod 20
\]

This proof is sent to the Verifier as a response to the challenge.

---

### Verifier checks the proof  
The Verifier validates the proof by checking if:

\[
(\text{proof} - r) \bmod 20 = x
\]

and also verifies if \( x = 13 \) (membership condition).

---

### Verifier accepts or rejects the claim  
- If the check passes and \( x = 13 \), the Verifier accepts the proof, confirming the Prover's claim that \( x \in L \).  
- Otherwise, the Verifier rejects the claim.

---

##  Example

- Prover sends: `bitstring = "01101"` → value = 13  
- Verifier sends challenge: `r = 7`  
- Prover computes: `proof = (13 + 7) % 20 = 0`  
- Verifier checks: `(0 - 7) % 20 = 13` → Accept 

If the value was not 13, the Verifier would reject.
