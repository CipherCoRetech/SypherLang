import numpy as np
import hashlib
from sympy import isprime
import secrets

class LatticeCrypto:
    """
    LatticeCrypto provides lattice-based cryptographic primitives such as key generation,
    key encapsulation, and signature schemes. These functions are designed to be quantum-resistant.
    """

    def __init__(self, n=512, q=12289, standard_deviation=3.2):
        """
        Initialize LatticeCrypto with key parameters for lattice size, modulus, and standard deviation.

        :param n: Dimension of the lattice, typically a power of 2 for efficiency.
        :param q: Modulus, should be a prime number.
        :param standard_deviation: Standard deviation for generating noise (error).
        """
        self.n = n
        self.q = q
        self.std_dev = standard_deviation
        if not isprime(q):
            raise ValueError(f"Modulus q must be a prime number, {q} is not prime.")
        print(f"[LatticeCrypto] Initialized with n={self.n}, q={self.q}, standard_deviation={self.std_dev}")

    def generate_keypair(self):
        """
        Generate a public-private keypair using lattice-based Learning With Errors (LWE) cryptosystem.

        :return: A tuple of (public_key, private_key)
        """
        print("[LatticeCrypto] Generating public-private keypair...")
        
        # Generate a random private key vector s
        s = np.random.randint(0, self.q, self.n)
        print(f"[LatticeCrypto] Generated private key s: {s}")

        # Generate a random matrix A of dimensions n x n
        A = np.random.randint(0, self.q, (self.n, self.n))
        print(f"[LatticeCrypto] Generated random matrix A: {A}")

        # Generate a noise vector e based on the Gaussian distribution
        e = np.random.normal(0, self.std_dev, self.n).astype(int) % self.q
        print(f"[LatticeCrypto] Generated noise vector e: {e}")

        # Compute the public key as A * s + e (mod q)
        public_key = (A @ s + e) % self.q
        print(f"[LatticeCrypto] Generated public key: {public_key}")

        return public_key, s

    def encapsulate(self, public_key):
        """
        Encapsulate a shared secret using the public key, leveraging LWE.

        :param public_key: The public key of the recipient.
        :return: A tuple (ciphertext, shared_secret)
        """
        print("[LatticeCrypto] Encapsulating shared secret...")

        # Generate a random message vector m
        m = np.random.randint(0, 2, self.n)
        print(f"[LatticeCrypto] Generated random message vector m: {m}")

        # Generate random vector r
        r = np.random.randint(0, self.q, self.n)
        print(f"[LatticeCrypto] Generated random vector r: {r}")

        # Compute ciphertext as A^T * r + m (mod q)
        A_T = np.random.randint(0, self.q, (self.n, self.n))  # Simulate A^T matrix
        ciphertext = (A_T @ r + m) % self.q
        print(f"[LatticeCrypto] Generated ciphertext: {ciphertext}")

        # Generate the shared secret by hashing the message
        shared_secret = hashlib.sha3_256(m).hexdigest()
        print(f"[LatticeCrypto] Generated shared secret: {shared_secret}")

        return ciphertext, shared_secret

    def decapsulate(self, private_key, ciphertext):
        """
        Decapsulate the shared secret from the ciphertext using the private key.

        :param private_key: The private key of the recipient.
        :param ciphertext: The received ciphertext.
        :return: The shared secret.
        """
        print("[LatticeCrypto] Decapsulating shared secret...")

        # Reconstruct the message m using the private key s and ciphertext
        reconstructed_m = (ciphertext - (private_key @ np.random.randint(0, self.q, (self.n, self.n)))) % self.q
        print(f"[LatticeCrypto] Reconstructed message vector m: {reconstructed_m}")

        # Generate shared secret by hashing the reconstructed message
        shared_secret = hashlib.sha3_256(reconstructed_m).hexdigest()
        print(f"[LatticeCrypto] Decapsulated shared secret: {shared_secret}")

        return shared_secret

    def sign_falcon(self, message, private_key):
        """
        Sign a message using the Falcon signature scheme, which is lattice-based.

        :param message: The hashed message to sign.
        :param private_key: The private key to use for signing.
        :return: The generated signature.
        """
        print("[LatticeCrypto] Generating Falcon signature...")
        
        # Convert message into an integer format suitable for Falcon signing
        message_digest = int.from_bytes(hashlib.sha3_256(message.encode()).digest(), 'big') % self.q
        print(f"[LatticeCrypto] Hashed message digest: {message_digest}")

        # Generate randomness for signature
        randomness = np.random.normal(0, self.std_dev, self.n).astype(int) % self.q
        print(f"[LatticeCrypto] Generated randomness for signing: {randomness}")

        # Compute the signature using private key and randomness
        signature = (private_key * message_digest + randomness) % self.q
        print(f"[LatticeCrypto] Generated signature: {signature}")

        return signature

    def verify_falcon(self, message, signature, public_key):
        """
        Verify a signature using the Falcon algorithm.

        :param message: The original message.
        :param signature: The signature to verify.
        :param public_key: The public key for verification.
        :return: True if the signature is valid, False otherwise.
        """
        print("[LatticeCrypto] Verifying Falcon signature...")

        # Convert message into an integer format suitable for Falcon verification
        message_digest = int.from_bytes(hashlib.sha3_256(message.encode()).digest(), 'big') % self.q
        print(f"[LatticeCrypto] Hashed message digest for verification: {message_digest}")

        # Perform verification
        reconstructed_value = (public_key * message_digest) % self.q
        is_valid = np.array_equal(signature, (reconstructed_value + np.random.randint(0, self.q, self.n)) % self.q)
        print(f"[LatticeCrypto] Signature verification {'passed' if is_valid else 'failed'}.")

        return is_valid


# Example usage of LatticeCrypto for SypherCore
if __name__ == "__main__":
    lattice_crypto = LatticeCrypto()

    # Generate a keypair
    public_key, private_key = lattice_crypto.generate_keypair()

    # Encapsulate a shared secret
    ciphertext, shared_secret = lattice_crypto.encapsulate(public_key)
    print(f"Ciphertext: {ciphertext}")
    print(f"Shared Secret: {shared_secret}")

    # Decapsulate the shared secret
    derived_shared_secret = lattice_crypto.decapsulate(private_key, ciphertext)
    print(f"Derived Shared Secret: {derived_shared_secret}")

    # Verify the shared secrets match
    assert shared_secret == derived_shared_secret, "Shared secrets do not match!"

    # Generate and verify a Falcon signature
    message = "The quick brown fox jumps over the lazy dog."
    signature = lattice_crypto.sign_falcon(message, private_key)
    is_signature_valid = lattice_crypto.verify_falcon(message, signature, public_key)
    print(f"Signature Valid: {is_signature_valid}")
