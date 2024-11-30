import numpy as np
import secrets
from numpy.linalg import norm

# Parameters for Lattice Cryptography
N = 512  # Lattice dimension
Q = 12289  # A large prime modulus
SIGMA = 3.2  # Standard deviation for error sampling

# Gaussian Sampling for Error Terms
def sample_error(size):
    """
    Samples error terms from a discrete Gaussian distribution.
    Uses rejection sampling to simulate Gaussian distribution with mean 0 and standard deviation SIGMA.
    """
    error = np.random.normal(0, SIGMA, size=size)
    return np.round(error).astype(int) % Q

# Key Generation
def key_generation():
    """
    Generates public and private keys using lattice-based Learning With Errors (LWE).
    """
    # Private key: small, random coefficients in Z_q
    s = np.random.randint(0, Q, size=N)
    
    # Public key: (A, b = A*s + e) where A is a random matrix, e is a small error vector
    A = np.random.randint(0, Q, size=(N, N))
    e = sample_error(size=N)
    b = (A @ s + e) % Q
    
    return (A, b), s

# Encryption
def encrypt(public_key, message):
    """
    Encrypts a message using the public key (A, b).
    """
    A, b = public_key
    
    # Random vector r for encryption
    r = np.random.randint(0, 2, size=N)
    
    # Ciphertext components
    u = (r @ A) % Q
    encrypted_message = (np.dot(r, b) + message) % Q
    
    return u, encrypted_message

# Decryption
def decrypt(private_key, ciphertext):
    """
    Decrypts the ciphertext using the private key s.
    """
    u, encrypted_message = ciphertext
    s = private_key
    
    # Decrypt the message
    decrypted_message = (encrypted_message - np.dot(u, s)) % Q
    return decrypted_message

# Trapdoor Generation for Enhanced Lattice Security
def trapdoor_generation():
    """
    Generates a trapdoor function for the lattice, used for additional security and ensuring
    efficient sampling of lattice points.
    """
    T = np.random.randint(-1, 2, size=(N, N))  # Randomly generate a small trapdoor matrix
    G = np.random.randint(0, Q, size=(N, N))   # Generate a basis matrix for the lattice
    
    # Ensure G*T has a low norm, optimizing it for a lattice basis reduction algorithm
    while norm(np.dot(G, T)) > (N * SIGMA):
        T = np.random.randint(-1, 2, size=(N, N))
    
    return G, T

# Quantum-Resistant Lattice Encryption using Trapdoor
def quantum_resistant_encrypt(public_key, message, trapdoor):
    """
    Encrypts a message using lattice-based cryptography with an added trapdoor function for enhanced security.
    """
    A, b = public_key
    G, T = trapdoor
    
    # Random vector r with low norm to ensure compactness
    r = sample_error(size=N) 
    
    # Encrypt with trapdoor-enhanced basis G
    u = (r @ G) % Q
    encrypted_message = (np.dot(r, b) + message) % Q
    
    return u, encrypted_message

# Hybrid Key Exchange: Classical + Post-Quantum
def hybrid_key_exchange():
    """
    Demonstrates a hybrid approach combining classical Diffie-Hellman and quantum-resistant lattice cryptography.
    """
    # Classical Diffie-Hellman parameters (for simplicity, not real-world safe values)
    p = 23  # Prime modulus
    g = 5   # Generator

    # Alice and Bob's secrets for Diffie-Hellman
    a_secret = secrets.randbelow(p)
    b_secret = secrets.randbelow(p)
    
    # Classical DH Key Exchange
    A = pow(g, a_secret, p)
    B = pow(g, b_secret, p)
    shared_classical_key = pow(B, a_secret, p)

    # Lattice-based key exchange for quantum security
    public_key_A, private_key_A = key_generation()
    G, T = trapdoor_generation()
    
    # Encrypt a shared secret message using lattice cryptography
    message = shared_classical_key % Q
    ciphertext = quantum_resistant_encrypt(public_key_A, message, (G, T))

    return ciphertext, private_key_A

# Example Usage
if __name__ == "__main__":
    # Generate keys
    public_key, private_key = key_generation()
    
    # Encrypt and decrypt a message
    message = 42
    ciphertext = encrypt(public_key, message)
    decrypted_message = decrypt(private_key, ciphertext)

    print("Original Message:", message)
    print("Decrypted Message:", decrypted_message)

    # Hybrid Key Exchange
    ciphertext, private_key = hybrid_key_exchange()
    print("Ciphertext from Hybrid Key Exchange:", ciphertext)
# Lattice-based cryptography implementation for quantum resistance
