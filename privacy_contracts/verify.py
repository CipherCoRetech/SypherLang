from Crypto.Hash import SHA256
from Crypto.Signature import pss
from Crypto.PublicKey import RSA

def verify_proof(proof, public_key):
    """
    Verify the provided proof using a public key.

    Parameters:
        proof (dict): The proof to verify, which includes the data, its hash, and the signature.
        public_key (str): The RSA public key in PEM format.

    Returns:
        bool: True if the proof is valid, otherwise False.
    """
    try:
        # Extract data and the original hash from the proof
        data = proof["data"]
        signature = bytes.fromhex(proof["signature"])

        # Recreate the hash from the provided data
        data_hash = SHA256.new(data.encode('utf-8'))

        # Load the public key
        key = RSA.import_key(public_key)

        # Verify the signature using the hash and public key
        verifier = pss.new(key)
        verifier.verify(data_hash, signature)

        return True
    except (ValueError, TypeError):
        return False

# Example usage
if __name__ == "__main__":
    # Load or generate a public/private key pair (for demonstration)
    key_pair = RSA.generate(2048)
    public_key_pem = key_pair.publickey().export_key()
    private_key_pem = key_pair.export_key()

    # Generate proof
    from prove import generate_proof
    proof = generate_proof("Transaction details", private_key_pem)

    # Verify proof
    is_valid = verify_proof(proof, public_key_pem)
    print("Proof verification:", "Valid" if is_valid else "Invalid")
