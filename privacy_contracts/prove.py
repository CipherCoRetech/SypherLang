from Crypto.Hash import SHA256
from Crypto.Signature import pss
from Crypto.PublicKey import RSA

def generate_proof(data, private_key):
    """
    Generate a cryptographic proof for the given data using a private key.

    Parameters:
        data (str): The input data for which proof needs to be generated.
        private_key (str): The RSA private key in PEM format.

    Returns:
        dict: A dictionary containing the original data, a signature for verification,
              and the hash of the data to ensure integrity.
    """
    # Create hash of the data
    data_hash = SHA256.new(data.encode('utf-8'))

    # Load private key
    key = RSA.import_key(private_key)

    # Sign the hash using the private key
    signature = pss.new(key).sign(data_hash)

    # Return a dictionary that includes data, hash, and signature
    proof = {
        "data": data,
        "hash": data_hash.hexdigest(),
        "signature": signature.hex()
    }

    return proof

# Example usage
if __name__ == "__main__":
    # Load or generate a private key (for demonstration)
    key_pair = RSA.generate(2048)
    private_key_pem = key_pair.export_key()

    # Generate proof
    data = "Transaction details"
    proof = generate_proof(data, private_key_pem)
    print("Generated Proof:", proof)
