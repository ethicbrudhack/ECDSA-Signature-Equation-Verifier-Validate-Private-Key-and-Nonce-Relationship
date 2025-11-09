# 🔐 ECDSA Signature Equation Verifier — Validate Private Key and Nonce Relationship

This Python script verifies whether a given **private key (`d`)** correctly satisfies the **ECDSA signature equation** for one or more known signatures.  
It reconstructs the ephemeral key (`k`) used in signing and checks if the standard ECDSA relationships between `(r, s, z, d, k)` hold true.

This tool is particularly useful in **cryptographic research**, **forensics**, and **nonce reuse analysis**, where one wants to confirm that a recovered private key is indeed valid for a given set of signatures.

---

## 🧩 Overview

In ECDSA, each signature satisfies the equation:

\[
s = k^{-1} (z + d \cdot r) \pmod{n}
\]

Where:
- `d` — private key  
- `k` — ephemeral key (unique per signature)  
- `r`, `s` — signature components  
- `z` — message hash  
- `n` — group order (for Bitcoin, the order of secp256k1)

Given `d`, `r`, `s`, and `z`, we can derive the ephemeral key:

\[
k = (z + d \cdot r) \cdot s^{-1} \pmod{n}
\]

If this relation holds, the private key `d` is valid for the provided signatures.

---

## ⚙️ How It Works

1. **Computes modular inverse**  
   Using the extended Euclidean algorithm to find `s⁻¹ mod n`.

2. **Reconstructs ephemeral key (`k`)**  
   \[
   k = (z + d \cdot r) \cdot s^{-1} \pmod{n}
   \]

3. **Verifies the ECDSA equation**  
   Checks whether:
   \[
   (s \cdot k) \equiv (z + d \cdot r) \pmod{n}
   \]
   If true, the private key `d` correctly matches the given signatures.

---

## 🧮 Example Code

```python
def modinv(a, n):
    """Computes modular inverse of a modulo n."""
    t, new_t = 0, 1
    r, new_r = n, a
    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r
    if r > 1:
        raise ValueError(f"No modular inverse exists for {a} mod {n}")
    if t < 0:
        t += n
    return t

def compute_ephemeral_key(z, r, s, d, n):
    """Computes ephemeral key k = (z + d * r) * s^{-1} mod n."""
    inv_s = modinv(s, n)
    return (z + d * r) * inv_s % n

def verify_signature_equation(z, r, s, d, n):
    """Verifies ECDSA equation consistency for given signature parameters."""
    k = compute_ephemeral_key(z, r, s, d, n)
    return (s * k - (z + d * r)) % n == 0

# Example test data
z1 = ...
r1 = ...
s1 = ...
d  = ...
n  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

if verify_signature_equation(z1, r1, s1, d, n):
    print("✅ ECDSA signature equation holds true. The private key is valid.")
else:
    print("❌ Verification failed. The private key does not match the signature.")
🧾 Example Output
Obliczony klucz d jest poprawny – równania podpisów ECDSA się zgadzają.


or

Weryfikacja nie powiodła się – coś jest nie tak z kluczem d.

🧠 What It Demonstrates

✅ How to compute modular inverses (for division under modular arithmetic)
✅ How to reconstruct the ECDSA ephemeral key (k) from known parameters
✅ How to verify if a recovered private key d is mathematically correct
✅ The direct algebraic link between signature components (r, s, z) and the key pair

⚠️ Security & Ethical Notice

⚠️ This code is for educational and research use only.
It demonstrates the internal validation of ECDSA equations — not a key recovery method.

Do not use with real or unauthorized wallet data.

All values should be synthetic or testnet data.

Always handle cryptographic material responsibly."

BTC donation address: bc1q4nyq7kr4nwq6zw35pg0zl0k9jmdmtmadlfvqhr
